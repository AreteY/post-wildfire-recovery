import os
import requests
import numpy as np
import h5py

def download_file(file_path, url):
    """Downloads a file from a url and writes file into specified path.

    The function checks if the file has already been downloaded. If the
    file exists, then the function reads the file; otherwise the
    function downloads and writes the file.

    Parameters
    ----------
    file_path : str
       Relative path to downloaded file.

    url : str
       A URL to fetch the file.

    Returns
    -------
    data : bytes
       Downloaded data file.
    """
    if not os.path.exists(file_path):
        # Download and save data if needed
        r = requests.get(url)
        with open(file_path, 'wb') as data_file:
            data_file.write(r.content)
            data = r.content
    else:
        # Read cached data
        with open(file_path, 'rb') as data_file:
            data = data_file.read()
    return data

def calc_norm_diff(band1, band2):
    """Calculates the normalized difference using two reflectance bands.

    When using a near-infrared band and a shortwave-infrared band as
    band 1 and band 2, respectively, the function calculates the
    normalized burn ratio. When using a near-infrared band and a red
    band as band 1 and band 2, respectively, the function calculates the
    normalized difference vegetation index.

    Parameters
    ----------
    band1 : numpy.ndarray
       A near-infrared reflectance band.
    band2 : numpy.ndarray
       A shortwave-infrared or red reflectance band.

    Returns
    -------
    norm_diff : numpy.ndarray
       A normalized difference band array.
    """
    if band1.shape == band2.shape:
        norm_diff = (band1 - band2) / (band1 + band2)
        return norm_diff
    else:
        print('Band 1 does not have the same shape as Band 2.')

def aop_h5refl2array(refl_filename):
    """Reads in a hdf5 file and returns an array and select metadata.

    This function is defined for the NEON AOP Reflectance hdf5 file
    format and is adapted from the NEON Tutorial "Plot a Spectral
    Signature in Python - Tiled Data".

    Parameters
    ----------
    refl_filename : str
       Relative path of reflectance hdf5 file.

    Returns
    -------
    refl_array : h5py.dataset
       Array of reflectance values.
    metadata : dict
       Dictionary containing the following metadata:
           epsg : coordinate reference system code as integer.
           *bad_band_window1 : numpy array of wavelengths to ignore.
           *bad_band_window2 : numpy array of wavelengths to ignore.
           extent : tuple of spatial extent (xmin, xmax, ymin, ymax).
           map_info : str of map information.
           *no_data_value : -9999.0
           projection : str of projection information.
           *res : dict containing 'pixel_width' and 'pixel_height'.
           *scale_factor : 10000.0
           shape : tuple of reflectance shape (y, x, number of bands).
           wavelength : h5py wavelengths dataset of the bands.
       * Asterixed values are the same for all NEON AOP hyperspectral
       reflectance files processed 2016 & after.
    """
    # Read reflectance hdf5 file
    hdf5_file = h5py.File(refl_filename, 'r')

    # Get site name
    file_attrs_string = str(list(hdf5_file.items()))
    file_attrs_string_split = file_attrs_string.split("'")
    sitename = file_attrs_string_split[1]

    # Extract reflectance dataset
    refl = hdf5_file[sitename]['Reflectance']
    refl_array = refl['Reflectance_Data']
    refl_shape = refl_array.shape

    # Create dictionary containing relevant metadata information
    metadata = {}
    metadata['shape'] = refl_array.shape
    metadata['wavelength'] = (
        refl['Metadata']['Spectral_Data']['Wavelength'])

    # Extract no data value & data scale factor
    metadata['no_data_value'] = float(
        refl_array.attrs['Data_Ignore_Value'])
    metadata['scale_factor'] = float(refl_array.attrs['Scale_Factor'])

    # Extract bad band windows
    metadata['bad_band_window1'] = (
        refl.attrs['Band_Window_1_Nanometers'])
    metadata['bad_band_window2'] = (
        refl.attrs['Band_Window_2_Nanometers'])

    # Extract projection information
    metadata['projection'] = (
        refl['Metadata']['Coordinate_System']['Proj4'][()])
    metadata['epsg'] = int(
        refl['Metadata']['Coordinate_System']['EPSG Code'][()])

    # Extract resolution from map information
    mapinfo = refl['Metadata']['Coordinate_System']['Map_Info'][()]
    mapinfo_string = str(mapinfo)
    mapinfo_split = mapinfo_string.split(",")
    metadata['res'] = {}
    metadata['res']['pixel_width'] = float(mapinfo_split[5])
    metadata['res']['pixel_height'] = float(mapinfo_split[6])

    # Extract the upper left-hand corner coordinates from map info
    xmin = float(mapinfo_split[3])
    ymax = float(mapinfo_split[4])

    # Calculate the xmax and ymin values from the dimensions
    xmax = xmin + (refl_shape[1] * metadata['res']['pixel_width'])
    ymin = ymax - (refl_shape[0] * metadata['res']['pixel_height'])

    # Store the extent
    metadata['extent'] = (xmin, xmax, ymin, ymax)

    hdf5_file.close
    return refl_array, metadata

def subset_clean_band(refl_array,metadata,band_number):
    """Extracts and cleans a reflectance band.

    The band is cleaned by applying the no data value and scale factor
    from the metadata dictionary. Adapted from the NEON Tutorial "Band
    Stacking, RGB & False Color Images, and Interactive Widgets in
    Python - Flightline Data".

    Parameters
    ----------
    refl_array: h5py.dataset
       Reflectance array of dimensions (y,x,426) from which a band is
       extracted.
    metadata: dict
       Reflectance metadata associated with reflectance array generated
       by aop_h5refl2array function.
    band_number: int
       Band number to be extracted (integer between 1-426).

    Returns
    -------
    clean_band: np.ndarray
       Subsetted band array with no data value set to NaN and scale
       factor applied.
    """
    clean_band = refl_array[:, :, band_number-1].astype(float)
    clean_band[clean_band==int(metadata['no_data_value'])]=np.nan
    clean_band = clean_band/metadata['scale_factor']

    return clean_band

def stack_subset_bands(refl_array, metadata, bands):
    """Subsets, cleans, and stacks bands from a reflectance array.

    Parameters
    ----------
    refl_array: h5py.dataset
       Reflectance array of dimensions (y,x,426) from which multiple
       bands (typically 3) are extracted.
    metadata: dict
       Reflectance metadata associated with reflectance array generated
       by aop_h5refl2array function.
    bands: tuple
       Band numbers to be stacked (integer between 1-426).

    Returns
    -------
    stacked_array: np.ndarray
       Array of subsetted, stacked bands with no data value set to NaN
       and scale factor applied.
    """
    # Calculate rows and columns of the stacked array using the extent
    rows = int(metadata['extent'][3] - metadata['extent'][2])
    cols = int(metadata['extent'][1] - metadata['extent'][0])

    # Initialize stacked array with zeros
    stacked_array = np.zeros((rows, cols, len(bands)))

    # Initialize band dictionary and names
    band_dict = {}
    band_names = []

    for i in range(len(bands)):
        band_names.append("b"+str(bands[i]))
        band_dict[band_names[i]] = subset_clean_band(
            refl_array, metadata, bands[i])
        stacked_array[...,i] = band_dict[band_names[i]]

    return stacked_array
