from django.shortcuts import render
from django.db.models import Q
from dal import autocomplete
from .models import *


class MuseumAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Museum.objects.none()

        if self.q:  
            return Museum.objects.filter(Q(**{'museum_name__istartswith': self.q}) | Q(**{'museum_abbr__istartswith': self.q}))
                    
        return Museum.objects.none()


class MuseumCollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return MuseumCollection.objects.none()
        
        qs = MuseumCollection.objects.all()
        museum = self.forwarded.get('museum', None)
        if museum:
            qs = qs.filter(museum_id=museum)
        if self.q:  
            return qs.filter(Q(**{'collection_name__istartswith': self.q}))
                    
        return qs



class VoucherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Voucher.objects.none()
        
        qs = Voucher.objects.all()
        if self.q:
            q = self.q.split()
            qs = qs.filter(Q(**{'museum__museum_abbr__istartswith': q[0]}))
            try:
                qs = qs.filter(
                    (Q(**{'catalog_number__istartswith': q[1]}) |
                        Q(**{'field_number__istartswith': q[1]})))
            except IndexError:
                pass
                                
        return qs


class SpecimenAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Specimen.objects.none()

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
            setvouchers = SpecimenVoucher.objects.filter(c2)

            c3 = Q(**{'id__istartswith': self.q})
            c3 |= Q(**{'taxon__scientific_name__istartswith': self.q})
            c3 |= Q(**{'id__in': setvouchers.values_list('specimen',
                                                         flat=True)})
            return Specimen.objects.filter(c3).order_by('-id')
                    
        return Specimen.objects.none()
