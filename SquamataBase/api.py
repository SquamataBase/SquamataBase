import json
from django.views.generic.list import BaseListView
from django.http import HttpResponse
from django.db.models import Q
from SquamataBase.Specimen.models import *
from SquamataBase.FoodRecord.models import *
from SquamataBase.Taxonomy.models import Taxon

class BaseAPIView(BaseListView):
    """Base view for web API."""

    http_methods_names = ['get']  # only get allowed
    model_fields = []
    return_fields = {}

class FoodRecordAPI(BaseAPIView):
    """API view to query food records."""

    sql = """
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = %s
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT col_taxon_id FROM q
    """

    # basic view - return predator, prey id's and location
    related_fields = [
        'predator__taxon',
        'prey__taxon',
        'locality__adm0',
        'locality__adm1',
        'locality__adm2',
    ]

    def dispatch(self, request, *args, **kwargs):
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
        if self.predator and not self.prey:
            all_taxa = [taxon.pk for taxon in Taxon.objects.raw(self.sql, [self.predator])]
            return FoodRecord.objects.filter(Q(**{'predator__taxon__pk__in': all_taxa})).select_related(*self.related_fields)
        elif self.prey and not self.predator:
            all_taxa = [taxon.pk for taxon in Taxon.objects.raw(self.sql, [self.prey])]
            return FoodRecord.objects.filter(Q(**{'prey__taxon__pk__in': all_taxa})).select_related(*self.related_fields)
        elif self.predator and self.prey:
            all_pred = [taxon.pk for taxon in Taxon.objects.raw(self.sql, [self.predator])]
            all_prey = [taxon.pk for taxon in Taxon.objects.raw(self.sql, [self.prey])]
            return FoodRecord.objects.filter(
                Q(**{'predator__taxon__pk__in': all_pred})).filter(
                    Q(**{'prey__taxon__pk__in': all_prey})).select_related(*self.related_fields)
        else:
            return []

    def get_specimen_json(self, obj):
        convert = lambda obj,to: to(obj) if obj else None
        json_response = {
            "id": obj.id,
            "taxon": obj.taxon.scientific_name,
            "count": obj.count
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
