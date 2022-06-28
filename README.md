[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6574445.svg)](https://doi.org/10.5281/zenodo.6574445)

# Post-Wildfire Recovery
This is an [Earth Lab](https://earthlab.colorado.edu) Certificate project by [Heidi Yoon](https://github.com/AreteY) studying post-wildfire recovery.

# Project Motivation and Goal
* Wildland fire is a multifaceted natural phenomenon of increasing importance to both human and ecological communities. In this project, we explore the post-wildfire recovery for the [2016 Chimney Tops 2 Fire](https://www.nps.gov/grsm/learn/chimney-tops-2-fire.htm) by spatially quantifying the vegetation recovery using hyperspectral reflectance data.
* This project highlights how high spatial resolution (1-meter) remote sensing measurements, such as hyperspectral reflectance data, can be used to study fire recovery on the order of the spatial variation on the ground.
* In this repository, we include [example notebooks](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) that process and analyze hyperspectral reflectance data to assess post-wildfire recovery.

# Project Environment
To run our project workflow, clone this repository:
```
$ git clone https://github.com/AreteY/post-wildfire-recovery.git
```
Then install the python environment described below.
## Installing and Running the Environment
1. Download the file `neon-environment.yml` from this repository, which contains instructions on how to install the environment, into the project directory `post-wildfire-recovery`.
2. Create the environment by running:
```
$ conda env create -f neon-environment.yml
```
3. Once the environment is installed, activate it by running:
```
$ conda activate earth-analytics-neon
```

# Tools and Packages Used
* io
* os
* glob
* sys
* warnings
* zipfile
* matplotlib
* numpy
* pandas
* requests
* h5py
* geopandas
* shapely
* rasterio
* rioxarray
* xarray
* earthpy
* folium

# Project Background
To learn more about our project, please see our blog post `post_wildfire_blog.ipynb` notebook and its figures in the [Reports folder](https://github.com/AreteY/post-wildfire-recovery/tree/main/reports) and the [Graphics folder](https://github.com/AreteY/post-wildfire-recovery/tree/main/graphics) (`blog-figure1-3.png` and `ig-raws.png`, `ig-raws-rose.png`, `ig-raws-rose-gust.png`), respectively.

To create the final `post_wildfire_blog.html` output, start the project environment (if needed) and make sure you are in the `reports` directory within `post-wildfire-recovery`. Then run jupyter nbconvert for the `post_wildfire_blog.html` output.
```
$ conda activate earth-analytics-neon
$ cd reports
$ jupyter nbconvert --to html --TemplateExporter.exclude_input=True post_wildfire_blog.ipynb
```

# Data Sources
## Raster data
1. [NEON Spectrometer Reflectance](https://data.neonscience.org/data-products/DP1.30006.001)
* **Reference:** National Ecological Observatory Network. Spectrometer orthorectified surface directional reflectance - mosaic (DP3.30006.001), RELEASE-2022. https://doi.org/10.48443/5er3-8n49. Dataset accessed from https://data.neonscience.org on April 15, 2022.
2. [Landsat 8 Surface Reflectance](https://www.usgs.gov/landsat-missions)
* **Reference:** Landsat Level-2 Surface Reflectance Science Product, courtesy of the U.S. Geological Survey.
Vermote, E., Justice, C., Claverie, M., & Franch, B. (2016). Preliminary analysis of the performance of the Landsat 8/OLI land surface reflectance product. Remote Sensing of Environment. http://dx.doi.org/10.1016/j.rse.2016.04.008.
Dataset accessed from https://earthexplorer.usgs.gov on June 6, 2022.

## Vector data
3. Chimney Tops 2 Fire Perimeter
* **Reference:** MTBS Data Access: Fire Level Geospatial Data. (2022, February - last revised). MTBS Project (USDA Forest Service/U.S. Geological Survey). Available: https://mtbs.gov/direct-download. Data accessed April 3, 2022.
* Available for download in this repository as [Release v1.0.0](https://github.com/AreteY/post-wildfire-recovery/releases) `chimtops2-boundary`
4. Great Smoky Mountains National Park Perimeter
* **Reference:** National Park Service- Land Resources Division. Great Smoky Mountains National Park Boundary. (December 30, 2019 - last revised). Available: https://grsm-nps.opendata.arcgis.com. Data accessed March 28, 2022.
* Available for download in this repository as [Release v1.0.1](https://github.com/AreteY/post-wildfire-recovery/releases) `grsm-boundary`
5. NEON Terrestrial Observation System Sampling Locations
* **Reference:** NEON Document Library: Spatial Data. (June 29, 2020 - last revised). Available: https://data.neonscience.org/documents. Data accessed April 18, 2022.
* Available for download in this repository as [Release v1.0.2](https://github.com/AreteY/post-wildfire-recovery/releases) `neon-tos-plot-centroids`

## Tabular data
6. [NEON Plant Presence and Percent Cover](https://data.neonscience.org/data-products/DP1.10058.001)
* **Reference:** NEON (National Ecological Observatory Network). Plant presence and percent cover (DP1.10058.001), RELEASE-2022. https://doi.org/10.48443/pr5e-1q60. Dataset accessed from https://data.neonscience.org on April 18, 2022.

# Project Workflow
<img src="graphics/workflow.png" width="100%">

The project workflow is a post-wildfire vegetation recovery analysis in which the vegetation recovery of an 1-km<sup>2</sup> area within the burn perimeter is characterized using vegetation indices and evaluated with a spectral analysis. First, vegetation indices ([NBR: normalized burn ratio](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/), [NDVI: normalized difference vegetation index](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/), [MSAVI: modified soil adjusted vegetation index](https://www.sciencedirect.com/science/article/pii/0034425794901341)) are calculated using [Landsat 8 Surface Reflectance](https://www.usgs.gov/landsat-missions) and [NEON Spectrometer Reflectance Measurements](https://data.neonscience.org/data-products/DP1.30006.001). Second, we have begun the spectral analysis by building the spectral library with the reflectance spectra and [percent cover](https://data.neonscience.org/data-products/DP1.10058.001) for NEON Terrestrial Observation System sampling locations within the fire boundary. Finally, [multiple endmember spectral band analysis](https://www.sciencedirect.com/science/article/pii/S0034425798000376?via%3Dihub) will be used to spectrally unmix the [NEON Spectrometer Reflectance Measurements](https://data.neonscience.org/data-products/DP1.30006.001) and evaluate the vegetation recovery at a sub-pixel level.

## Run Workflow
* Run the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks)  `vegetation_indices.ipynb` with the [module](https://github.com/AreteY/post-wildfire-recovery/tree/main/modules) `reflectance.py` to calculate the vegetation indices using a downloaded NEON reflectance file and to plot the results using matplotlib and earthpy. First, start the project environment if needed. Next, make sure you are in the `notebooks` directory within `post-wildfire-recovery`. Then use Jupyter Notebook to open `vegetation_indices.ipynb` in your default web browser.
```
$ conda activate earth-analytics-neon
$ cd notebooks
$ jupyter notebook vegetation_indices.ipynb
```
* Run the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `landsat_vegetation.ipynb`  with [modules](https://github.com/AreteY/post-wildfire-recovery/tree/main/modules) `landsat.py` and `reflectance.py` to calculate the vegetation indices, using downloaded Landsat 8 files, for a fire boundary and for a 1-km<sup>2</sup> area that corresponds to a NEON reflectance tile. In the notebook, we generate the shapefile `tile_274000_3947000.shp` to crop the Landsat data to the 1-km<sup>2</sup> area. All the results are plotted using matplotlib and rasterio. To start the notebook, start the project environment and make sure you are in the `notebooks` directory within `post-wildfire-recovery` if needed. Then use Jupyter Notebook to open `landsat_vegetation.ipynb` in your default web browser.
```
$ conda activate earth-analytics-neon
$ cd notebooks
$ jupyter notebook landsat_vegetation.ipynb
```
* Run the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_subplots.ipynb` with the [module](https://github.com/AreteY/post-wildfire-recovery/tree/main/modules) `reflectance.py` to determine which NEON Terrestrial Observation System plots are within a fire boundary and which plots have been sampled by the [NEON TOS Plant Presence and Percent Cover Data Product](https://data.neonscience.org/data-products/DP1.10058.001). In this notebook, find the coordinates of the subplots using the NEON API, extract the percent cover results into a pandas dataframe, and plot the results using a pivot table in matplotlib. To the start the notebook, start the project environment and make sure you are in the `notebooks` directory within `post-wildfire-recovery` if needed. Then use Jupyter Notebook to open `vegetation_subplots.ipynb` in your default web browser.
```
$ conda activate earth-analytics-neon
$ cd notebooks
$ jupyter notebook vegetation_subplots.ipynb
```
* Run the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_spectra.ipynb` with the [module](https://github.com/AreteY/post-wildfire-recovery/tree/main/modules) `reflectance.py` to plot the reflectance spectrum for each NEON Terrestrial Observation System subplot using the [output](https://github.com/AreteY/post-wildfire-recovery/tree/main/outputs) `grsm_plots_coords.csv` generated by notebook `vegetation_subplots.ipynb`. To start the notebook, start the project environment and make sure you are in the `notebooks` directory within `post-wildfire-recovery` if needed. Then use Jupyter Notebook to open `vegetation_spectra.ipynb` in your default web browser.
```
$ conda activate earth-analytics-neon
$ cd notebooks
$ jupyter notebook vegetation_spectra.ipynb
```

# Example Usage
* The vegetation indices of any NEON Airborne Observation Platform Hyperspectral Reflectance hdf5 file can be calculated using [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_indices.ipynb`. This could include the [NEON spectrometer orthorectified surface directional reflectance - mosaic data product](https://data.neonscience.org/data-products/DP3.30006.001) used in this workflow and the [NEON spectrometer orthorectified surface directional reflectance - flightline](https://data.neonscience.org/data-products/DP1.30006.001) data product.
* The vegetation indices of any [Landsat 8 scene](https://earthexplorer.usgs.gov) that overlaps a fire boundary can be calculated using [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `landsat_vegetation.ipynb`.
* Any xarray.DataArray can be cropped to a 1-km<sup>2</sup> area in UTM coordinates using [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `landsat_vegetation.ipynb`.
* The overlap of any fire boundary and any NEON Terrestrial Observation System plot can be determined using [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_subplots.ipynb`.
* The reflectance spectrum for any location in UTM coordinates for any NEON Airborne Observation Platform Hyperspectral Reflectance hdf5 file can be determined using [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_spectra.ipynb`.

# License
The post-wildfire-recovery project is under the [MIT License](https://github.com/AreteY/post-wildfire-recovery/blob/main/LICENSE.md).
