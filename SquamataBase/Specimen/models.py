from django.db import models
from SquamataBase.Taxonomy.models import Taxon
from SquamataBase.Glossary.models import OntologyTerm
from SquamataBase.Workbench.models import Workbench

class Museum(models.Model):
    """Natural history institutions."""
    
    museum_name = models.CharField(
        max_length=255)
        
    museum_abbr = models.CharField(
        max_length=255)
        
    address = models.CharField(
        max_length=255)

    class Meta:
        db_table = 'sb_museum'
        
        
    def __str__(self):
        return ': '.join([self.museum_abbr, self.museum_name])


class MuseumCollection(models.Model):
    """Natural history institution collection types."""
    
    museum = models.ForeignKey(
        Museum, on_delete=models.PROTECT)
        
    collection_name = models.CharField(
        max_length=255)

    collection_code = models.CharField(
        max_length=255, blank=True, null=True)
        
    class Meta:
        db_table = 'sb_museum_collection'
        
    def __str__(self):
        return self.collection_name
        

class Voucher(models.Model):
    """Voucher specimens."""
    
    museum = models.ForeignKey(
        Museum, on_delete=models.PROTECT)
        
    museum_collection = models.ForeignKey(
        MuseumCollection, blank=True, null=True, on_delete=models.PROTECT)
        
    catalog_number = models.CharField(
        max_length=255, blank=True, null=True)
        
    field_number = models.CharField(
        max_length=255, blank=True, null=True)
        
    class Meta:
        db_table = 'sb_voucher'

    def __str__(self):
        voucher = ' '.join([self.museum.museum_abbr,
                            (self.catalog_number if self.catalog_number is not ''
                                else self.field_number)])
        if self.museum_collection is not None:
            return ' '.join([voucher, '({} Collection)'.format(str(self.museum_collection))])
        return voucher


class Specimen(models.Model):
    """Table that holds instances of sets of individual organisms.
    
    .. py:attribute:: taxon
    .. py:attribute:: verbatim_name
    .. py:attribute:: ambiguous
    .. py:attribute:: count
    .. py:attribute:: mass
    .. py:attribute:: mass_unit
    .. py:attribute:: volume
    .. py:attribute:: volume_unit
    .. py:attribute:: lifestage
    .. py:attribute:: sex
    .. py:attribute:: anatomical_part
    """
    wb = models.ForeignKey(
        Workbench, blank=True, null=True, on_delete=models.SET_NULL)

    taxon = models.ForeignKey(
        Taxon, on_delete=models.PROTECT)
        
    verbatim_name = models.CharField(
        max_length=255)
        
    ambiguous = models.BooleanField()
    
    count = models.IntegerField(
        blank=True, null=True)
    
    mass = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    
    mass_unit = models.ForeignKey(
        OntologyTerm, related_name='specimen_massunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    volume = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    
    volume_unit = models.ForeignKey(
        OntologyTerm, related_name='specimen_volumeunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    lifestage = models.ForeignKey(
        OntologyTerm, related_name='specimen_lifestageset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    sex = models.ForeignKey(
        OntologyTerm, related_name='specimen_sexset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    component_part = models.ForeignKey(
        OntologyTerm, related_name='specimen_componentset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_specimen'
        
    def __str__(self):
        voucher_str= ':'.join([str(v) for v in self.vouchers])
        if voucher_str != '':
            return ' | '.join([str(self.id), self.taxon.scientific_name,
                                voucher_str])
        return ' | '.join([str(self.id), self.taxon.scientific_name])

    @property
    def measurements(self):
        return SpecimenMeasurement.objects.filter(specimen_id=self.id)

    @property
    def vouchers(self):
        return SpecimenVoucher.objects.filter(specimen_id=self.id)

class SpecimenIntersection(models.Model):
    """Overlapping sets of individual organisms."""
    
    specimen = models.ForeignKey(
        Specimen, related_name='specimenintersection_childset',
        on_delete=models.PROTECT)
        
    intersects_with = models.ForeignKey(
        Specimen, related_name='specimenintersection_parentset',
        on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_specimen_intersection'
        verbose_name = 'intersection'

    def __str__(self):
        return ''

class SpecimenMeasurement(models.Model):
    """Measurements made on sets of individual organisms."""
    
    specimen = models.ForeignKey(
        Specimen, on_delete=models.PROTECT)
        
    measurement_type = models.ForeignKey(
        OntologyTerm, related_name='specimenmeasurement_measurementtypeset',
        on_delete=models.PROTECT)
        
    measurement_value = models.DecimalField(
        max_digits=10, decimal_places=3)
        
    measurement_unit = models.ForeignKey(
        OntologyTerm, related_name='specimenmeasurement_measurementunitset',
        on_delete=models.PROTECT)
        
    verbatim_value = models.CharField(
        max_length=255)

    class Meta:
        db_table = 'sb_specimen_measurement'
        verbose_name = 'measurement'

    def __str__(self):
        return ' '.join([str(self.measurement_type), str(self.measurement_value), str(self.measurement_unit)])

class SpecimenVoucher(models.Model):
    """Voucher specimens associated with individual organisms."""
    
    specimen = models.ForeignKey(
        Specimen, on_delete=models.PROTECT)
        
    voucher = models.ForeignKey(
        Voucher, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_specimen_voucher'
        verbose_name = 'voucher'
        
    def __str__(self):
        return str(self.voucher)
                         