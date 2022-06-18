import numpy as np
import xarray as xr
import rioxarray as rxr

def open_clean_band(band_path, clip_extent, valid_range=None):
    """Opens a Landsat band as an rioxarray object.

    Parameters
    ----------
    band_path : str
       Relative path to the tif file.
    clip_extent : geopandas.GeoDataFrame
       A geodataframe containing the clip extent of interest. NOTE:
       this will fail if the clip extent is in a different CRS than the
       raster data.
    valid_range : tuple (optional)
       The min and max valid range for the data. All pixels with values
       outside of this range will be masked.

    Returns
    -------
       A single xarray object with the Landsat band data.

    """
    # Clip a Landsat band to the area of interest
    band = rxr.open_rasterio(band_path, masked=True).rio.clip(
        clip_extent.geometry, from_disk=True).squeeze()

    # Mask values outside of a valid range
    if valid_range:
        mask = ((band < valid_range[0]) | (band > valid_range[1]))
        band = band.where(~mask, np.nan)

    return band

def process_bands(all_bands_path, clip_extent, stack=False):
    """Opens, cleans, and crops a list of Landsat bands.

    Parameters
    ----------
    all_bands_path : list
       Sorted list of the paths of all the Landsat bands with the same
       resolution, crs, and spatial extent.
    clip_extent : geopandas.GeoDataFrame
       A geodataframe containing the clip extent of interest. NOTE:
       this will fail if the clip extent is in a different CRS than the
       raster data.
    stack : Boolean
       If true, returns a stacked xarray object. If false, returns a
       list of xarray objects.

    Returns
    -------
       Either a stacked xarray object or a list of xarray objects.
    """
    # Open all landsat bands in a loop
    all_bands = []
    for i, aband in enumerate(all_bands_path):
        all_bands.append(open_clean_band(aband, clip_extent))
        # Assign a band number to the new xarray object
        all_bands[i]["band"] = i + 1

    if stack:
        return xr.concat(all_bands, dim="band")
    else:
        return all_bands

def masked_norm_diff(all_bands, clip_extent, pixel_qa_path, vals, calc):
    """Calculate a normalized difference and cloud mask a Landsat band.

    Parameters
    ----------
    all_bands : list
       A list containing Landsat bands as xarray objects, where band 1
       is the red band, band 2 is the near-infrared band, and band 4 is
       the shortwave-infrared 2 band.
    clip_extent: geopandas.GeoDataFrame
       A geodataframe containing the clip extent of interest. NOTE:
       this will fail if the clip extent is in a different CRS than the
       raster data.
    pixel_qa_path: str
       A path to a pixel quality-assurance tif file.
    vals: list
       A list of values for the cloud mask classes.
    calc: string
       A string denoting the type of normalized difference calculation.
       calc = 'ndvi' for a normalized difference vegetation index.
       calc = 'nbr' for a normalized burn ratio.

    Returns
    -------
    norm_diff : xarray.DataArray
        A masked xarray object containing normalized difference values.
    """
    # Open and clip landsat qa layer
    pixel_qa = rxr.open_rasterio(
        pixel_qa_path, masked=True).rio.clip(
        clip_extent.geometry, from_disk=True).squeeze()

    # Calculate NDVI
    if calc == 'ndvi':
        norm_diff = (
            all_bands[1]-all_bands[0]) / (all_bands[1]+all_bands[0])
    # Calculate NBR
    elif calc == 'nbr':
        norm_diff = (
            all_bands[1]-all_bands[3]) / (all_bands[1]+all_bands[3])

    # Apply cloud mask to NDVI
    norm_diff = norm_diff.where(~pixel_qa.isin(vals))

    return norm_diff

def masked_msavi(all_bands, clip_extent, pixel_qa_path, vals):
    """Calculate a modified soil adjusted vegetation index and cloud
    mask a Landsat band.

    The MSAVI equation has been expanded for ease of computation.

    Parameters
    ----------
    all_bands : list
       A list containing Landsat bands as xarray objects, where band 1
       is the red band and band 2 is the near-infrared band.
    clip_extent: geopandas.GeoDataFrame
       A geodataframe containing the clip extent of interest. NOTE:
       this will fail if the clip extent is in a different CRS than the
       raster data.
    pixel_qa_path: str
       A path to a pixel quality-assurance tif file.
    vals: list
       A list of values for the cloud mask classes.

    Returns
    -------
    msavi : xarray.DataArray
        A masked xarray object containing the modified soil adjusted
        vegetation index values.
    """
    # Open and clip landsat qa layer
    pixel_qa = rxr.open_rasterio(
        pixel_qa_path, masked=True).rio.clip(
        clip_extent.geometry, from_disk=True).squeeze()

    # Calculate MSAVI
    msavi = all_bands[1] + 0.5 - 0.5 * np.sqrt(
        (4 * all_bands[1] * all_bands[1]) - (
         4 * all_bands[1]) + (
         8 * all_bands[0]) + 1)

    # Apply cloud mask to MSAVI
    msavi = msavi.where(~pixel_qa.isin(vals))

    return msavi
