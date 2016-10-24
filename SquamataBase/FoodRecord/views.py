from django.shortcuts import render
from django.db.models import Q, F
from dal import autocomplete
from .models import FoodRecord


class FoodRecordAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return FoodRecord.objects.none()

        if self.q:
            c = Q(**{'predator__taxon__scientific_name__istartswith': self.q})
            c |= Q(**{'prey__taxon__scientific_name__istartswith': self.q})
            return FoodRecord.objects.filter(c).order_by('-id')
                    
        return FoodRecord.objects.none()
