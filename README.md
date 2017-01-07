# SquamataBase

Django web application to administer SquamataBase on macOS.

## Requirements
+ python (version 3.4 or 3.5), pip
+ django (version 1.10), django-autocomplete-light (version 3), django-nested-admin (version 3)
+ SpatiaLite

To install the Python package dependencies use `pip`
```bash
pip install django
pip install django-autocomplete-light
pip install django-nested-admin
```

The recommended way to install the SpatiaLite dependency is via HomeBrew:
```bash
brew install spatialite-tools
```

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
python manage.py sb_services start ui
```
You are now ready to start using SquamataBase. Just point your browser to http://localhost:8000. 

For more information consult the project wiki https://github.com/SquamataBase/SquamataBase/wiki.
