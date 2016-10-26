from django import forms
from dal import autocomplete
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .widgets import *


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
                url = 'specimen-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for specimens . . .',
                    'data-minimum-input-length': 1,
                },
            ),
            'prey': autocomplete.ModelSelect2(
                url = 'specimen-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for specimens . . .',
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
            'basis': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'context': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'conditions': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'outcome': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'ingestion_direction': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'prey_capture_mode': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'prey_handle_mode': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
            'habitat': autocomplete.ModelSelect2(
                attrs = {
                    'data-placeholder': '',
                }
            ),
        }


        