# HydroBox


![PyPI](https://img.shields.io/pypi/v/hydrobox?color=green&logo=pypi&style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/vforwater/hydrobox?logo=github&style=flat-square)
![GitHub commit checks state](https://img.shields.io/github/checks-status/vforwater/hydrobox/main?label=build%20status&logo=github&style=flat-square)
[![DOI](https://zenodo.org/badge/129882492.svg)](https://zenodo.org/badge/latestdoi/129882492)

## Description

**The HydroBox is mainly a toolbox used in the [V-FOR-WaTer](https://vforwater.de) Project. It will be expanded to serve general hydrological data exploration with a future release.**

The HydroBox package is a toolbox for hydrological data analysis developed at the [Chair of Hydrology](https://hyd.iwg.kit.edu/english/index.php) at the
[Karlsruhe Institute of Technology (KIT)](https://kit.edu/english/index.php).

The full documentation can be found at: https://vforwater.github.io/hydrobox

HydroBox has several submodules called toolboxes, which are a collection of functions and classes for specific purposes. As of this writing, the toolboxes are:

* `geostat` for geostatistics. Mainly implemented through `scikit-gstat` and `gstools`

In development are:

* `uncertainty_framwork` for uncertainty analysis
* `bridget` for evapotranspiration tools

## Citation

If you use the package in other software or for publications, please cite it like:

>  Mirko Mälicke, 2021. VForWaTer/hydrobox: Version 0.2. doi:10.5281/zenodo.4774860

Be aware that the dependencies of hydrobox require a citation as well. The (non-exhaustive) list of packages that you must cite are:

* scipy, matplotlib, numpy   - for all toolboxes
* plotly  - for the `plotly` plotting backend
* scikit-gstat, gstools   - for the `hydrobox.geostat` toolbox   
