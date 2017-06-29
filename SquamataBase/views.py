import json
from functools import lru_cache
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView
from django.http import HttpResponse
from django.db.models import Q
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SquamataBase.Specimen.models import *
from SquamataBase.FoodRecord.models import *
from SquamataBase.Taxonomy.models import Taxon


class SiteView(TemplateView):
    """View for the non-admin website."""
    
    template_name = "site/index.html"

    def dispatch(self, request, *args, **kwargs):
        self.q = request.GET.get('taxon', '').lower().capitalize()
        self.taxonrole = request.GET.get('taxonrole', '')
        kwargs['taxon'] = self.q
        kwargs['taxonrole'] = self.taxonrole
        if self.q:
            # logic to query food records and add them to the request context data
            #qs = self.get_queryset(self.q, self.taxonrole)
            qs, nres, coordinates = eval_qs(self.q, self.taxonrole)
            paginator = Paginator(qs, 10)
            page = request.GET.get('page')
            try:
                foodrecords = paginator.page(page)
            except PageNotAnInteger:
                foodrecords = paginator.page(1)
            except EmptyPage:
                foodrecords = paginator.page(paginator.num_pages)
            kwargs['foodrecords'] = foodrecords
            kwargs['n_results'] = nres
            kwargs['coordinates'] = coordinates
            if page:
                kwargs['page'] = page
        return super(SiteView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get_queryset(q, context):
        all_taxa = [d.pk for taxon in Taxon.objects.filter(scientific_name=q) for d in taxon.descendants]
        if context == 'pred':
            query = Q(**{'predator__taxon__pk__in': all_taxa})
        elif context == 'prey':
            query = Q(**{'prey__taxon__pk__in': all_taxa})
        elif context == 'predprey':
            query = Q(**{'predator__taxon__pk__in': all_taxa}) | Q(**{'prey__taxon__pk__in': all_taxa})
        else:
            return FoodRecord.objects.none()
        return FoodRecord.objects.filter(query)


@lru_cache(maxsize=32)
def eval_qs(q, context):
    qs = SiteView.get_queryset(q, context)
    nres = 0
    coordinates = []
    for obj in qs:
        nres += 1
        if obj.locality is not None:
            if obj.locality.point is not None:
                coordinates.append([obj.locality.point.y, obj.locality.point.x, str(obj.predator.taxon), str(obj.prey.taxon)])  # leaflet expects lat-long format
            elif obj.locality.named_place is not None:
                if obj.locality.named_place.point is not None:
                    coordinates.append([obj.locality.named_place.point.y, obj.locality.named_place.point.x, str(obj.predator.taxon), str(obj.prey.taxon)])
    return (qs, nres, coordinates)



class BaseAPIView(BaseListView):
    """Base view for web API."""

    http_methods_names = ['get']  # only get allowed
    model_fields = []
    return_fields = {}


class TaxonomyAPI(BaseAPIView):
    """API view to query taxonomy."""

    def dispatch(self, request, *args, **kwargs):
        self.taxon_name = [name.lower().capitalize() for name in json.loads(request.GET.get('taxon_name', '[]'))]
        self.taxon_id = json.loads(request.GET.get('taxon_id', '[]'))
        return super(BaseAPIView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.taxon_id and not self.taxon_name:
            return Taxon.objects.filter(pk__in=self.taxon_id)
        elif self.taxon_name and not self.taxon_id:
            return Taxon.objects.filter(scientific_name__in=self.taxon_name)
        elif self.taxon_name and self.taxon_id:
            return Taxon.objects.filter(scientific_name__in=self.taxon_name).filter(pk__in=self.taxon_id)
        else:
            return []

    def get_results(self, context):
        return [
            {
                'id': result.col_taxon_id,
                'scientific_name': result.scientific_name,
                'taxon_status': result.taxon_status,
                'hierarchy': [
                    {
                        'id': ancestor.col_taxon_id,
                        'scientific_name': ancestor.scientific_name,
                        'rank': ancestor.taxon_rank,
                    } for ancestor in result.ancestors
                ],
            } for result in context['object_list']
        ]

    def render_to_response(self, context):
        return HttpResponse(
            json.dumps({
                'taxa': self.get_results(context),
            }),
            content_type='application/json',
        )


class FoodRecordAPI(BaseAPIView):
    """API view to query food records."""

    # Basic view will return predator, prey names and locality data.
    # These are the fields to call select_related on
    related_fields = [
        'predator__taxon',
        'prey__taxon',
        'predator__mass_unit',
        'predator__volume_unit',
        'prey__mass_unit',
        'prey__volume_unit',
        'locality__adm0',
        'locality__adm1',
        'locality__adm2',
    ]

    def dispatch(self, request, *args, **kwargs):
        self.taxon = request.GET.get('taxon', '').lower().capitalize()
        self.taxonrole = request.GET.get('taxonrole', '')
        self.predator = request.GET.get('predator', '').lower().capitalize()
        self.prey = request.GET.get('prey', '').lower().capitalize()
        self.view = request.GET.get('view', 'basic').lower()
        if self.view == 'detailed':
            self.related_fields.extend([
                'basis',
                'context',
                'outcome',
                'conditions',
                'habitat',
                'prey_handle_mode',
                'prey_capture_mode',
                'ingestion_direction',
                'predator__lifestage',
                'predator__sex',
                'predator__component_part',
                'prey__lifestage',
                'prey__sex',
                'prey__component_part',
                'locality__elevation_unit',
                'locality__named_place',
            ])
        return super(BaseAPIView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.taxon:
            all_taxa = [d.pk for taxon in Taxon.objects.filter(scientific_name=self.taxon) for d in taxon.descendants]
            if self.taxonrole == 'pred':
                query = Q(**{'predator__taxon__pk__in': all_taxa})
            elif self.taxonrole == 'prey':
                query = Q(**{'prey__taxon__pk__in': all_taxa})
            elif self.taxonrole == 'predprey':
                query = Q(**{'predator__taxon__pk__in': all_taxa}) | Q(**{'prey__taxon__pk__in': all_taxa})
            else:
                return FoodRecord.objects.none()
            return FoodRecord.objects.filter(query).select_related(*self.related_fields)
        elif self.predator and not self.prey:
            all_taxa = [d.pk for taxon in Taxon.objects.filter(scientific_name=self.predator) for d in taxon.descendants]
            return FoodRecord.objects.filter(Q(**{'predator__taxon__pk__in': all_taxa})).select_related(*self.related_fields)
        elif self.prey and not self.predator:
            all_taxa = [d.pk for taxon in Taxon.objects.filter(scientific_name=self.prey) for d in taxon.descendants]
            return FoodRecord.objects.filter(Q(**{'prey__taxon__pk__in': all_taxa})).select_related(*self.related_fields)
        elif self.predator and self.prey:
            all_pred = [d.pk for taxon in Taxon.objects.filter(scientific_name=self.predator) for d in taxon.descendants]
            all_prey = [d.pk for taxon in Taxon.objects.filter(scientific_name=self.prey) for d in taxon.descendants]
            return FoodRecord.objects.filter(
                Q(**{'predator__taxon__pk__in': all_pred})).filter(
                    Q(**{'prey__taxon__pk__in': all_prey})).select_related(*self.related_fields)
        else:
            return []

    def get_specimen_json(self, obj):
        convert = lambda obj,to: to(obj) if obj else None
        json_response = {
            "specimen_id": obj.id,
            "taxon": obj.taxon.scientific_name,
            "taxon_id": obj.taxon.col_taxon_id,
            "taxon_rank": obj.taxon.taxon_rank,
            "count": obj.count,
            "mass": convert(obj.mass, float),
            "mass_unit": convert(obj.mass_unit, str),
            "volume": convert(obj.volume, float),
            "volume_unit": convert(obj.volume_unit, str),
        }
        if self.view == 'detailed':
            measurements = SpecimenMeasurement.objects.filter(specimen=obj).select_related('measurement_type', 'measurement_unit')
            json_response.update({
                "lifestage": convert(obj.lifestage, str),
                "sex": convert(obj.sex, str),
                "component": convert(obj.component_part, str),
                "mass": convert(obj.mass, float),
                "volume": convert(obj.volume, float),
                "measurements": [
                    {
                        "type": str(measurement.measurement_type),
                        "value": float(measurement.measurement_value),
                        "unit": str(measurement.measurement_unit)
                    } for measurement in measurements
                ],
            })
        return json_response

    def get_locality_json(self, obj):
        convert = lambda obj,to: to(obj) if obj else None
        if not obj:
            return {}
        json_response = {
            "country": str(obj.adm0),
            "state": convert(obj.adm1, str),
            "county": convert(obj.adm2, str),
            "coordinates": {
                'latitude': float(obj.point.y) if obj.point else None,
                'longitude': float(obj.point.x) if obj.point else None,
            },
        }
        if self.view == 'detailed':
            json_response.update({
                "place": str(obj.named_place.place_name) if obj.named_place else None,
                "mud_map": convert(obj.dirtmap, str),
                "elevation": {
                    "start": convert(obj.elevation_start, float),
                    "end": convert(obj.elevation_start, float),
                    "unit": convert(obj.elevation_unit, str),
                }
            })
        return json_response

    def get_details_json(self, obj):
        convert = lambda obj,to: to(obj) if obj else None
        json_response = {
            'locality': self.get_locality_json(obj.locality),
        }
        if self.view == 'detailed':
            json_response.update({
                'date': convert(obj.event_date, str),
                'basis': convert(obj.basis, str),
                'ingestion_direction': convert(obj.ingestion_direction, str),
                'context': convert(obj.context, str),
                'conditions': convert(obj.conditions, str),
                'outcome': convert(obj.outcome, str),
                'time': {
                    'start': convert(obj.start_time, str),
                    'end': convert(obj.end_time, str),
                }, 
                'habitat': convert(obj.habitat, str),
                'foraging strategy' : {
                    'capture': convert(obj.prey_capture_mode, str),
                    'subdue': convert(obj.prey_handle_mode, str),
                },
            })
        return json_response

    def get_results(self, context):
        return [
            {
                'predator': self.get_specimen_json(result.predator),
                'prey': self.get_specimen_json(result.prey),
                'details': self.get_details_json(result), 
            } for result in context['object_list']
        ]

    def render_to_response(self, context):
        return HttpResponse(
            json.dumps({
                'foodrecords': self.get_results(context),
            }),
            content_type='application/json',
        )
