from django.contrib import admin
from .models import *

@admin.register(Taxon)
class TaxonAdmin(admin.ModelAdmin):
    list_display = ('col_taxon_id', 'scientific_name', 'taxon_status')
    list_per_page = 30
    readonly_fields = (
        'col_taxon_id', 'col_identifier', 'scientific_name', 'taxon_status',
        'taxon_rank', 'accepted_name', 'parent_name', 'author')
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
   