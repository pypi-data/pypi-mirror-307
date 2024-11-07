from odc.geo.geobox import GeoBox, GeoboxTiles
import odc.geo.xr
from odc.geo.xr import xr_zeros
from typing import Generator, Callable

import geopandas as gpd
import pandas as pd
import zarr
import numpy as np
import xarray as xr
import rioxarray as rxr
from shapely.geometry import Polygon

from joblib import Parallel, delayed
from tqdm import tqdm
from dataclasses import dataclass
import logging
import os, shutil

from coastal_resilience_utilities.utils.geo import transform_point
from coastal_resilience_utilities.utils.dataset import compressRaster



@dataclass(frozen=True)
class DataCube:
    id: str
    dx: float
    epsg: int
    bounds: tuple[float, float, float, float]
    varnames: str
    chunk_size: int
    storage: str
    nodata: float = 0.0

    @property
    def crs(self) -> str:
        return f"epsg:{self.epsg}"

    @property
    def geobox(self) -> GeoBox:
        return GeoBox.from_bbox(self.bounds, crs=self.crs, resolution=self.dx)

    @property
    def chunk_shape(self) -> tuple[int, int]:
        return (self.chunk_size, self.chunk_size)

    @property
    def tiles(self) -> GeoboxTiles:
        return GeoboxTiles(self.geobox, self.chunk_shape)
    
    def tiles_by_bounds(self, left: float, bottom: float, right: float, top: float) -> GeoboxTiles:
        '''
        Filter tiles to given bounds, and return the tile indexes
        '''
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            if not (
                bbox.left < right and
                bbox.right > left and
                bbox.bottom < top and
                bbox.top > bottom
            ):
                continue
            yield idx
    
    
    def tiles_for_da(self, da: xr.DataArray):
        '''
        Convenience function to reproject a DataArray
        and get the tiles associated with the bounds
        '''
        
        # Get the bounds in the native CRS
        da_bounds = da.rio.bounds()
        da_bl = transform_point(da_bounds[0], da_bounds[1], da.rio.crs, self.crs)
        da_tr = transform_point(da_bounds[2], da_bounds[3], da.rio.crs, self.crs)
            
        # Get the tiles that intersect with the data array
        return self.tiles_by_bounds(da_bl.x, da_bl.y, da_tr.x, da_tr.y)

    @property
    def num_tiles(self) -> int:
        tiles = self.tiles
        return tiles.shape[0] * tiles.shape[1]

    @property
    def num_jobs(self) -> int:
        # not exact; some of the tiles are over ocean and won't generate jobs
        return len(self.time_data) * self.num_tiles

    def create_dataset_schema(self, remove_if_exists=True) -> None:
        '''
        Initialize a datacube, that has a very simple schema;
        Each index is 2D, and datasets within the cube are created for each layer
        '''
        
        # TODO should this be more flexible, and take a schema for the dataset?
        # I lean no, since most calculations happen on a 2D level (AEB integration being the exception)
        big_ds = (
            xr_zeros(self.geobox, chunks=self.chunk_shape, dtype="float32")
            .expand_dims(
                {
                    "var": self.varnames,
                }
            )
        ).rename({"longitude": "x", "latitude": "y"}).to_dataset("var")
        
        big_ds.attrs["title"] = self.id

        lon_encoding = optimize_coord_encoding(big_ds.x.values, self.dx)
        lat_encoding = optimize_coord_encoding(big_ds.y.values, -self.dx)
        encoding = {
            "x": {**lon_encoding},
            "y": {**lat_encoding},
        }
        
        if remove_if_exists:
            if os.path.exists(self.storage):
                shutil.rmtree(self.storage)
        
        big_ds.to_zarr(
            self.storage,
            encoding=encoding,
            compute=False,
        )
        
    def get_extents(
        self
    ) -> None:
        '''
        
        '''
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            extent = bbox.left, bbox.right, bbox.bottom, bbox.top
            yield extent
    
    def get_covering_polygons(
        self
    ) -> gpd.GeoDataFrame:
        buff = []
        for extent in self.get_extents():
            buff.append(Polygon([(extent[0], extent[2]), (extent[1], extent[2]), (extent[1], extent[3]), (extent[0], extent[3])]))

        return gpd.GeoDataFrame(geometry=buff, crs="EPSG:4326")
    
    def add_path(self, path: str):
        store = zarr.open(self.storage, mode="a") 
        ds = (
            xr_zeros(self.geobox, dtype="float32")
                .rename({"longitude": "x", "latitude": "y"})
        )
        try:
            store.create_dataset(path, data=ds.data, chunks=self.chunk_shape)
        except zarr.errors.ContainsArrayError:
            pass
        
    def list_paths(self):
        store = zarr.open(self.storage, mode="r") 
        return [i for i in store.keys()]
        
    
    def geobox_to_rxr(self, geobox: GeoBox) -> xr.DataArray:
        # Create a dummy data array with the same shape as the Geobox
        data = np.zeros((geobox.height, geobox.width))
        data_array = xr.DataArray(data, dims=("y", "x"))
        data_array.rio.write_crs(self.crs, inplace=True)
        data_array.rio.write_transform(geobox.transform, inplace=True)

        # Set the x and y coordinates based on the Geobox
        x_coords = np.arange(geobox.width) * geobox.resolution.x + geobox.transform.c + self.dx/2.
        y_coords = np.arange(geobox.height) * geobox.resolution.y + geobox.transform.f - self.dx/2.
        # y_coords = y_coords[::-1]
        data_array = data_array.assign_coords({"x": x_coords, "y": y_coords})
        data_array = data_array.rio.set_spatial_dims(x_dim="x", y_dim="y")
        data_array.rio.write_nodata(self.nodata, inplace=True)
        # Create a dataset from the data array
        return data_array
    
    def set_data(self, var: str, idx: tuple[int, int], ds: xr.DataArray):
        
        src = zarr.open(self.storage, path=var)
        if ds.y[0] < ds.y[-1]:
            ds = ds.reindex(y=ds.y[::-1])
        xy_slice = self.get_xy_slice(ds.shape, idx)
        src[xy_slice] = ds.data.astype("float32")
        
    
    def get_xy_slice(self, shape: tuple[int, int], idx: tuple[int, int]) -> tuple[slice, slice]:
        return tuple(
            slice(cs * ci, cs * (ci + 1))
            for cs, ci in zip(shape, idx)
        )

    
    def intake_data(self, 
                    da: xr.DataArray | xr.Dataset, 
                    intake_var: str,
                    resolveFunction: Callable = None, expandedTiles: int = 1, njobs: int = 20 ) -> None:
        # Handle NoData values
        try:
            da = da.where(da != da.rio.nodata, self.nodata)
        except:
            da = da.where(da != da.attrs['_FillValue'], self.nodata)
        da.rio.write_nodata(self.nodata, inplace=True)
        
        def prep_single_tile(idx: tuple[int, int], da: xr.DataArray):
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            bl = transform_point(bbox.left, bbox.bottom, self.crs, da.rio.crs)
            tr = transform_point(bbox.right, bbox.top, self.crs, da.rio.crs)
            
            # Get a dummy data array with the same shape as the tile
            empty_tile_as_da = self.geobox_to_rxr(tile)
            
            # Clip the data array to the tile in the native CRS of the data array
            # Need to buffer a little bit to avoid edge effects after reprojecting
            boxbuff = 1000
            try:
                da_clipped = da.rio.clip_box(
                    minx=bl.x - boxbuff,
                    miny=bl.y - boxbuff,
                    maxx=tr.x + boxbuff,
                    maxy=tr.y + boxbuff
                )
                # Now that data is smaller, reproject it to the tile
                da_tiled = da_clipped.rio.reproject_match(empty_tile_as_da)
                return (intake_var, idx, da_tiled)
            except (rxr.exceptions.NoDataInBounds, rxr.exceptions.OneDimensionalRaster):
                logging.info("no data")
                return None
            
        # Get the tiles that intersect with the data array
        idxs = self.tiles_for_da(da)
        
        def f(idx, da):
            r = prep_single_tile(idx, da)
            if r:
                v, xy_slice, data = r
                self.set_data(v, xy_slice, data)
        
        Parallel(n_jobs=njobs)(delayed(f)(idx, da) for idx in tqdm(idxs))


    # def tile_expansion():
    #     if resolveFunction is not None:
    #         logging.info(f"Resolving {v}")
    #         xarray_buff = []
    #         new_vals = old_vals.copy()
    #         expanded_old_vals = old_vals.copy()
    #         idx_within_expanded_tile = (0, 0)
    #         for xoffs in range(-expandedTiles, expandedTiles+1):
    #             for yoffs in range(-expandedTiles, expandedTiles+1):
    #                 if xoffs == 0 and yoffs == 0:
    #                     continue
    #                 data_to_add = self.get_xarray_tiles_from_idx(v, (idx[0]+xoffs, idx[1]+yoffs))[0]
                    
    #                 if xoffs == -1 and yoffs == -1:
    #                     idx_within_expanded_tile = data_to_add.shape
    #                 try:
    #                     xarray_buff.append(data_to_add)
    #                 except:
    #                     pass
            
    #         for xidx in range(len(xarray_buff)):
    #             expanded_old_vals = xr.concat([expanded_old_vals, xarray_buff[xidx]], dim=['x', 'y']).max(dim="concat_dim")
            
    #         expanded_left, expanded_top, expanded_right, expanded_bottom = expanded_old_vals.rio.bounds()
    #         bl = transform_point(expanded_left, expanded_bottom, self.crs, ds.rio.crs)
    #         tr = transform_point(expanded_right, expanded_top, self.crs, ds.rio.crs)
    #         logging.info(bl)
    #         logging.info(tr)
    #         expanded_ds = ds.rio.clip_box(
    #             minx=bl.x,
    #             miny=bl.y,
    #             maxx=tr.x,
    #             maxy=tr.y,
    #         )
    #         expanded_var_tile = expanded_ds[v].rio.reproject_match(expanded_old_vals)
    #         mosaicked = resolveFunction(expanded_var_tile, expanded_old_vals)
    #         logging.info(mosaicked)
    #         logging.info(mosaicked.shape)
    #         expanded_xy_slice = (
    #             slice(idx_within_expanded_tile[0], idx_within_expanded_tile[0] + new_vals.shape[0], None),
    #             slice(idx_within_expanded_tile[1], idx_within_expanded_tile[1] + new_vals.shape[1], None)
    #         )
    #         logging.info(expanded_xy_slice)
    #         mosaicked = mosaicked.reindex(y=mosaicked.y[::-1])
    #         new_vals.data = mosaicked.data[expanded_xy_slice]
    #         data = new_vals
    #     else:
    #         data = var_tile``
                
                
        #         buff.append((v, xy_slice, data.compute()))
             
    def get_xarray_tiles_from_idx(self, var:str, get_idx: tuple[int, int]) -> list[xr.DataArray]:
        src = zarr.open(self.storage, path=var)
        for idx in self.tiles._all_tiles():
            if idx != get_idx:
                continue
            tile = self.tiles[idx]
            xy_slice = self.get_xy_slice(tile.shape, idx)
            da = self.geobox_to_rxr(tile)
            # da.data = np.where(np.isnan(src[xy_slice]), self.nodata, da.data)
            da.rio.write_nodata(self.nodata, inplace=True)
            
            return da, idx, tile
        
            
    def get_xarray_tiles(self, var:str, filter_nan: bool = True, get_idx: tuple[int, int] = None) -> list[xr.DataArray]:
        src = zarr.open(self.storage, path=var)
        
        for idx in self.tiles._all_tiles():
            if get_idx and idx != get_idx:
                continue
            
            tile = self.tiles[idx]
            xy_slice = tuple(
                slice(cs * ci, cs * (ci + 1))
                for cs, ci in zip(tile.shape, idx)
            )
            
            data = src[xy_slice]
            if filter_nan:
                if np.isnan(data).all():
                    continue
                if np.all(data == self.nodata):
                    continue
            
            da = self.geobox_to_rxr(tile)
            da.data = src[xy_slice]
            da.rio.write_nodata(self.nodata, inplace=True)
            da.rio.write_crs(self.epsg, inplace=True)
            
            yield da, idx, tile
            

    def apply_function(self, f: Callable, output: str, idxs: list[tuple[int, int]], njobs:int =40, **kwargs):
        # src = zarr.open(self.storage, path=output)
        def process(idx):
            _kwargs = kwargs.copy()
            for key, value in _kwargs.items():
                if isinstance(value, XArrayAccessor):
                    try:
                        _kwargs[key] = value.get_xarray_tiles()(idx)
                    except IndexError:
                        return
            result = f(**_kwargs)
            self.set_data(output, idx, result)
            
        for idx in tqdm(idxs):
            process(idx)
            
        # Parallel(n_jobs=njobs)(delayed(process)(idx) for idx in tqdm(idxs))
        
                
    def export_as_cog(self, var: str, output: str, **kwargs) -> None:
        src = zarr.open(self.storage, path=var)
        da = self.geobox_to_rxr(self.geobox)
        da.data = src
        compressRaster(
            da, 
            output,
            **kwargs
        )
        
    def as_da(self, var: str) -> None:
        src = zarr.open(self.storage, path=var)
        da = self.geobox_to_rxr(self.geobox)
        da.data = src
        da.rio.write_nodata(self.nodata, inplace=True)
        return da


