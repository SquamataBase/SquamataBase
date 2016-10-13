from django import forms
from dal import autocomplete
from Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .widgets import *

class IndividualSetForm(forms.ModelForm):
    
    TAXON_CONTEXT = (
        ('life',        'All life'),
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
    
    taxon_context = forms.ChoiceField(choices=TAXON_CONTEXT, required=False, initial='reptiles')
    
    class Meta:
        model = IndividualSet
        fields = ('__all__')
        widgets = {
            'taxon': autocomplete.ModelSelect2(
                url = 'taxon-autocomplete',
                attrs = {
                    'data-placeholder': '',
                    'data-minimum-input-length': 2,
                },
                forward = ['taxon_context'],
            ),
        }
        
        
class IndividualSetVoucherForm(forms.ModelForm):
    class Meta:
        model = IndividualSetVoucher
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


class IndividualSetIntersectionForm(forms.ModelForm):
    class Meta:
        model = IndividualSetIntersection
        fields = ('__all__')
        widgets = {
            'intersects_with': autocomplete.ModelSelect2(
                url = 'individual-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for individuals . . .',
                    'data-minimum-input-length': 1,
                },
            ),
        }


class DataSetForm(forms.ModelForm):
    
    try:
        cid = OntologyCollection.objects.get(collection_name='publication_types')
        res = OntologyTerm.objects.filter(collection=cid)
    except:
        res = ()

    REFTYPE = ((i, i) for i in res)

    ref_type = forms.ChoiceField(choices=REFTYPE, required=False)
    start_date = MyDateField(required=False)
    end_date = MyDateField(required=False)
    class Meta:
        model = DataSet
        fields = ('__all__')
        widgets = {
            'ref': autocomplete.ModelSelect2(
                url = 'reference-autocomplete',
                attrs = {
                    'data-placeholder': '',
                    'data-minimum-input-length': 2,
                },
                forward = ['ref_type'],
            ),
        }


class DataSetLocalityForm(forms.ModelForm):
    class Meta:
        model = DataSetLocality
        fields = ('__all__')
        widgets = {
            'locality': autocomplete.ModelSelect2(
                url = 'locality-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for localities . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        
        }
        
        
class DataSetFoodRecordForm(forms.ModelForm):
    class Meta:
        model = DataSetFoodRecord
        fields = ('__all__')
        widgets = {
            'foodrecord': autocomplete.ModelSelect2(
                url = 'foodrecord-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for food records . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        }        
        
        
class FoodRecordForm(forms.ModelForm):
    
    try:
        cid = OntologyCollection.objects.get(collection_name='publication_types')
        res = OntologyTerm.objects.filter(collection=cid)
    except:
        res = ()

    REFTYPE = ((i, i) for i in res)
    
    ref_type = forms.ChoiceField(choices=REFTYPE, required=False)
    event_date = MyDateField(required=False)
    start_time = MyTimeField(required=False)
    end_time = MyTimeField(required=False)
    
    alimentary_pos = forms.ChoiceField(widget=forms.RadioSelect, choices=(('stomach', 'Stomach'), ('intestine', 'Intestine')),
            required=False)

    class Meta:
        model = FoodRecord
        fields = ('__all__')
        widgets = {
            'ref': autocomplete.ModelSelect2(
                url = 'reference-autocomplete',
                attrs = {
                    'data-placeholder': '',
                    'data-minimum-input-length': 2,
                },
                forward = ['ref_type'],
            ),
            'predator': autocomplete.ModelSelect2(
                url = 'individual-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for individuals . . .',
                    'data-minimum-input-length': 1,
                },
            ),
            'prey': autocomplete.ModelSelect2(
                url = 'individual-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for individuals . . .',
                    'data-minimum-input-length': 1,
                },
            ),
            'locality': autocomplete.ModelSelect2(
                url = 'locality-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for localities . . .',
                    'data-minimum-input-length': 2,
                },
            ),
        }
        