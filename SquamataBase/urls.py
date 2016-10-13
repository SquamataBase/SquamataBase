from django.conf.urls import url, include
from django.conf import settings
from django.contrib.gis import admin
from MuseumCatalog.views import *
from Taxonomy.views import *
from Geography.views import *
from Glossary.views import *
from Bibliography.views import *
from FoodRecord.views import *

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

autocompletes = [
    url(r'^museum-autocomplete/$', MuseumAutocomplete.as_view(), 
            name='museum-autocomplete',),
    url(r'^museum-collection-autocomplete/$', MuseumCollectionAutocomplete.as_view(), 
            name='museum-collection-autocomplete',),
    url(r'^voucher-autocomplete/$', VoucherAutocomplete.as_view(), 
            name='voucher-autocomplete',),
    url(r'^taxon-autocomplete/$', TaxonAutocomplete.as_view(),
            name='taxon-autocomplete',),
    url(r'^admu-autocomplete/$', AdmUnitAutocomplete.as_view(),
            name='admu-autocomplete',),
    url(r'^placename-autocomplete/$', NamedPlaceAutocomplete.as_view(),
            name='placename-autocomplete',),
    url(r'^locality-autocomplete/$', LocalityAutocomplete.as_view(),
            name='locality-autocomplete',),
    url(r'^srs-autocomplete/$', SpatialRefSysAutocomplete.as_view(),
            name='srs-autocomplete',),
    url(r'^ontology-collection-autocomplete/$',
            OntologyCollectionAutocomplete.as_view(),
                name='ontology-collection-autocomplete',),
    url(r'^ontology-term-autocomplete/$', OntologyTermAutocomplete.as_view(),
            name='ontology-term-autocomplete',),
    url(r'^journal-autocomplete/$', JournalAutocomplete.as_view(),
            name='journal-autocomplete',),
    url(r'^book-autocomplete/$', BookAutocomplete.as_view(),
            name='book-autocomplete',),
    url(r'^reference-autocomplete/$', ReferenceAutocomplete.as_view(),
            name='reference-autocomplete',),
    url(r'^individual-autocomplete/$', IndividualAutocomplete.as_view(),
            name='individual-autocomplete',),
    url(r'^foodrecord-autocomplete/$', FoodRecordAutocomplete.as_view(),
            name='foodrecord-autocomplete',),
    url(r'^person-autocomplete/$', PersonAutocomplete.as_view(),
            name='person-autocomplete',),
]

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    
] + autocompletes

