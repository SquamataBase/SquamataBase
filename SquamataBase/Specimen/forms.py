from django import forms
from dal import autocomplete
from django.core.exceptions import ValidationError             
from .models import *

class VoucherForm(forms.ModelForm):
    
    class Meta:
        model = Voucher
        fields = ('__all__')
        widgets = {
            'museum': autocomplete.ModelSelect2(
                url = 'museum-autocomplete',
                attrs = {
                    'data-minimum-input-length': 2,
                },
            ),
            'museum_collection': autocomplete.ModelSelect2(
                url = 'museum-collection-autocomplete',
                attrs = {
                    'data-minimum-input-length': 0,
                },
                forward = ['museum']
            ),
        }
        
    def clean(self):
        import re
        
        cleaned_data = super(VoucherForm, self).clean()
        
        museum = cleaned_data['museum']
        catalog_no = cleaned_data['catalog_number']
        field_no = cleaned_data['field_number']
        
        p = re.compile('.?{}.?'.format(museum.museum_abbr))
        
        if catalog_no and len(re.findall(p, catalog_no)):
            raise ValidationError('Museum abbreviation may not be present in the catalog number')
        
        if field_no and len(re.findall(p, field_no)):
            raise ValidationError('Museum abbreviation may not be present in the field number')


class SpecimenForm(forms.ModelForm):
    
    TAXON_CONTEXT = (
        ('life',        '---------'),
        ('amphibians',  'Amphibians'),
        ('birds',       'Birds'),
        ('fish',        'Fishes'),
        ('mammals',     'Mammals'),
        ('reptiles',    'Reptiles'),
        ('annelids',    'Annelids'),
        ('arthropods',  'Arthropods'),
        ('mollusks',    'Mollusks'),
        ('onychophora', 'Onychophorans'),
        ('animals',     'Animals'),
        ('fungi',       'Fungi'),
        ('plants',      'Plants'),
    )
    
    taxon_lookup_context = forms.ChoiceField(choices=TAXON_CONTEXT, required=False, initial='life')
    
    class Meta:
        model = Specimen
        fields = ('__all__')
        widgets = {
            'taxon': autocomplete.ModelSelect2(
                url = 'taxon-autocomplete',
                attrs = {
                    'data-placeholder': '',
                    'data-minimum-input-length': 2,
                },
                forward = ['taxon_lookup_context'],
            ),
        }
        
        
class SpecimenVoucherForm(forms.ModelForm):
    class Meta:
        model = SpecimenVoucher
        fields = ('__all__')
        widgets = {
            'voucher': autocomplete.ModelSelect2(
                url = 'voucher-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for vouchers . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        }


class SpecimenIntersectionForm(forms.ModelForm):
    class Meta:
        model = SpecimenIntersection
        fields = ('__all__')
        widgets = {
            'intersects_with': autocomplete.ModelSelect2(
                url = 'specimen-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for specimens . . .',
                    'data-minimum-input-length': 1,
                },
            ),
        }
            