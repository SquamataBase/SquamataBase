from django import forms
from dal import autocomplete
from .models import *
             
class OntologyTermForm(forms.ModelForm):
    
    class Meta:
        model = OntologyTerm
        fields = ('__all__') 
        widgets = {
            'collection': autocomplete.ModelSelect2(
                url = 'ontology-collection-autocomplete',
                attrs = {
                    'data-minimum-input-length': 0,
                },
            ),
            'parent': autocomplete.ModelSelect2(
                url = 'ontology-term-autocomplete',
                attrs = {
                    'data-minimum-input-length': 0,
                },
                forward = ['collection']
            ),
        }
        