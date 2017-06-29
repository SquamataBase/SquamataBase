from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from SquamataBase.Specimen.models import *

register = template.Library()

@register.inclusion_tag('site/specimen_measurements.html')
def specimen_measurements(specimen):
    measurements = SpecimenMeasurement.objects.filter(specimen_id=specimen).select_related('measurement_type', 'measurement_unit')
    return {'measurements': measurements}