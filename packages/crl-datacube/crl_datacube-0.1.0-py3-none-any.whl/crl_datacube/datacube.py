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
from dataclasses import dataclass, field
import logging
import os, shutil, sys
from glob import glob
import uuid

import warnings

from coastal_resilience_utilities.utils.geo import transform_point
from coastal_resilience_utilities.utils.dataset import compressRaster, meters_to_degrees, merge_datasets
from coastal_resilience_utilities.utils.timing import TimingContext
from coastal_resilience_utilities.summary_stats.summary_stats import summary_stats2

from crl_datacube.conf import get_all

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("My Personal")
logger.propagate = True
logger.setLevel(logging.DEBUG)


@dataclass(frozen=True)
class DataCube:
    id: str
    dx: float
    epsg: int
    bounds: tuple[float, float, float, float]
    chunk_size: int
    storage: str
    varnames: list[str]
    nodata: float = 0.0
    earthmover: bool = False
    earthmover_repo: str = None

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
    

    def create_dataset_schema(self, group=None, varnames=None) -> None:
        '''
        Initialize a datacube, that has a very simple schema;
        Each index is 2D, and datasets within the cube are created for each layer
        '''
        if varnames:
            varnames_to_create = varnames
        else:
            varnames_to_create = self.varnames
        # TODO should this be more flexible, and take a schema for the dataset?
        # I lean no, since most calculations happen on a 2D level (AEB integration being the exception)
        big_ds = (
            xr_zeros(self.geobox, chunks=self.chunk_shape, dtype="float32")
            .expand_dims(
                {
                    "var": varnames_to_create,
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
        
        big_ds.to_zarr(
            self.storage,
            group=group,
            mode="w",
            encoding=encoding,
            compute=False,
        )
        
    def delete_group(self, group: str):
        import shutil
        shutil.rmtree(os.path.join(self.storage, group))
        
    def list_groups(self) -> list[str]:
        """
        List all base group names in the Zarr store, excluding datasets.
        """
        store = zarr.open(self.storage, mode='r')
        groups = []

        def visit(path, obj):
            if isinstance(obj, zarr.hierarchy.Group):
                groups.append(path.split('/')[0])

        store.visititems(visit)
        return sorted(set(groups))
    
    def list_datasets(self, group: str = None) -> list[str]:
        """
        List all datasets within a specified group in the Zarr store.
        """
        if group:
            store = zarr.open_group(self.storage, path=group, mode='r')
        else:
            store = zarr.open_group(self.storage, mode='r')
        
        datasets = []

        def visit(path, obj):
            if isinstance(obj, zarr.core.Array):
                logging.info(path)
                datasets.append(path.split('/')[0])

        store.visititems(visit)
        return sorted(set([d for d in datasets if d not in ("x", "y", "spatial_ref")]))
        
    def get_extents(
        self
    ) -> None:
        '''
        
        '''
        for idx in self.tiles._all_tiles():
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            extent = bbox.left, bbox.right, bbox.bottom, bbox.top
            yield idx, extent
    
    def get_covering_polygons(
        self
    ) -> gpd.GeoDataFrame:
        buff = []
        x = []
        y = []
        for idx, extent in self.get_extents():
            buff.append(Polygon([(extent[0], extent[2]), (extent[1], extent[2]), (extent[1], extent[3]), (extent[0], extent[3])]))
            x.append(idx[0])
            y.append(idx[1])
            
        return gpd.GeoDataFrame(pd.DataFrame({'x': x, 'y': y}), geometry=buff, crs="EPSG:4326")
        
    
    def geobox_to_rxr(self, geobox: GeoBox) -> xr.DataArray:
        # Create a dummy data array with the same shape as the Geobox
        data = np.zeros((geobox.height, geobox.width))
        data_array = xr.DataArray(data, dims=("y", "x"))
        data_array.rio.write_crs(self.crs, inplace=True)
        data_array.rio.write_transform(geobox.transform, inplace=True)

        # Set the x and y coordinates based on the Geobox
        x_coords = np.arange(geobox.width) * geobox.resolution.x + geobox.transform.c + self.dx/2.
        y_coords = np.arange(geobox.height) * geobox.resolution.y + geobox.transform.f - self.dx/2.
        data_array = data_array.assign_coords({"x": x_coords, "y": y_coords})
        data_array = data_array.rio.set_spatial_dims(x_dim="x", y_dim="y")
        data_array.rio.write_nodata(self.nodata, inplace=True)
        # Create a dataset from the data array
        return data_array
    
    def set_data(self, var: str, idx: tuple[int, int], ds: xr.DataArray, group: str = None):
        
        if group:
            src = zarr.open(self.storage, path=f'{group}/{var}')
        else:
            src = zarr.open(self.storage, path=var)
            
        if ds.y[0] < ds.y[-1]:
            ds = ds.reindex(y=ds.y[::-1])
        
        xy_slice = self.get_xy_slice(ds.shape, idx)
        src[xy_slice] = ds.data.astype("float32")
        
    
    def get_xy_slice(self, shape: tuple[int, int], idx: tuple[int, int]) -> tuple[slice, slice]:
        to_return = (
            slice(idx[0] * self.chunk_size, idx[0] * self.chunk_size + shape[0]),
            slice(idx[1] * self.chunk_size, idx[1] * self.chunk_size + shape[1]),
        )
        return to_return
        

    
    def intake_data(self, 
                    da: xr.DataArray | xr.Dataset, 
                    var: str,
                    group: str = None, 
                    only_idxs: list[tuple[int, int]] = None,
                    boxbuff: int = 0.1,
                    create_if_not_exists: bool = True
                    ) -> None:
        # Handle NoData values
        init_crs = da.rio.crs
        try:
            da = da.where(da != da.rio.nodata, self.nodata)
        except:
            da = da.where(da != da.attrs['_FillValue'], self.nodata)
        da.rio.write_nodata(self.nodata, inplace=True)
        da.rio.write_crs(init_crs, inplace=True)
        
        if group not in self.list_groups() and create_if_not_exists:
            self.create_dataset_schema(group=group)
        
        def prep_single_tile(idx: tuple[int, int], da: xr.DataArray):
            tile = self.tiles[idx]
            bbox = tile.boundingbox
            bl = transform_point(bbox.left, bbox.bottom, self.crs, da.rio.crs)
            tr = transform_point(bbox.right, bbox.top, self.crs, da.rio.crs)
            
            # Get a dummy data array with the same shape as the tile
            empty_tile_as_da = self.geobox_to_rxr(tile)
            
            # Clip the data array to the tile in the native CRS of the data array
            # Need to buffer a little bit to avoid edge effects after reprojecting
            # boxbuff = 10000
            try:
                da_clipped = da.rio.clip_box(
                    minx=bl.x - boxbuff,
                    miny=bl.y - boxbuff,
                    maxx=tr.x + boxbuff,
                    maxy=tr.y + boxbuff
                )
                # Now that data is smaller, reproject it to the tile
                da_tiled = da_clipped.rio.reproject_match(empty_tile_as_da)
                return (idx, da_tiled)
            except (rxr.exceptions.NoDataInBounds, rxr.exceptions.OneDimensionalRaster):
                return None
            
        # Get the tiles that intersect with the data array
        idxs = self.tiles_for_da(da)
        
        def f(idx):
            i = prep_single_tile(idx, da)
            if i:
                idx, da_clipped = i
                if da_clipped.max() == self.nodata:
                    return
                
                self.set_data(var, idx, da_clipped, group=group)
        
        for idx in tqdm([i for i in idxs]):
            if not only_idxs:
                f(idx)
            else:
                if idx in only_idxs:
                    f(idx)
        

            
    def get_xarray_tiles(self, var:str, filter_nan: bool = True, get_idx: tuple[int, int] = None, group: str = None) -> list[xr.DataArray]:
        if group:
            src = zarr.open(self.storage, path=f'{group}/{var}')
        else:
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
                if np.nanmin(data) == self.nodata and np.nanmax(data) == self.nodata:
                    continue
                if np.all(data == np.nan):
                    continue
            
            da = self.geobox_to_rxr(tile)
            da.data = src[xy_slice]
            da.rio.write_nodata(self.nodata, inplace=True)
            da.rio.write_crs(self.epsg, inplace=True)
            
            yield da, idx, tile
            

    def apply_function(self, f: Callable, output: str, idxs: list[tuple[int, int]], args: list = [], kwargs: dict() = dict(), tile_kwargs: dict = dict(), group: str = None):
        def process(idx):
            _args = []
            for arg in args:
                if isinstance(arg, XArrayAccessor):
                    try:
                        _args.append(arg.get_xarray_tiles(**tile_kwargs)(idx))
                    except IndexError:
                        return
            
            _kwargs = kwargs.copy()
            for key, value in _kwargs.items():
                if isinstance(value, XArrayAccessor):
                    try:
                        _kwargs[key] = value.get_xarray_tiles(**tile_kwargs)(idx)
                    except IndexError:
                        return
            
            result = f(*_args, **_kwargs)
            self.set_data(output, idx, result, group)
            
        for idx in tqdm(idxs):
            process(idx)
            
                
    def export_as_cog(self, var: str, output: str, group: str = None, idxs: list[tuple[int, int]] = None) -> None:
        id = str(uuid.uuid4())
        tmp_dir = f"/tmp/{id}"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        self.export_as_cog_tiles(var, tmp_dir, group=group, idxs=idxs)
        datasets = glob(os.path.join(tmp_dir, "*"))
        merge_datasets(datasets, output)
        
        
        
    def export_as_cog_tiles(self, var: str, output: str, group: str = None, idxs: list[tuple[int, int]] = None) -> None:
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
            
        for da, idx, tile in self.get_xarray_tiles(var, group=group):
            if idxs and idx not in idxs:
                continue
            da.rio.write_crs(self.epsg, inplace=True)
            da.rio.write_nodata(self.nodata, inplace=True)
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                compressRaster(da, f'{output}/{var}_{idx[0]}_{idx[1]}.tif')
    
        
    def as_da(self, var: str, group=None, idxs: list[tuple[int, int]] = None) -> None:
        id = str(uuid.uuid4())
        tmp_file = f"/tmp/{id}.tif"
        self.export_as_cog(var, tmp_file, group=group, idxs=idxs)
        return rxr.open_rasterio(tmp_file)
    


@dataclass(frozen=True)
class XArrayAccessor:
    dc: DataCube
    var: str
    group: str = None
    
    def get_xarray_tiles(self, **kwargs):
        return lambda idx: [i for i in self.dc.get_xarray_tiles(self.var, group=self.group, get_idx=idx, **kwargs)][0][0]
        


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

def summary_stats(dc: DataCube, var:str, gdf: gpd.GeoDataFrame, group:str=None, stats=["sum", "count"], return_with_fields: bool = False):
    logging.info(var)
    tiles = dc.get_xarray_tiles(var, group=group)
    gdf = gdf.reset_index()
    
    buff = []
    for da, idx, tile in tiles:
        bbox = tile.boundingbox
        extent = bbox.left, bbox.right, bbox.bottom, bbox.top
        _gdf = gdf.cx[extent[0]:extent[1], extent[2]:extent[3]]
        if _gdf.shape[0] == 0:
            continue
        
        output = summary_stats2(_gdf, da, stats)
        buff.append(output)
    
    output = pd.concat(buff).groupby(["index", "geometry"]).apply(lambda x: x.apply(np.nansum)).reset_index().set_index("index")
    # output = pd.concat(buff).groupby(["index", "geometry"]).sum().reset_index().set_index("index")
    if return_with_fields:
        return pd.merge(gdf, output[[c for c in output.columns if c != "geometry"]], left_index=True, right_index=True, how="left")

    else:
        gdf['dummycolumn'] = 0
        return pd.merge(gdf[["dummycolumn"]], output[[c for c in output.columns if c != "geometry"]], left_index=True, right_index=True, how="left").drop(columns=["dummycolumn"])
            # return output