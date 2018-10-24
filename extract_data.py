import xarray as xr
import pandas as pd

data_folder = '/home/shawn/data/cmip5/'

forecast_file = data_folder + 'downscaled_cmip5_precip_forecasts.nc'

site_forecast_file = data_folder + 'site_forecasts.csv'
###########################################################

site_details = [{'sitename':'portal',
                 'latitude':31.95,
                 'longitude':-109.09}]

# or load sites using pandas


#############################################################

cmip_forecast = xr.open_dataset(forecast_file)

for site_i, site in enumerate(site_details):
    site['longitude'] += 360
    site_subset = cmip_forecast.sel(latitude=site['latitude'], longitude=site['longitude'], method='nearest')
    
    site_subset = site_subset.to_dataframe().reset_index()
    
    site_subset['sitename'] = site['sitename']
    
    if site_i == 0:
        all_site_forecasts = site_subset
    else:
        all_site_forecasts = all_site_forecasts.append(site_subset)

all_site_forecasts.to_csv(site_forecast_file)