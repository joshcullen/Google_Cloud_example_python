## First create conda environ, then install packages

# This example follows much of what's included in tutorial from NMFS OpenSci
#https://nmfs-opensci.github.io/NMFSHackDays-2025/topics-2025/2025-02-28-ERDDAP-Py/erddap_xarray.html#resample-to-create-monthly-means


# Install packages (only need to run this `pip install` step for first time setting up)
pip install xarray netCDF4 numpy pandas matplotlib cartopy dask pydap h5netcdf zarr

import xarray as xr
import matplotlib.pyplot as plt
import dask

# Read in JPL MUR SST data (lazily)
url = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41"
ds = xr.open_dataset(url)

# View size of dataset
print(f"Size in TB: {ds.nbytes / 1e12:.2f} TB")
ds.sizes
ds

# Subset 1 week of data
dc = ds['analysed_sst'].sel(
  latitude=slice(25, 45), 
  longitude=slice(-130, -110), 
  time=slice('2025-08-14', '2025-08-21'))
print(f"Size in GB: {dc.nbytes / 1e9:.2f} GB")  #260 MB
dc.sizes

%%time
# Load the data into memory so the next steps are fast
dc.load()  #1 min to load

# Plot one day
dc.sel(time="'2025-08-21").plot()
plt.close()

# Create facet plot
dc.isel(time=slice(0,9)).plot(x='longitude', y='latitude', col='time', col_wrap=3)
plt.close()


# Calculate mean of all layers and pixels
dc.mean().item()

# Plot mean raster
dc.mean(dim=['time']).plot()

# Plot daily means
plt.figure()
dc.mean(dim=['latitude', 'longitude']).plot()




## Process data from cloud-optimized format (Zarr) ##
ds2 = xr.open_zarr("https://mur-sst.s3.us-west-2.amazonaws.com/zarr-v1")
print(f"Size in GB: {ds2.nbytes / 1e9:.2f} GB")  #117 TB

# Subset data in space and time
dc2 = ds2['analysed_sst'].sel(
                        lat=slice(33.5, 35.5), 
                        lon=slice(-75.5, -73.5),
                        time=slice('2003-01-01', '2006-12-31'))

# Import this subset to disk (on VM)
dc2_chunk = dc2.chunk({'time': 500, 'lat': -1, 'lon': -1})
from dask.diagnostics import ProgressBar

with ProgressBar():
    mean_all_years = dc2_chunk.mean(dim=['lat', 'lon']).compute()  #took 23 sec

# Plot daily mean SST
plt.figure()
mean_all_years.plot()
