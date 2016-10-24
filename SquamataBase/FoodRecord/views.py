from django.shortcuts import render
from django.db.models import Q, F
from dal import autocomplete
from SquamataBase.Specimen.models import Voucher
from .models import IndividualSet, IndividualSetVoucher, FoodRecord


class IndividualAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return IndividualSet.objects.none()

        if self.q:
            m = self.q.split()
            if len(m):
                c1 = Q(**{'museum__museum_abbr__istartswith': m[0]})
                if len(m) > 1:
                    c1 &= (Q(**{'catalog_number__istartswith': m[1]}) 
                            | Q(**{'field_number__istartswith': m[1]}))
            else:
                c1 = Q(**{'museum__museum_abbr__istartswith': self.q})
                               
            vouchers = Voucher.objects.filter(c1)
            c2 = Q(**{'voucher__in': vouchers.values_list('id', flat=True)})
            setvouchers = IndividualSetVoucher.objects.filter(c2)

            c3 = Q(**{'id__istartswith': self.q})
            c3 |= Q(**{'taxon__scientific_name__istartswith': self.q})
            c3 |= Q(**{'id__in': setvouchers.values_list('individual_set',
                                                         flat=True)})
            return IndividualSet.objects.filter(c3).order_by('-id')
                    
        return IndividualSet.objects.none()


class FoodRecordAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return FoodRecord.objects.none()

        if self.q:
            c = Q(**{'predator__taxon__scientific_name__istartswith': self.q})
            c |= Q(**{'prey__taxon__scientific_name__istartswith': self.q})
            return FoodRecord.objects.filter(c).order_by('-id')
                    
        return FoodRecord.objects.none()
