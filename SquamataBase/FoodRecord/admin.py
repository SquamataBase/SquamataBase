from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
from SquamataBase.Geography.models import Locality
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .forms import *


class DataSetMethodInlineAdmin(admin.TabularInline):
    model = DataSetMethod
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'basis':
            try:
                cid = OntologyCollection.objects.get(collection_name='observation_methods').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(DataSetMethodInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DataSetLocalityInlineAdmin(admin.TabularInline):
    model = DataSetLocality
    form = DataSetLocalityForm
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
        

class DataSetFoodRecordInlineAdmin(admin.TabularInline):
    model = DataSetFoodRecord
    form = DataSetFoodRecordForm
    extra = 1;
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra

       
@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    form = DataSetForm
    change_form_template = 'admin/FoodRecord/extra/dataset_changeform.html'
    fieldsets = (
        ('Data Source', {
            'fields': ('ref',),
        }),
        ('Predator Set', {
            'fields': ('n_predators_examined', 'n_predators_ate'),
        }),
        ('Prey Set', {
            'fields': (
                'n_prey_eaten',
                ('mass_prey_eaten', 'mass_unit'),
                ('volume_prey_eaten', 'volume_unit'),),
        }),
        ('Study Dates', {
            'fields': ('start_date', 'end_date'),
        }),
    )

    inlines = (
        DataSetMethodInlineAdmin,
        DataSetLocalityInlineAdmin,
        DataSetFoodRecordInlineAdmin,
    )
    
    list_display = ('id', 'ref')

    class Media:
        js = ('FoodRecord/js/reference_placeholder.js',
              'admin/js/responsive_tabs.js',)
        css = {
            'all': ('admin/css/admin_tabs.css',),
        }
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'mass_unit' or db_field.name == 'volume_unit':
            try:
                cid = OntologyCollection.objects.get(collection_name='measurement_units').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(DataSetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def response_post_save_change(self, request, obj):
        # we only add datasets via the Workbench action, so redirect back
        # to that index page
        return HttpResponseRedirect('/admin/Workbench/foodrecordworkbench/')

  
@admin.register(FoodRecord)
class FoodRecordAdmin(admin.ModelAdmin):
    form = FoodRecordForm
    fieldsets = (
        ('Data Source', {
            'fields': ('ref',),
        }),
        ('Specimens', {
            'fields': ('predator', 'prey',),
        }),
        ('Context', {
            'fields': (
                ('basis', 'alimentary_pos'), 'context', 'conditions', 'outcome',
                'ingestion_direction', 'prey_capture_mode', 'prey_handle_mode'),
        }),
        ('Locality', {
            'fields': (
                'locality', 'event_date', 'start_time', 'end_time',
                'habitat', 'verbatim_habitat'),
        }),
        ('Remarks', {
            'fields': ('remark',),
        }),   
    )
    
    list_display = ('id', 'get_predator', 'get_prey',)
    search_fields = ('predator__taxon__scientific_name', 'prey__taxon__scientific_name',)
    actions = ['clone', 'duplicate']
    
    class Media:
        js = ('FoodRecord/js/reference_placeholder.js', 'FoodRecord/js/format_time.js')
        
    def get_predator(self, obj):
        return format_html(
            '<a href="/admin/Specimen/specimen/{}/change/">{}</a>',
            obj.predator.id, 
            obj.predator.taxon.scientific_name
        )
    get_predator.short_description = 'Predator'
        
    def get_prey(self, obj):
        return format_html(
            '<a href="/admin/Specimen/specimen/{}/change/">{}</a>',
             obj.prey.id, 
             obj.prey.taxon.scientific_name
        )
    get_prey.short_description = 'Prey'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'basis':
            try:
                cid = OntologyCollection.objects.get(collection_name='observation_methods').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'context':
            try:
                cid = OntologyCollection.objects.get(collection_name='observation_contexts').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'conditions':
            try:
                cid = OntologyCollection.objects.get(collection_name='predation_contexts').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'outcome':
            try:
                cid = OntologyCollection.objects.get(collection_name='predation_outcomes').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'ingestion_direction':
            try:
                cid = OntologyCollection.objects.get(collection_name='ingestion_orientations').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'habitat':
            try:
                cid = OntologyCollection.objects.get(collection_name='habitats').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'prey_capture_mode':
            try:
                cid = OntologyCollection.objects.get(collection_name='prey_capture_modes').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        if db_field.name == 'prey_handle_mode':
            try:
                cid = OntologyCollection.objects.get(collection_name='prey_handling_modes').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(FoodRecordAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def clone(self, request, queryset):
        """Create a new food by copying an existing one.
            
            This method creates new instances of predator and
            prey individuals.
        """
        message=[{'added': {}}]
        for m in queryset:
            pred = m.predator  # clone the predator
            prey = m.prey  # clone the prey
            pred.id = None
            prey.id = None
            pred.save()
            self.log_addition(request, pred, message)
            prey.save()
            self.log_addition(request, prey, message)
            m.id = None  # clone the food record with new predator and prey
            m.predator = pred
            m.prey = prey
            m.save()
            self.log_addition(request, m, message)
    clone.short_description = 'Clone selected food records'

    def duplicate(self, request, queryset):
        """Create a new food by copying an existing one.
            
            This method creates new instances of
            prey individuals but not of predator
            individuals.
        """
        message=[{'added': {}}]
        for m in queryset:
            prey = m.prey  # clone the prey
            prey.id = None
            prey.save()
            self.log_addition(request, prey, message)
            m.id = None  # clone the food record with new prey
            m.prey = prey
            m.save()
            self.log_addition(request, m, message)
    duplicate.short_description = 'Duplicate selected food records'
            