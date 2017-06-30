# SquamataBase

## Documentation
https://github.com/SquamataBase/SquamataBase/wiki

## Required dependencies
To use SquamataBase you will need:
+ [Python](https://python.org) (3.5+)
+ [SQLite](https://sqlite.org) (3.7.3+)
+ [SpatiaLite](http://www.gaia-gis.it/gaia-sins/) (4.3.0a+)

SpatiaLite is built on top of several required spatial libraries (GEOS, PROJ.4, GDAL), which should be installed prior to SpatiaLite. Instructions for doing so are available [here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/geolibs/). Instructions for SpatiaLite itself are [here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/). 

Windows installation is not currently supported.

## Installation
After satisfying the required dependencies, use a terminal to execute the following commands in a directory of your choosing:
```bash
mkdir SquamataBase
cd SquamataBase
mkdir SquamataBase
wget https://github.com/SquamataBase/SquamataBase/archive/2017-06-30.tar.gz
tar xzf 2017-06-30.tar.gz && mv SquamataBase-2017-06-30 SquamataBase
```
After this step, open the file called `settings_local.py` and find the line that says
```python
SPATIALITE_LIBRARY_PATH = '/usr/local/lib/mod_spatialite.dylib'
```
If this does not indicate your SpatiaLite library path make sure to change it appropriately. See [here](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/spatialite/) for additional instructions. After verifying the SpatiaLite library path you can finish the installation process with these commands
```bash
cd SquamataBase
make
```
You are now ready to start using SquamataBase. In a new terminal window you can type
```bash
squamatabase
```
to start a python shell to interface with the database or
```bash
squamatabase ui
```
to launch a user interface in your web browser.
