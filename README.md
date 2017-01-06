# SquamataBase

Django web application to administer SquamataBase.

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
cd ../SquamataBase
python manage.py sb_init
```

## Requirements
+ python 3, pip
+ django, django-autocomplete-light, django-nested-admin
+ SpatiaLite

To install the Python package dependencies use `pip`
```bash
pip install django
pip install django-autocomplete-light
pip install django-nested-admin
```

To recommended way to install the SpatiaLite dependency is via HomeBrew
```bash
brew install spatialite-tools
```
