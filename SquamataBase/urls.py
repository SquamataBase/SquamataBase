from django.conf.urls import url, include
from django.contrib.gis import admin
from SquamataBase.Specimen.views import *
from SquamataBase.Taxonomy.views import *
from SquamataBase.Geography.views import *
from SquamataBase.Glossary.views import *
from SquamataBase.Bibliography.views import *
from SquamataBase.FoodRecord.views import *
from SquamataBase.views import *

autocompletes = [
    #url(r'^museum-autocomplete/$', MuseumAutocomplete.as_view(), 
    #        name='museum-autocomplete',),
    url(r'^admin/museum-collection-autocomplete/$', MuseumCollectionAutocomplete.as_view(), 
            name='museum-collection-autocomplete',),
    url(r'^admin/voucher-autocomplete/$', VoucherAutocomplete.as_view(), 
            name='voucher-autocomplete',),
    url(r'^admin/taxon-autocomplete/$', TaxonAutocomplete.as_view(),
            name='taxon-autocomplete',),
    url(r'^admin/admu-autocomplete/$', AdmUnitAutocomplete.as_view(),
            name='admu-autocomplete',),
    url(r'^admin/placename-autocomplete/$', NamedPlaceAutocomplete.as_view(),
            name='placename-autocomplete',),
    url(r'^admin/locality-autocomplete/$', LocalityAutocomplete.as_view(),
            name='locality-autocomplete',),
    url(r'^admin/srs-autocomplete/$', SpatialRefSysAutocomplete.as_view(),
            name='srs-autocomplete',),
    url(r'^admin/ontology-collection-autocomplete/$',
            OntologyCollectionAutocomplete.as_view(),
                name='ontology-collection-autocomplete',),
    url(r'^admin/ontology-term-autocomplete/$', OntologyTermAutocomplete.as_view(),
            name='ontology-term-autocomplete',),
    url(r'^admin/journal-autocomplete/$', JournalAutocomplete.as_view(create_field='journal_name'),
            name='journal-autocomplete',),
    url(r'^admin/book-autocomplete/$', BookAutocomplete.as_view(),
            name='book-autocomplete',),
    url(r'^admin/reference-autocomplete/$', ReferenceAutocomplete.as_view(),
            name='reference-autocomplete',),
    url(r'^admin/specimen-autocomplete/$', SpecimenAutocomplete.as_view(),
            name='specimen-autocomplete',),
    url(r'^admin/foodrecord-autocomplete/$', FoodRecordAutocomplete.as_view(),
            name='foodrecord-autocomplete',),
    url(r'^admin/person-autocomplete/$', PersonAutocomplete.as_view(create_field='first_name|last_name'),
            name='person-autocomplete',),
]

urlpatterns = [
    url(r'^$', SiteView.as_view(), name='index'),
    url(r'^foodrecord/([0-9]+)/$', FoodRecordView.as_view(), name='foodrecord'),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^data/foodrecords/$', FoodRecordAPI.as_view(), name='foodrecords'),
    url(r'^data/taxonomy/$', TaxonomyAPI.as_view(), name='taxonomy'),
    
] + autocompletes

