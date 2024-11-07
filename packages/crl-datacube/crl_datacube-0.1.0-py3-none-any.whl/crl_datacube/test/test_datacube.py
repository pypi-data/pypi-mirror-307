from crl_datacube.datacube import DataCube, XArrayAccessor, DataCubeConfig
from crl_datacube.test.test_config import caribbean_config
from coastal_resilience_utilities.utils.dataset import meters_to_degrees, open_as_ds, compressRaster
from coastal_resilience_utilities.damage_assessment.damage_assessment import exposure, damages_dollar_equivalent, apply_dollar_weights
from coastal_resilience_utilities.damage_assessment.population_assessment import main as population
from coastal_resilience_utilities.mosaic.mosaic import idw_mosaic_slim
from coastal_resilience_utilities.utils.timing import TimingContext
import logging
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
import pandas as pd
import numpy as np
from tqdm import tqdm
# from joblib import Parallel, delayed
import zarr
import os

pytest_plugins = ('pytest_asyncio',)

dc = DataCube(**caribbean_config)


BASE = "/cccr-lab/001_projects/002_nbs-adapt/001_databases/00_DATA_BY_REGION/{region}/bathymetry_0_meters.tif"
regions = [
    "MEX_01", 
    "MEX_02", 
    # "MEX_03", 
    # "MEX_04", 
    # "MEX_05", 
    # "MEX_06", 
    # "MEX_07", 
    # "MEX_08", 
    # "USA_FL_W1_05", 
    # "USA_FL_W2_06", 
    # "USA_FL_E1_07", 
    # "USA_FL_08", 
]
# floodvars = [i for i in get_all() if i.startswith("WaterDepthMax")]

def test_init():
    dc.create_dataset_schema()


def test_intake():
    for r in regions:
        bathy = rxr.open_rasterio(BASE.format(region=r)).isel(band=0)
        bathy_crs = bathy.rio.crs
        bathy = xr.where(bathy != bathy.rio.nodata, bathy, dc.nodata)
        bathy = xr.where(bathy < 0, bathy, dc.nodata)  
        bathy.rio.write_nodata(dc.nodata, inplace=True)
        bathy.rio.write_crs(bathy_crs, inplace=True)
        dc.intake_data(bathy, "bathy", group=r)
        

# def test_export():
#     dc.as_da("bathy", group="MEX_08").rio.to_raster("/app/data/bathy.tif")


def test_compile():
    base = None
    var = "bathy"
    
    def first(da1: xr.DataArray, da2: xr.DataArray):
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="All-NaN axis encountered")
        to_return = da1.copy()
        to_return.data = np.nanmax([da1.data, da2.data], axis=0)
        return to_return

    for r in regions:
        idxs = [i[1] for i in dc.get_xarray_tiles(var, group=r)]
        logging.info(len(idxs))
        logging.info(f"{r} -> {base}")
        dc.apply_function(
            first, 
            var, 
            idxs, 
            args = [
                XArrayAccessor(dc, var=var, group=base),
                XArrayAccessor(dc, var=var, group=r),
            ],
            tile_kwargs={"filter_nan": False}
        )
        print(len([i for i in dc.get_xarray_tiles(var)]))


def test_export():
    dc.as_da("bathy").rio.to_raster("/app/data/bathy.tif")


# def test_single_intake(dc, var, regions, base):

#     for r in regions:
#         da = open_as_ds(base.format(region=r))[var]
#         dc.intake_data(da, var, group=r)
        
#     base = regions[0]
#     base_idxs = [i[1] for i in dc.get_xarray_tiles(var, group=base)]
#     for r in regions[1:]:
#         r_idxs = [i[1] for i in dc.get_xarray_tiles(var, group=r)]
#         base_idxs = list(set(base_idxs + r_idxs))
#         dc.apply_function(
#             resolveFunction, 
#             var, 
#             base_idxs, 
#             args = [
#                 XArrayAccessor(dc, var=var, group=base),
#                 XArrayAccessor(dc, var=var, group=r)
#             ],
#             tile_kwargs={"filter_nan": False}
#         )
#         base = None

# def test_summary_stats():
#     dc = DataCube(**caribbean_config)
#     gdf = gpd.read_file('/app/data/gadm_410.gpkg').reset_index(drop=True)
#     # logging.info(gdf)
    
#     stats = [
#         [f"AEV-{i}", dc.summary_stats(i, gdf, group="AEV-Damages", stats=["sum"])]
#         for i in (
#             "Damages_Historic_S1",
#             "Damages_Historic_S2",
#             "Damages_Historic_S3",
#             "Damages_Historic_S4",
#             "Damages_Future2050_S1",
#             "Damages_Future2050_S2",
#             "Damages_Future2050_S3",
#             "Damages_Future2050_S4",
#         )
#     ]
    
#     stats += [
#         [f"AEV-{i}", dc.summary_stats(i, gdf, group="AEV-Population", stats=["sum"])]
#         for i in (
#             "Population_Historic_S1",
#             "Population_Historic_S2",
#             "Population_Historic_S3",
#             "Population_Historic_S4",
#             "Population_Future2050_S1",
#             "Population_Future2050_S2",
#             "Population_Future2050_S3",
#             "Population_Future2050_S4",
#         )
#     ]
#     for i, stat in stats:
#         # logging.info(stat)
#         # logging.info(gdf)
#         assert stat.shape[0] == gdf.shape[0], f"Shapes don't match: {gdf.shape} vs {stat.shape}"
    
#     logging.info([s.columns for i, s in stats])
#     stats0 = stats[0][1].rename(columns={"sum": f"{stats[0][0]}_sum"})
#     logging.info(stats0.sum())
#     for i, stat in stats[1:]:
#         stat = stat[[c for c in stat.columns if c != "geometry"]].rename(columns={"sum": f"{i}_sum"})
#         logging.info(stat)
#         stats0 = pd.merge(stats0, stat[[c for c in stat.columns if c != "geometry"]].rename(columns={"sum": f"{i}_sum"}), left_index=True, right_index=True)
#     # stats = pd.concat(buff + [s[[c for c in s.columns if c != "geometry"]].rename(columns={"sum": f"{i}_sum"}) for i, s in stats[1:]], axis=1)
    
#     logging.info(stats0)
#     # return
#     # stats0.to_file('/app/data/summary_stats.gpkg')
#     # gdf = pd.merge(gdf, stats0[[c for c in stats0.columns if c != "geometry"]], left_index=True, right_index=True)
#     gdf = pd.merge(gdf[["geometry"]], stats0[[c for c in stats0.columns if c != "geometry"]], left_index=True, right_index=True)
#     logging.info(gdf)
#     gdf.to_file('/app/data/summary_stats.gpkg')
    