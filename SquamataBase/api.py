from django.views.generic.list import ListView
from django.http import JsonResponse
from django.db.models import Q
from SquamataBase.FoodRecord.models import *


class BaseAPIView(object):
    """Base view for web API."""

    def dispatch(self, request, *args, **kwargs):
        self.q = request.GET.get('q', '')
        return super(BaseAPIView, self).dispatch(request, *args, **kwargs)


class QueryAPI(ListView):
    """API view to query food records."""

    def get_queryset(self):
        return IndividualSet.objects.filter(**Q({'predator__scientific_name__startswith': self.q}))


    def render_to_response(self, context):
        return JsonResponse(context)