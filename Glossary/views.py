from django.shortcuts import render
from django.db.models import Q
from dal import autocomplete
from .models import *


class OntologyCollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return OntologyCollection.objects.none()
        
        qs = OntologyCollection.objects.all()
        
        if self.q:
            qs = qs.filter(Q(**{'collection_name__istartswith': self.q}))
                
        return qs


class OntologyTermAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return OntologyTerm.objects.none()
        
        qs = OntologyTerm.objects.none()
        collection_id = self.forwarded.get('collection', None)
        
        if collection_id:
            qs = OntologyTerm.objects.filter(collection=collection_id)
        
        if self.q:
            qs = qs.filter(Q(**{'term__istartswith': self.q}))
                
        return qs