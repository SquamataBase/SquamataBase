from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import ugettext as _
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
        qs = NamedPlace.objects.defer('point').all()
        country = self.forwarded.get('adm0', None)
        state = self.forwarded.get('adm1', None)
        county = self.forwarded.get('adm2', None)
        
        if country:
            qs = qs.filter(Q(adm0_id=country))
        if state:
            qs = qs.filter(Q(adm1_id=state))
        if county:
            qs = qs.filter(Q(adm2_id=county))
        if self.q:
            qs = qs.filter(Q(**{'place_name__unaccent__istartswith': self.q}))             
        return qs

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        country = self.forwarded.get('adm0', None)
        state = self.forwarded.get('adm1', None)
        county = self.forwarded.get('adm2', None)
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True
        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def create_object(self, text):
        """Create a new place name."""
        country = self.forwarded.get('adm0', None)
        state = self.forwarded.get('adm1', None)
        county = self.forwarded.get('adm2', None)
        place = text.strip()
        return self.get_queryset().create(**{
            'adm0_id': int(country) if country else None,
            'adm1_id': int(state) if state else None,
            'adm2_id': int(county) if county else None,
            'place_name': place,
            })


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
