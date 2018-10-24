import xarray as xr


data_folder = '/home/shawn/data/cmip5/'

final_forecast_file = data_folder + 'downscaled_cmip5_precip_forecasts.nc'
#################################
downloaded_cmip_files = [
#        'ccsm4/rcp45/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp45_r1i1p1_20060101-20151231.nc4',
        #'ccsm4/rcp45/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp45_r1i1p1_20260101-20351231.nc4',
        #'ccsm4/rcp45/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp45_r1i1p1_20160101-20251231.nc4'
        'ccsm4/rcp45/pr/BCCAv2_0.125deg_pr_day_CCSM4_rcp45_r1i1p1_20160101-20251231.nc4',
        'ccsm4/rcp45/pr/BCCAv2_0.125deg_pr_day_CCSM4_rcp45_r1i1p1_20260101-20351231.nc4',
        'ccsm4/rcp45/pr/BCCAv2_0.125deg_pr_day_CCSM4_rcp45_r1i1p1_20060101-20151231.nc4',
#        'ccsm4/rcp45/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp45_r1i1p1_20160101-20251231.nc4',
#        'ccsm4/rcp45/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp45_r1i1p1_20260101-20351231.nc4'
#        'ccsm4/rcp45/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp45_r1i1p1_20060101-20151231.nc4',
#        'ccsm4/rcp8.5/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp85_r1i1p1_20060101-20151231.nc4',
#        'ccsm4/rcp8.5/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp85_r1i1p1_20260101-20351231.nc4',
#        'ccsm4/rcp8.5/tmin/BCCA_0.125deg_tasmin_day_CCSM4_rcp85_r1i1p1_20160101-20251231.nc4',
#        'ccsm4/rcp8.5/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp85_r1i1p1_20160101-20251231.nc4'
#        'ccsm4/rcp8.5/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp85_r1i1p1_20060101-20151231.nc4',
#        'ccsm4/rcp8.5/tmax/BCCA_0.125deg_tasmax_day_CCSM4_rcp85_r1i1p1_20260101-20351231.nc4',
        'ccsm4/rcp8.5/precip/BCCAv2_0.125deg_pr_day_CCSM4_rcp85_r1i1p1_20260101-20351231.nc4',
        'ccsm4/rcp8.5/precip/BCCAv2_0.125deg_pr_day_CCSM4_rcp85_r1i1p1_20060101-20151231.nc4',
        'ccsm4/rcp8.5/precip/BCCAv2_0.125deg_pr_day_CCSM4_rcp85_r1i1p1_20160101-20251231.nc4'
        ]

downloaded_cmip_files = [data_folder + f for f in downloaded_cmip_files]
########################################
processed_file_objects = []

for f in downloaded_cmip_files:
    with xr.open_dataset(f) as file_object:
    
        # Set the unique coordinates defining each one. This will allow all
        # files to be merged as one.
        # The model name, and experiment (which is the emission scenario)
        file_object = file_object.assign_coords(model    = [file_object.model_id],
                                                scenario = [file_object.experiment_id])
        
        # attributes no longer needed
        file_object.attrs = {}
        
        processed_file_objects.append(file_object)

cmip_forecasts = xr.auto_combine(processed_file_objects)

# other variables to encode are pr and tasmax
cmip_forecasts.to_netcdf(final_forecast_file, encoding={'tasmin':{'zlib':True,
                                                                   'complevel':4, 
                                                                   'dtype':'int32', 
                                                                   'scale_factor':0.001,  
                                                                   '_FillValue': -9999},
                                                        'tasmax':{'zlib':True,
                                                                   'complevel':4, 
                                                                   'dtype':'int32', 
                                                                   'scale_factor':0.001,  
                                                                   '_FillValue': -9999},
                                                        'pr':{'zlib':True,
                                                                   'complevel':4, 
                                                                   'dtype':'int32', 
                                                                   'scale_factor':0.001,  
                                                                   '_FillValue': -9999}})

cmip_forecasts.close()