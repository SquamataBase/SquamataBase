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


    def dispatch(self, request, *args, **kwargs):
        self.predator = request.GET.get('predator', '').lower().capitalize()
        self.prey = request.GET.get('prey', '').lower().capitalize()
        return super(BaseAPIView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.predator:
            all_taxa = [taxon.pk for taxon in Taxon.objects.raw(self.sql, [self.predator])]
            return FoodRecord.objects.filter(Q(**{'predator__taxon__pk__in': all_taxa}))
        else:
            return []


    def get_specimen_json(self, obj):
        return {
            "id": obj.id,
            "taxon": obj.taxon.scientific_name,
            "count": str(obj.count) if obj.count else '',
            "mass": str(obj.mass) if obj.mass else '',
            "volume": str(obj.volume) if obj.volume else '',
            "measurements": [
                {
                    "type": str(measurement.measurement_type),
                    "value": str(measurement.measurement_value),
                    "unit": str(measurement.measurement_unit.term)
                } for measurement in SpecimenMeasurement.objects.filter(specimen=obj)
            ]
        }

    def get_results(self, context):

        return [
            {
                'predator': self.get_specimen_json(result.predator),
                'prey': self.get_specimen_json(result.prey)
            } for result in context['object_list']
        ]


    def render_to_response(self, context):
    
        return HttpResponse(
            json.dumps({
                'foodrecords': self.get_results(context),
            }),
            content_type='application/json',
        )
