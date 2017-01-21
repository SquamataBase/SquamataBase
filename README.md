# SquamataBase

## Requirements
+ python (version 3.4 or 3.5)
+ django (version 1.10), django-autocomplete-light (version 3), django-nested-admin (version 3)
+ SpatiaLite

To install the Python package dependencies use `pip`
```bash
pip install django
pip install django-autocomplete-light
pip install django-nested-admin
```

The recommended way to install the SpatiaLite dependency is to get a hold of spatialite-tools. For macOS users you can just use Homebrew:
```bash
brew install spatialite-tools
```
See the SpatiaLite website (https://www.gaia-gis.it/fossil/libspatialite/index) for more details.

## Installation
In a directory of your choosing execute the following commands.
```bash
mkdir SquamataBase
cd SquamataBase
git clone https://github.com/SquamataBase/SquamataBase-Fixtures-0
git clone https://github.com/SquamataBase/SquamataBase
cd SquamataBase-Fixtures-0/Taxonomy
curl -L https://github.com/SquamataBase/SquamataBase-Taxonomy/releases/download/v1/taxonomy.txt.zip > taxonomy.txt.zip
unzip taxonomy.txt.zip
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
