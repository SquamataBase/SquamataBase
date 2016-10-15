from django.contrib import admin
from .models import *
from .forms import *


class OntologyHasRelationshipInlineAdmin(admin.TabularInline):
    model = OntologyHasRelationship
    extra = 1
    fk_name = 'ontology_from'
    show_change_link = True
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra


@admin.register(OntologyTerm)
class OntologyTermAdmin(admin.ModelAdmin):
    form = OntologyTermForm
    inlines = (OntologyHasRelationshipInlineAdmin,)
    list_display = ('id', 'get_term_name', 'parent', 'collection',)
    list_filter = ('collection',)
    list_per_page = 30

    def get_term_name(self, obj):
        return str(obj)
    get_term_name.short_description = 'Term'

@admin.register(OntologyCollection)
class OntologyCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_collection_name')
    
    def get_collection_name(self, obj):
        return str(obj)
    get_collection_name.short_description = 'Collection name'

@admin.register(OntologyRelationship)
class OntologyRelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'relationship_name')