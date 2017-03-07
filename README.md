# SquamataBase

## Documentation
https://github.com/SquamataBase/SquamataBase/wiki

## Required dependencies
To use SquamataBase you will need:
+ [Python](https://python.org) (3.5.x)
+ [Django](https://www.djangoproject.com) (1.10.5+), [django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light) (3.2.1+), [django-nested-admin](https://github.com/theatlantic/django-nested-admin) (3.0.15+)
+ [SQLite](https://sqlite.org) (3.7.3+)
+ [SpatiaLite](http://www.gaia-gis.it/gaia-sins/) (4.3.0a+)
+ [Git](https://git-scm.com/)

Detailed installation instructions can be found on the websites of each required dependency. 

**NOTE:** It is _highly recommended_ way to satisfy the SpatiaLite dependency using the spatialite-tools library. To satisfy this dependency, first install [libspatialite](https://www.gaia-gis.it/fossil/libspatialite/index). Afterwards, install [spatialite-tools](https://www.gaia-gis.it/fossil/spatialite-tools/index), which is built on top of libspatialite. This ensures that SQLite and SpatiaLite communicate nicely.

## Installation
After satisfying the required dependencies, use a terminal to execute the following commands in a directory of your choosing:
After satisfying the required dependencies, use a terminal to execute the following commands in a directory of your choosing:
```bash
mkdir SquamataBase
cd SquamataBase
git clone https://github.com/SquamataBase/SquamataBase
```
After this step, open the file called `settings_local.py` and find the line that says
```python
SPATIALITE_LIBRARY_PATH = '/usr/local/lib/mod_spatialite.dylib'
```
If this does not indicate the SpatiaLite library path make sure to change it appropriately. See [here](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/spatialite/) for additional instructions. After verifying the SpatiaLite library path you can finish the installation process with these commands
```bash
git clone https://github.com/SquamataBase/SquamataBase-Fixtures-0
cd SquamataBase-Fixtures-0/Taxonomy
curl -L https://github.com/SquamataBase/SquamataBase-Fixtures-0/releases/download/v1/taxonomy.txt.zip > taxonomy.txt.zip
unzip taxonomy.txt.zip
cd ../Geography
curl -L https://github.com/SquamataBase/SquamataBase-Fixtures-0/releases/download/v1/sb_adm_boundary.sql.zip > sb_adm_boundary.sql.zip
unzip sb_adm_boundary.sql.zip
cd ../../SquamataBase
python manage.py sb_init
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