@dataclass(frozen=True)
class XArrayAccessor:
    jc: DataCube
    var: str
    
    def get_xarray_tiles(self):
        return lambda idx: [i for i in self.jc.get_xarray_tiles(self.var, get_idx=idx)][0][0]
        


def optimize_coord_encoding(values, dx):
    dx_all = np.diff(values)
    # dx = dx_all[0]
    np.testing.assert_allclose(dx_all, dx), "must be regularly spaced"

    offset_codec = zarr.FixedScaleOffset(
        offset=values[0], scale=1 / dx, dtype=values.dtype, astype="i8"
    )
    delta_codec = zarr.Delta("i8", "i2")
    compressor = zarr.Blosc(cname="zstd")

    enc0 = offset_codec.encode(values)
    # everything should be offset by 1 at this point
    np.testing.assert_equal(np.unique(np.diff(enc0)), [1])
    enc1 = delta_codec.encode(enc0)
    # now we should be able to compress the shit out of this
    enc2 = compressor.encode(enc1)
    decoded = offset_codec.decode(delta_codec.decode(compressor.decode(enc2)))

    # will produce numerical precision differences
    # np.testing.assert_equal(values, decoded)
    np.testing.assert_allclose(values, decoded)

    return {"compressor": compressor, "filters": (offset_codec, delta_codec)}