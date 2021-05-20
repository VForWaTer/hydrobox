# HydroBox


![PyPI](https://img.shields.io/pypi/v/hydrobox?color=green&logo=pypi&style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/vforwater/hydrobox?logo=github&style=flat-square)
[![Test and docs](https://github.com/VForWaTer/hydrobox/actions/workflows/main.yaml/badge.svg)](https://github.com/VForWaTer/hydrobox/actions/workflows/main.yaml)


**The HydroBox is mainly a toolbox used in the [V-FOR-WaTer](https://vforwater.de) Project. It will be expanded to
serve general hydrological data exploration with a future release.**

The HydroBox package is a toolbox for hydrological data analysis developed at the
[Chair of Hydrology](https://hyd.iwg.kit.edu/english/index.php) at the
[Karlsruhe Institute of Technology (KIT)](https://kit.edu/english/index.php).
HydroBox has several submodules called toolboxes, which are a collection of functions and classes for specific purposes.
As of this writing these toolboxes are:

* `geostat` for geostatistics. Mainly implemented through `scikit-gstat` and `gstools`

In development are:

* `uncertainty_framwork` for uncertainty analysis
* `bridget` for evapotranspiration tools
