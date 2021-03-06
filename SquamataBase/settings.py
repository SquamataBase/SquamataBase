import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths to fixture directories like this: os.path.join(BASE_FIXDIR, ...)
BASE_FIXDIR = os.path.dirname(BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'keep-me-secret'

DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'SquamataBase.Taxonomy',
    'SquamataBase.Glossary',
    'SquamataBase.Geography',
    'SquamataBase.Bibliography',
    'SquamataBase.Specimen',
    'SquamataBase.FoodRecord',
    'SquamataBase.Workbench',
    'nested_admin',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SquamataBase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Layout for the admin page

ADMIN_REORDER = {
    'app_layout': [
        'auth',
        'Workbench',
        'Specimen',
        'Bibliography',
        'FoodRecord',
        'Glossary',
        'Geography',
        'Taxonomy'
    ],
    'model_layout': {
        'Bibliography': ['Ref', 'Person', 'Journal'],
        'FoodRecord': ['FoodRecord', 'DataSet']
    },
    'exclude': {
        'apps': [
            'auth',
            'Specimen',
            'FoodRecord',
            'Geography',
            'Glossary',
            'Taxonomy'
        ],
        'app_models': {
            'Bibliography': ['Person', 'Journal']
        }
    }
}

WSGI_APPLICATION = 'SquamataBase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'squamatabase.sqlite'),
        'CONN_MAX_AGE': None,
        # when CONN_MAX_AGE is set to 0 (default) we run up against a 'ERROR: too many connections: max 64' 
        # whenever we hit 64 requests because a new connection is opened for each request. 
        # even though the connections are closed at the end of each request they appear to
        # maintain their hold on the database due to an internal leak, as discussed in this post:
        # https://groups.google.com/forum/#!topic/spatialite-users/xrV7CA_GlwM.
        # by setting CONN_MAX_AGE = None connections will never expire and when this is used
        # in combination with python manage.py runserver --nothreading these error messages
        # disappear because we reuse the same connection for each subsequent request.
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

FIXTURES = {
    'Bibliography': {
        'app_label': 'Bibliography',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
    },
    'FoodRecord': {
        'app_label': 'FoodRecord',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
    },
    'Geography': {
        'app_label': 'Geography',
        'backup': False,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
        'exclude': ['NamedPlace', 'Locality', 'SpatialRefSys'],
    },
    'Occurrence': {
        'app_label': 'Geography',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
        'exclude': ['AdmUnit', 'AdmUnitBoundary', 'SpatialRefSys'],
    },
    'Glossary': {
        'app_label': 'Glossary',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
    },
    'Specimen': {
        'app_label': 'Specimen',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
    },
    'Workbench': {
        'app_label': 'Workbench',
        'backup': True,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
    },
    'Taxonomy': {
        'app_label': 'Taxonomy',
        'backup': False,
        'dirs': [
            os.path.join(BASE_FIXDIR, 'SquamataBase-Fixtures-0'),
        ],
        'include': ['Taxon',]
    },
}

from SquamataBase.settings_local import *
