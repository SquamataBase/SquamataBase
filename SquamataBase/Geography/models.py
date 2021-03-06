from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point
from django.conf import settings
from SquamataBase.Glossary.models import OntologyTerm


class SpatialRefSys(models.Model):
    """Spatial reference systems table. 
    
    .. py:admonition:: Note
    
        This table is automatically created by enabling the postgis
        extension on the database.
    """
    
    srid = models.IntegerField(
        primary_key=True)
        
    auth_name = models.CharField(
        max_length=256, blank=True, null=True)
        
    auth_srid = models.IntegerField(
        blank=True, null=True)
        
    srtext = models.CharField(
        max_length=2048, blank=True, null=True)
        
    proj4text = models.CharField(
        max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'
        
    def __str__(self):
        import re
        srtext = self.srtext
        if srtext.startswith('GEOGCS'):
            p = re.compile(
                '(?:GEOGCS\[")(.+?)(?:",DATUM.+?SPHEROID\[")(.+?)(?:".)')
            match = re.findall(p, srtext)
            if len(match):
                return match[0][0] + ' (' + match[0][1] + ')'
        elif srtext.startswith('PROJCS'):
            p = re.compile(
                '(?:PROJCS\[")(.+?)(?:",GEOGCS.+?SPHEROID\[")(.+?)(?:".)')
            match = re.findall(p, srtext)
            if len(match):
                return match[0][0] + ' (' + match[0][1] + ')'
        return ''
        
        
class AdmUnit(models.Model):
    """Administrative units from geonames.org."""
 
    geoname_id = models.IntegerField(
        primary_key=True)
    
    admin_level = models.IntegerField()
    
    unit_name_ascii = models.CharField(
        max_length=255)
        
    unit_name = models.CharField(
        max_length=255)
        
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_adm'
        verbose_name = 'Administrative unit'
        verbose_name_plural = 'Administrative units'
        
    def __str__(self):
        return self.unit_name_ascii


class AdmUnitBoundary(models.Model):
    """Top-level administrative unit boundaries from geonames.org."""
        
    geoname_id = models.OneToOneField(AdmUnit, primary_key=True, db_column='geoname_id')
          
    # wgs84 srid
    geom = models.MultiPolygonField(srid=4326)
    
    class Meta:
        db_table = 'sb_adm_boundary'
        verbose_name = 'Administrative unit shapefile'
        verbose_name_plural = 'Administrative unit shapefiles'
        
    def __str__(self):
        return str(self.geoname_id)

    @property
    def point(self):
        """Choose a uniform random point within boundary."""
        from numpy import random
        ext = self.geom.extent
        lon = random.uniform(low=ext[0], high=ext[2])
        lat = random.uniform(low=ext[1], high=ext[3])
        pnt = Point(x=lon, y=lat, srid=self.geom.srid)
        if self.geom.intersects(pnt):
            return pnt
        else:
            return self.point
        

class NamedPlace(models.Model):
    """Gazetted place names."""
    
    adm0 = models.ForeignKey(
        AdmUnit, related_name='namedplace_countryset', on_delete=models.PROTECT)
        
    adm1 = models.ForeignKey(
        AdmUnit, related_name='namedplace_stateset', blank=True,
        null=True, on_delete=models.PROTECT)
        
    adm2 = models.ForeignKey(
        AdmUnit, related_name='namedplace_countyset', blank=True,
        null=True, on_delete=models.PROTECT)
        
    place_name = models.CharField(
        max_length=255)
    
    verbatim_coordinates = models.CharField(
        max_length=255, blank=True, null=True)
    
    verbatim_srid = models.ForeignKey(
        SpatialRefSys, blank=True, null=True,
        on_delete=models.DO_NOTHING, db_column='srid')
            
    point = models.PointField(
        srid=4326, blank=True, null=True)
        
    elevation_start = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
        
    elevation_end = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    
    elevation_unit = models.ForeignKey(
        OntologyTerm, blank=True, null=True, on_delete=models.PROTECT)
        
    remark = models.TextField(
        blank=True, null=True)

    class Meta:
        db_table = 'sb_namedplace'
        verbose_name = 'Place name'
        verbose_name_plural = 'Place names'
    
    def __str__(self):
        return self.place_name

class Locality(models.Model):
    """Points on the map."""
    
    adm0 = models.ForeignKey(
        AdmUnit, related_name='locality_countryset', on_delete=models.PROTECT)
    
    adm1 = models.ForeignKey(
        AdmUnit, related_name='locality_stateset', blank=True,
        null=True, on_delete=models.PROTECT)
    
    adm2 = models.ForeignKey(
        AdmUnit, related_name='locality_countyset', blank=True,
        null=True, on_delete=models.PROTECT)
    
    named_place = models.ForeignKey(
        NamedPlace, blank=True, null=True, on_delete=models.PROTECT)
    
    dirtmap = models.CharField(
        max_length=255, blank=True, null=True)
        
    verbatim_coordinates = models.CharField(
        max_length=255, blank=True, null=True)
    
    verbatim_srid = models.ForeignKey(
        SpatialRefSys, blank=True, null=True,
        on_delete=models.DO_NOTHING, db_column='srid')
    
    point = models.PointField(
        srid=4326, blank=True, null=True)
    
    coordinate_uncertainty = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    
    uncertainty_unit = models.ForeignKey(
        OntologyTerm, related_name='locality_uncertaintyunitset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    georeferenced_from = models.CharField(
        max_length=255, blank=True, null=True)
        
    elevation_start = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
        
    elevation_end = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    
    elevation_unit = models.ForeignKey(
        OntologyTerm, related_name='locality_elevationunitset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    verbatim_elevation = models.CharField(
        max_length=255, blank=True, null=True)
    
    remark = models.TextField(
        blank=True, null=True)

    class Meta:
        db_table = 'sb_locality'
        verbose_name = 'Locality'
        verbose_name_plural = 'Localities'
        
    def __str__(self):
        if self.verbatim_coordinates is not None and self.verbatim_coordinates != '':
            if self.named_place is not None:
                return ', '.join([str(self.named_place), self.verbatim_coordinates])
            return self.verbatim_coordinates
        elif self.named_place is not None:
            return str(self.named_place)
        else:
            return ', '.join([str(a) for a in [self.dirtmap, self.adm2, self.adm1, self.adm0] if a != '' and a is not None])

    def get_point(self):
        if self.point is not None:
            return self.point
        else:
            try:
                if self.named_place.point is not None:
                    return self.named_place.point
                else:
                    raise AttributeError
            except AttributeError:
                if settings.ALLOW_RANDOM_COORDINATES:
                    try:
                        bndry = AdmUnitBoundary.objects.get(geoname_id=self.adm2)
                        return bndry.point
                    except:
                        try:
                            bndry = AdmUnitBoundary.objects.get(geoname_id=self.adm1)
                            return bndry.point
                        except:
                            try:
                                bndry = AdmUnitBoundary.objects.get(geoname_id=self.adm0)
                                return bndry.point
                            except:
                                return None
                else:
                    return None
                
               