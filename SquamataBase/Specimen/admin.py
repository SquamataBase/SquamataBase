from django.contrib import admin
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