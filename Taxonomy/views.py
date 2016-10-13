from django.shortcuts import render
from django.db.models import Q
from dal import autocomplete
from .models import *


class TaxonAutocomplete(autocomplete.Select2QuerySetView):
    
    TAXON_CONTEXT_MODELS = {
        'life': Taxon,
        'amphibians': TaxonAmphibian,
        'birds': TaxonBird,
        'fish': TaxonFish,
        'mammals': TaxonMammal,
        'reptiles': TaxonReptile,
        'annelids': TaxonAnnelid,
        'arthropods': TaxonArthropod,
        'mollusks': TaxonMollusk,
        'onychophora': TaxonOnychophoran,
        'animals': TaxonAnimal,
        'fungi': TaxonFungus,
        'plants': TaxonPlant,
    }
    
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Taxon.objects.none()

        if self.q:
            taxon_context = self.forwarded.get('taxon_context', None)
            m = Taxon
            q = self.q.lower().capitalize()  # format the query term so that it matches storage in database.
            if taxon_context:
                m = self.TAXON_CONTEXT_MODELS[taxon_context]
            c1 = Q(**{'scientific_name__startswith': q})  # no need to use case-insensitive query because we know formatting of query matches data
            c1 &= Q(**{'taxon_status__exact': 'synonym'})
            resolved_taxa = m.objects.filter(c1).select_related('accepted_name')
            c2 = Q(**{'scientific_name__startswith': q})
            c2 &= ~Q(**{'taxon_status__exact': 'synonym'})
            c2 |= Q(**{'col_taxon_id__in': resolved_taxa.values_list('accepted_name_id', flat=True)})
            
            return m.objects.defer('col_identifier', 'taxon_rank', 'parent_name', 'author').filter(c2)
                    
        return Taxon.objects.none()
