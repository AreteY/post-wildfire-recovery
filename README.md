[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6574445.svg)](https://doi.org/10.5281/zenodo.6574445)

# Post-Wildfire Recovery
This is an [Earth Lab](https://earthlab.colorado.edu) Certificate project by [Heidi Yoon](https://github.com/AreteY) studying post-wildfire recovery.

# Project Motivation and Goal
* Wildland fire is a multifaceted natural phenomenon of increasing importance to both human and ecological communities. In this project, we explore the post-wildfire recovery for the [2016 Chimney Tops 2 Fire](https://www.nps.gov/grsm/learn/chimney-tops-2-fire.htm) by spatially quantifying the vegetation recovery using hyperspectral reflectance data.
* This project highlights how high spatial resolution (1-meter) remote sensing measurements, such as hyperspectral reflectance data, can be used to study fire recovery on the order of the spatial variation on the ground.
* In this repository, we include [example notebooks](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) that process and analyze hyperspectral reflectance data to assess post-wildfire recovery.

# Project Environment
To run our project workflow, clone this repository and install the python environment described below.
## Installing and Running the Environment
1. Download the file `neon-environment.yml` from this repository, which contains instructions on how to install the environment, into the project directory.
2. Create the environment by running: `conda env create -f neon-environment.yml`.
3. Once the environment is installed, activate it by running: `conda activate earth-analytics-neon`.

# Tools and Packages Used
* os
* matplotlib
* numpy
* requests
* h5py
* geopandas
* earthpy
* folium

# Project Background
To learn more about our project, please see our blog post `post_wildfire_blog.ipynb` notebook and its figures in the [Reports folder](https://github.com/AreteY/post-wildfire-recovery/tree/main/reports) and the [Graphics folder](https://github.com/AreteY/post-wildfire-recovery/tree/main/graphics) (`blog-figure1-3.png` and `ig-raws.png`, `ig-raws-rose.png`, `ig-raws-rose-gust.png`), respectively.

To create the final `post_wildfire_blog.html` output, make sure you are in the `reports` directory within `post-wildfire-recovery` and run the following bash script.
```
$ jupyter nbconvert --to html --TemplateExporter.exclude_input=True post_wildfire_blog.ipynb
```

# Data Sources
## Raster data
1. [NEON LiDAR Ecosystem Structure](https://data.neonscience.org/data-products/DP3.30015.001)
* **Reference**: National Ecological Observatory Network. 2022. Data Product DP3.30015.001, Ecosystem structure. Provisional data downloaded from https://data.neonscience.org on March 31, 2022. Battelle, Boulder, CO, USA NEON. 2022.
2. [NEON Spectrometer Reflectance](https://data.neonscience.org/data-products/DP1.30006.001)
* **Reference:** National Ecological Observatory Network. Spectrometer orthorectified surface directional reflectance - mosaic (DP3.30006.001), RELEASE-2022. https://doi.org/10.48443/5er3-8n49. Dataset accessed from https://data.neonscience.org on April 15, 2022
3. [NEON LiDAR Elevation Digital Terrain Model](https://data.neonscience.org/data-products/DP3.30024.001)  
* **Reference:** National Ecological Observatory Network. Elevation - LiDAR (DP3.30024.001), RELEASE-2022. https://doi.org/10.48443/ymmp-fr93. Dataset accessed from https://data.neonscience.org on April 18, 2022
4. [LandFire Biophysical Setting and Vegetation Departure Grids. ](https://landfire.gov/index.php)
* **Reference:** LANDFIRE: LANDFIRE Remap 2016 Biophysical Settings (BPS) CONUS layer.(2020, October - last update). U.S. Department of Interior, Geological Survey, and U.S. Department of Agriculture. Available: https://landfire.gov/bps.php. Data accessed April 3, 2022.
* **Reference:** LANDFIRE: LANDFIRE Remap 2016 Vegetation Departure grid (VDEP) CONUS layer.(2020, October - last update). U.S. Department of Interior, Geological Survey, and U.S. Department of Agriculture. Available: https://landfire.gov/vdep.php. Data accessed April 3, 2022.

## Vector data
5. Chimney Tops 2 Fire Perimeter
* **Reference:** MTBS Data Access: Fire Level Geospatial Data. (2022, February - last revised). MTBS Project (USDA Forest Service/U.S. Geological Survey). Available: https://mtbs.gov/direct-download. Data accessed April 3, 2022.
* Available for download in this repository as [Release v1.0.0](https://github.com/AreteY/post-wildfire-recovery/releases) `chimtops2-boundary`
6. Great Smoky Mountains National Park Perimeter
* **Reference:** National Park Service- Land Resources Division. Great Smoky Mountains National Park Boundary. (December 30, 2019 - last revised). Available: https://grsm-nps.opendata.arcgis.com. Data accessed March 28, 2022.
* Available for download in this repository as [Release v1.0.1](https://github.com/AreteY/post-wildfire-recovery/releases) `grsm-boundary`

## Time-series data
7. [Remote Automated Weather Station (RAWS) data for Indian Grave RAWS Site](https://raws.dri.edu/cgi-bin/rawMAIN.pl?laTIND).
* **Reference:** Indian Grave RAWS hourly data for November 2016. U.S. Forest Service Fire and Aviation Management Information Technology Portal. 2022. FW13 hourly station data (station ID:407603). Downloaded from https://famit.nwcg.gov/applications/FAMWeb on April 16, 2022.

## Tabular data
8. [NEON Plant Presence and Percent Cover](https://data.neonscience.org/data-products/DP1.10058.001)
* **Reference:** NEON (National Ecological Observatory Network). Plant presence and percent cover (DP1.10058.001), RELEASE-2022. https://doi.org/10.48443/pr5e-1q60. Dataset accessed from https://data.neonscience.org on April 18, 2022.

# Project Workflow
<img src="graphics/workflow.png" width="100%">

The project workflow is a vegetation recovery analysis in which the vegetation recovery of an 1-km<sup>2</sup> area within the burn perimeter can be evaluated first by calculating vegetation indices ([NBR: normalized burn ratio](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/), [NDVI: normalized difference vegetation index](https://www.earthdatascience.org/courses/use-data-open-source-python/multispectral-remote-sensing/vegetation-indices-in-python/), [MSAVI: modified soil adjusted vegetation index](https://www.sciencedirect.com/science/article/pii/0034425794901341)). Then the index that can best discriminate between unburned and burned areas is determined by the [random forests algorithm](https://link.springer.com/article/10.1023/A:1010933404324). Finally, [multiple endmember spectral band analysis](https://www.sciencedirect.com/science/article/pii/S0034425798000376?via%3Dihub) is used to classify the vegetation at a sub-pixel level into green growth [green], standing dead or dormant vegetation [deadwood], or burned areas [char].
## Run Workflow
* Run the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks)  `vegetation_indices.ipynb` to calculate the vegetation indices using a downloaded reflectance file and to plot the results using matplotlib and earthpy. To open `vegetation_indices.ipynb` with Jupyter Notebook, make sure you are in the `notebooks` directory within `post-wildfire-recovery`. Run the following bash script to start the notebook server in your default web browser:
```
$ jupyter notebook vegetation_indices.ipynb
```

# Example Usage
* The vegetation indices of any NEON Airborne Observation Platform Hyperspectral Reflectance hdf5 file can be calculated by Workflow A. This could include the [NEON spectrometer orthorectified surface directional reflectance - mosaic data product](https://data.neonscience.org/data-products/DP3.30006.001) used in this workflow and the [NEON spectrometer orthorectified surface directional reflectance - flightline](https://data.neonscience.org/data-products/DP1.30006.001) data product.
* In addition, any boundary shapefile for the Reflectance hdf5 file could also be plotted with the reflectance in Matplotlib using the [notebook](https://github.com/AreteY/post-wildfire-recovery/tree/main/notebooks) `vegetation_indices.ipynb`.

# License
The post-wildfire-recovery project is under the [MIT License](https://github.com/AreteY/post-wildfire-recovery/blob/main/LICENSE.md).
