from django.contrib.gis import admin
from django.core.exceptions import ObjectDoesNotExist
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .forms import *


@admin.register(AdmUnit)
class AdmUnitAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('geoname_id', 'unit_name_ascii', 'parent')
    list_filter = ('admin_level',)
    readonly_fields = ('geoname_id', 'admin_level', 'unit_name_ascii', 'unit_name', 'parent')
    search_fields = ('unit_name_ascii',)

    def has_add_permission(self, obj):
        return False

@admin.register(AdmUnitBoundary)
class AdmUnitBoundaryAdmin(admin.OSMGeoAdmin):
    list_per_page = 10
    list_display = ('get_id', 'get_unit')
    readonly_fields = ('geoname_id',)
    search_fields = ('geoname_id__unit_name_ascii',)
    modifiable = False
    
    def get_id(self, obj):
        return obj.geoname_id.geoname_id
    get_id.short_description = 'Geoname ID'
    
    def get_unit(self, obj):
        return obj.geoname_id.unit_name_ascii
    get_unit.short_description = 'Administrative unit'
    
    def has_add_permission(self, obj):
        return False
    
    
@admin.register(NamedPlace)
class NamedPlaceAdmin(admin.OSMGeoAdmin):
    form = NamedPlaceForm

    fieldsets = (
        ('Locality', {
            'fields': ('adm0', 'adm1', 'adm2', 'place_name', 'parent_admin'),
        }),
        ('Coordinates', {
            'fields': (
                'verbatim_coordinates', 'verbatim_srid', 'coord_format', 'utm_zone'
            )
        }),
        ('Elevation', {
            'fields': (
                'elevation_start',
                ('elevation_end', 'elevation_unit'),),
        }),
        ('Remarks', {
            'fields': ('remark',),
        }),
    )
    
    list_display = ('id', 'place_name')
    #list_filter = ('adm0',)
    search_fields = ('place_name',)

    class Media:
        js = ('Geography/js/dynamic_coord_form.js',
                'Geography/js/admu_autocomplete.js',)
        css = {
            'all': ('Geography/css/coordinates.css',)
        }
        
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('point', None):
            obj.point = form.cleaned_data['point']
        obj.save()
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'elevation_unit':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_units').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(NamedPlaceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(Locality)
class LocalityAdmin(admin.OSMGeoAdmin):
    form = LocalityForm

    fieldsets = (
        ('Locality', {
            'fields': ('adm0', 'adm1', 'adm2', 'named_place', 'dirtmap', 'parent_admin'),
        }),
        ('Coordinates', {
            'fields': (
                'verbatim_coordinates', 'verbatim_srid', 'coord_format', 'utm_zone'),
        }),
        ('Elevation', {
            'fields': (
                'elevation_start',
                ('elevation_end', 'elevation_unit'), 'verbatim_elevation'),
        }),
        ('Remarks', {
            'fields': ('remark',),
        }),
    )

    list_display = ('id', 'verbatim_coordinates', 'named_place', 'dirtmap', 'adm2', 'adm1', 'adm0')
    
    class Media:
        js = ('Geography/js/dynamic_coord_form.js',
                'Geography/js/admu_autocomplete.js',)
        css = {
            'all': ('Geography/css/coordinates.css',)
        }

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('point', None):
            obj.point = form.cleaned_data['point']
        obj.save()
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'elevation_unit':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_units').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(LocalityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        