from django.contrib import admin
import nested_admin
from SquamataBase.Glossary.models import *
from SquamataBase.FoodRecord.models import *
from SquamataBase.FoodRecord.forms import *
from SquamataBase.Bibliography.models import *
from SquamataBase.Bibliography.forms import *
from .models import *


class IndividualSetMeasurementNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = IndividualSetMeasurement
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
        return super(IndividualSetMeasurementNestedInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
class IndividualSetVoucherNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = IndividualSetVoucher
    form = IndividualSetVoucherForm
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
        
 
class IndividualSetIntersectionNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = IndividualSetIntersection
    form = IndividualSetIntersectionForm
    fk_name = 'individual_set'
    extra = 1
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra


class IndividualSetNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = IndividualSet
    form = IndividualSetForm
    extra = 2
    max_num = 2
    can_delete = False
    verbose_name = 'specimen'
    template = 'admin/Workbench/extra/inline_specimen.html'

    inlines = [IndividualSetMeasurementNestedInlineAdmin,
               IndividualSetVoucherNestedInlineAdmin,
               IndividualSetIntersectionNestedInlineAdmin]

    fieldsets = (
        ('Taxon',  {
            'fields': (
                'taxon_context', 'taxon',
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
        
    class Media:
        js = ('FoodRecord/js/taxon_placeholder.js',
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
        return super(IndividualSetNestedInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class FoodRecordNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = FoodRecord
    form = FoodRecordForm
    exclude = ('predator', 'prey', 'ref_type', 'ref')
    extra = 1
    max_num = 1
    can_delete = False
    verbose_name = 'foodrecord'
    template = 'admin/stacked_inline_noheader.html'

    fieldsets = (
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
    
    class Media:
        js = ('FoodRecord/js/reference_placeholder.js', 'FoodRecord/js/format_time.js')
    
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
        return super(FoodRecordNestedInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class JournalArticleNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = JournalArticle
    form = JournalArticleForm
    can_delete = False
    template = 'admin/stacked_inline_noheader.html'

class BookNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = Book
    can_delete = False
    template = 'admin/stacked_inline_noheader.html'
        
class BookChapterNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = BookChapter
    form = BookChapterForm
    can_delete = False
    template = 'admin/stacked_inline_noheader.html'

class ContributionNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = Contribution
    form = ContributionForm
    extra = 1
    show_change_link = True
    
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person_role':
            try:
                cid = OntologyCollection.objects.get(collection_name='person_roles').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(ContributionNestedInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs) 


class RefNestedInlineAdmin(nested_admin.NestedStackedInline):
    model = Ref
    verbose_name = 'datasource'
    extra = 1
    max_num = 1
    can_delete = False
    template = 'admin/stacked_inline_noheader.html'

    inlines = (
        JournalArticleNestedInlineAdmin,
        BookNestedInlineAdmin,
        BookChapterNestedInlineAdmin,
        ContributionNestedInlineAdmin,
    )
        
    class Media:
        js = ('admin/Workbench/js/dynamic_ref_form.js',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ref_type':
            try:
                cid = OntologyCollection.objects.get(collection_name='publication_types').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(RefNestedInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(FoodRecordWorkbench)
class FoodRecordWorkbenchAdmin(nested_admin.NestedModelAdmin):
    change_form_template = 'admin/Workbench/extra/wbfoodrecord_changeform.html'
    inlines = [IndividualSetNestedInlineAdmin, FoodRecordNestedInlineAdmin, RefNestedInlineAdmin]

    class Media:
        js = ('admin/js/responsive_tabs.js',)
        css = {
            'all': ('admin/css/admin_tabs.css',),
        }

    def save_related(self, request, form, formsets, change):
        """
        We need to override save_related so that we can attach the
        predator and prey specimens to their appropriate foreign key
        fields in the food record before it is saved.
        """
        specimens = []
        data_source = []
        for formset in formsets:
            if formset.prefix == 'individualset_set':
                specimens.extend(formset.save())
            elif formset.prefix == 'ref_set':
                data_source.extend(formset.save())
            elif formset.prefix == 'foodrecord_set':
                for form in formset.forms:
                    setattr(form.instance, 'predator', specimens[0])
                    setattr(form.instance, 'prey', specimens[1])
                    setattr(form.instance, 'ref', data_source[0])
        super(FoodRecordWorkbenchAdmin, self).save_related(request, form, formsets, change)


