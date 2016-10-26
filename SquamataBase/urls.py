from django.conf.urls import url, include
from django.contrib.gis import admin
from SquamataBase.Specimen.views import *
from SquamataBase.Taxonomy.views import *
from SquamataBase.Geography.views import *
from SquamataBase.Glossary.views import *
from SquamataBase.Bibliography.views import *
from SquamataBase.FoodRecord.views import *
from SquamataBase.api import *

autocompletes = [
    #url(r'^museum-autocomplete/$', MuseumAutocomplete.as_view(), 
    #        name='museum-autocomplete',),
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
    url(r'^journal-autocomplete/$', JournalAutocomplete.as_view(create_field='journal_name'),
            name='journal-autocomplete',),
    url(r'^book-autocomplete/$', BookAutocomplete.as_view(),
            name='book-autocomplete',),
    url(r'^reference-autocomplete/$', ReferenceAutocomplete.as_view(),
            name='reference-autocomplete',),
    url(r'^specimen-autocomplete/$', SpecimenAutocomplete.as_view(),
            name='specimen-autocomplete',),
    url(r'^foodrecord-autocomplete/$', FoodRecordAutocomplete.as_view(),
            name='foodrecord-autocomplete',),
    url(r'^person-autocomplete/$', PersonAutocomplete.as_view(create_field='first_name|last_name'),
            name='person-autocomplete',),
]

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^api/', QueryAPI.as_view(), name='api-view'),
    
] + autocompletes

