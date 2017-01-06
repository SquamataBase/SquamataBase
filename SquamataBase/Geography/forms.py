from django.contrib.gis import forms
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
from dal import autocomplete
from .models import *
from .widgets import *


def parse_coordinate_string(value):
    if value.find("''") != -1:  # DMS coordinate format
        v = value.split()
        deg_x = float(v[1][0:v[1].find('°')])
        deg_y = float(v[0][0:v[0].find('°')])
        x_coord = (
            abs(deg_x) + 
                float(v[1][(v[1].find('°')+1):v[1].find("'")])/60. + 
                    float(v[1][(v[1].find("'")+1):v[1].find("''")])/3600.)
        y_coord = (
            abs(deg_y) + 
                float(v[0][(v[0].find('°')+1):v[0].find("'")])/60. + 
                    float(v[0][(v[0].find("'")+1):v[0].find("''")])/3600.)
        if deg_x < 0:
            x_coord *= -1.
        if deg_y < 0:
            y_coord *= -1.
    elif value.find("'") != -1:  # DDM coordinate format
        v = value.split()
        deg_x = float(v[1][0:v[1].find('°')])
        deg_y = float(v[0][0:v[0].find('°')])
        x_coord = (
            abs(deg_x) +
                float(v[1][(v[1].find('°')+1):v[1].find("'")])/60.)
        y_coord = (
            abs(deg_y) +
                float(v[0][(v[0].find('°')+1):v[0].find("'")])/60.)
        if deg_x < 0:
            x_coord *= -1.
        if deg_y < 0:
            y_coord *= -1.
    elif value.find("°") != -1:  # DD coordinate format
        v = value.split()
        x_coord = float(v[1][0:v[1].find('°')])
        y_coord = float(v[0][0:v[0].find('°')])
    elif value.find('UTM') != -1:  # UTM coordinate format
        x_coord = int(value.split()[3][0:-1])
        y_coord = int(value.split()[4][0:-1])
    else:
        assert False, "Unrecognized coordinate format."    
    return (x_coord, y_coord)


class NamedPlaceForm(forms.ModelForm):
        
    verbatim_coordinates = CoordinateField(required=False)
    coord_format = forms.CharField(required=False)  # we use javascript to ensure this always echoes the choice in verbatim_coordinates
    utm_zone = forms.CharField(required=False)  # we use javascript to ensure this always echoes the choice in verbatim_coordinates
    parent_admin = forms.CharField(required=False)
    
    class Meta:
        model = NamedPlace
        fields = ('__all__') 
        widgets = {
            'adm0': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for countries . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'adm1': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for states . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'adm2': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for counties . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'verbatim_srid': autocomplete.ModelSelect2(
                url = 'srs-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for spatial ref system . . .',
                    'data-minimum-input-length': 1,
                },
                forward = ['coord_format', 'utm_zone']
            ),
        }
        
    def clean(self):
        cleaned_data = super(NamedPlaceForm, self).clean()
        if (cleaned_data.get('verbatim_coordinates', None) and 
                cleaned_data.get('verbatim_srid', None)):
            my_srid = cleaned_data['verbatim_srid'].srid
            srs_from = SpatialReference(my_srid)
            srs_to = SpatialReference(4326)
            ptransf = CoordTransform(srs_from, srs_to)
            value = cleaned_data['verbatim_coordinates']
            x, y = parse_coordinate_string(value)
            point = Point(x=x, y=y, srid=my_srid)
            point.transform(ptransf)
            country = cleaned_data['adm0']
            try:
                g = AdmUnitBoundary.objects.get(geoname_id=country.geoname_id)
                if g.geom.intersects(point):
                    pass
                else:
                    raise ValidationError('Point does not fall within'
                                          ' selected country boundary.')
            except ObjectDoesNotExist:
                pass    
            cleaned_data['point'] = point
            
            
                         
class LocalityForm(forms.ModelForm):
    
    verbatim_coordinates = CoordinateField(required=False)
    coord_format = forms.CharField(required=False)  # we use javascript to ensure this always echoes the choice in verbatim_coordinates
    utm_zone = forms.CharField(required=False)  # we use javascript to ensure this always echoes the choice in verbatim_coordinates
    parent_admin = forms.CharField(required=False)
    
    class Meta:
        model = Locality
        fields = ('__all__') 
        widgets = {
            'adm0': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for countries . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'adm1': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for states . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'adm2': autocomplete.ModelSelect2(
                url = 'admu-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for counties . . .',
                    'data-minimum-input-length': 2,
                },
                forward = ['parent_admin']
            ),
            'named_place': autocomplete.ModelSelect2(
                url = 'placename-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for place names . . .',
                    'data-minimum-input-length': 0,
                },
                forward = ['adm0','adm1','adm2']
            ),
            'verbatim_srid': autocomplete.ModelSelect2(
                url = 'srs-autocomplete',
                attrs = {
                    'data-placeholder': 'Search for spatial ref system . . .',
                    'data-minimum-input-length': 1,
                },
                forward = ['coord_format', 'utm_zone']
            ),
        }
        
    def clean(self):
        cleaned_data = super(LocalityForm, self).clean()
        if (cleaned_data.get('verbatim_coordinates', None) and 
                cleaned_data.get('verbatim_srid', None)):
            my_srid = cleaned_data['verbatim_srid'].srid
            srs_from = SpatialReference(my_srid)
            srs_to = SpatialReference(4326)
            ptransf = CoordTransform(srs_from, srs_to)
            value = cleaned_data['verbatim_coordinates']
            x, y = parse_coordinate_string(value)
            point = Point(x=x, y=y, srid=my_srid)
            point.transform(ptransf)
            country = cleaned_data['adm0']
            try:
                VALIDATE_COORDINATES = settings.VALIDATE_COORDINATES
            except AttributeError:
                VALIDATE_COORDINATES = True
            if VALIDATE_COORDINATES:
                try:
                    g = AdmUnitBoundary.objects.get(geoname_id=country.geoname_id)
                    if g.geom.intersects(point):
                        pass
                    else:
                        raise ValidationError('Point does not fall within'
                                              ' selected country boundary.')
                except ObjectDoesNotExist:
                    pass
            cleaned_data['point'] = point

