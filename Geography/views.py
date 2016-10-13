from django.shortcuts import render
from django.db.models import Q
from dal import autocomplete
from .models import *


class AdmUnitAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return AdmUnit.objects.none()
        
        qs = AdmUnit.objects.all()
        parent = self.forwarded.get('parent_admin', None)
        if parent:
            qs = qs.filter(parent=parent)
        else:
            qs = qs.filter(parent=None)
        if self.q:
            return qs.filter(Q(**{'unit_name_ascii__istartswith': self.q}))
                    
        return AdmUnit.objects.none()
        

class NamedPlaceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return NamedPlace.objects.none()

        if self.q:
            country = self.forwarded.get('adm0', None)
            state = self.forwarded.get('adm1', None)
            county = self.forwarded.get('adm2', None)
            qs = NamedPlace.objects.defer('point').all()
            if country:
                qs = qs.filter(Q(adm0_id=country))
            if state:
                qs = qs.filter(Q(adm1_id=state))
            if county:
                qs = qs.filter(Q(adm2_id=county))
            qs = qs.filter(Q(**{'place_name__unaccent__istartswith': self.q}))
            return qs
                    
        return NamedPlace.objects.none()


class LocalityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Locality.objects.none()

        if self.q:
            qs = Locality.objects.defer('point').all()
            c  = Q(**{'named_place__place_name__unaccent__istartswith': self.q})
            c |= Q(**{'dirtmap__istartswith': self.q})
            c |= Q(**{'verbatim_coordinates__startswith': self.q})
            c |= Q(**{'adm0__unit_name_ascii__istartswith': self.q})
            c |= Q(**{'adm1__unit_name_ascii__istartswith': self.q})
            c |= Q(**{'adm2__unit_name_ascii__istartswith': self.q})
            return qs.filter(c)
                    
        return Locality.objects.none()


class SpatialRefSysAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return SpatialRefSys.objects.none()
        
        if self.q:
            qs = SpatialRefSys.objects.all()
            format = self.forwarded.get('coord_format', None)
            if format == 'UTM':
                f = '+proj=utm +zone={}'.format(self.forwarded.get('utm_zone', None))
                q = 'PROJCS["{}'.format(self.q)                
            else:
                f = '+proj=longlat'
                q = 'GEOGCS["{}'.format(self.q)
            c  = Q(**{'proj4text__istartswith': f})
            c &= Q(**{'srtext__istartswith': q})
            return qs.filter(c)
            
        return SpatialRefSys.objects.none()
