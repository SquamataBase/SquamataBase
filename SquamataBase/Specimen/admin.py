from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .forms import *


class MuseumCollectionInlineAdmin(admin.TabularInline):
    model = MuseumCollection
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
        
        
@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ('id', 'museum_abbr', 'museum_name',)
    inlines = (MuseumCollectionInlineAdmin,)
    search_fields = ('museum_name', 'museum_abbr',)


@admin.register(MuseumCollection)
class MuseumCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'museum', 'collection_name',)

    
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    form = VoucherForm
    list_display = ('id', 'museum', 'catalog_number', 'field_number',)
    search_fields = ('museum__museum_name', 'museum__museum_abbr', 'catalog_number', 'field_number',)


class SpecimenMeasurementInlineAdmin(admin.TabularInline):
    model = SpecimenMeasurement
    extra = 1
    show_change_link = True
    fieldsets = (
        ('Measurement', {
            'fields': ('measurement_type', 'measurement_unit'),
        }),
        ('Value', {
            'fields': ('measurement_value', 'verbatim_value'),
        }),
    )
    
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'measurement_unit':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_units').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'measurement_type':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_types').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(SpecimenMeasurementInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
class SpecimenVoucherInlineAdmin(admin.TabularInline):
    model = SpecimenVoucher
    form = SpecimenVoucherForm
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
        
 
class SpecimenIntersectionInlineAdmin(admin.TabularInline):
    model = SpecimenIntersection
    form = SpecimenIntersectionForm
    fk_name = 'specimen'
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
 
        
@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    form = SpecimenForm
    change_form_template = 'admin/Specimen/extra/specimen_changeform.html'
    fieldsets = (
        ('Taxon',  {
            'fields': (
                'taxon_lookup_context', 'taxon',
                ('verbatim_name','ambiguous'),
                'lifestage', 'sex', 'component_part'),
        }),
        ('Amount',  {
            'fields': (
                'count',
                ('mass', 'mass_unit'),
                ('volume','volume_unit'),),
        }),
    )
    
    inlines = (
        SpecimenVoucherInlineAdmin,
        SpecimenMeasurementInlineAdmin,
        SpecimenIntersectionInlineAdmin,
    )
        
    list_display = ('id', 'taxon', 'get_vouchers')
    
    class Media:
        js = ('FoodRecord/js/taxon_placeholder.js',
              'admin/js/responsive_tabs.js',)
        css = {
            'all': ('admin/css/admin_tabs.css',),
        }
    
    def get_vouchers(self, obj):
        return ':'.join((str(v) for v in SpecimenVoucher.objects.filter(specimen=obj.id)))
    get_vouchers.short_description = 'Voucher'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'mass_unit' or db_field.name == 'volume_unit':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_units').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'lifestage':
            try:
                cid = OntologyCollection.objects.get(collection_name='life_stages').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'sex':
            try:
                cid = OntologyCollection.objects.get(collection_name='sexes').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'component_part':
            try:
                cid = OntologyCollection.objects.get(collection_name='organism_components').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(SpecimenAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
