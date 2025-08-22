## First create conda environ, then install packages

# Install packages
#pip install xarray netCDF4 numpy pandas matplotlib cartopy dask pydap h5netcdf

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


# Use dask to do chunking for larger than memory computations
dc_all = ds['analysed_sst'].sel(
                        latitude=slice(33.5, 35.5), 
                        longitude=slice(-75.5, -73.5))

print(f"Size in GB: {dc_all.nbytes / 1e9:.2f} GB")  #2.75 GB
dc_all.sizes


# Load large dataset in chunks via dask
dc_chunk = dc_all.chunk({'time': 500, 'latitude': -1, 'longitude': -1})
dc_chunk
