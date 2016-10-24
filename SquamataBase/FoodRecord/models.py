from django.db import models
from SquamataBase.Bibliography.models import Ref
from SquamataBase.Geography.models import Locality
from SquamataBase.Glossary.models import OntologyTerm
from SquamataBase.MuseumCatalog.models import Voucher
from SquamataBase.Taxonomy.models import Taxon
from SquamataBase.Workbench.models import Workbench
from .validators import *


class IndividualSet(models.Model):
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
        OntologyTerm, related_name='individualset_massunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    volume = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    
    volume_unit = models.ForeignKey(
        OntologyTerm, related_name='individualset_volumeunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    lifestage = models.ForeignKey(
        OntologyTerm, related_name='individualset_lifestageset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    sex = models.ForeignKey(
        OntologyTerm, related_name='individualset_sexset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    component_part = models.ForeignKey(
        OntologyTerm, related_name='individualset_componentset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_individual_set'
        
    def __str__(self):
        vouchers = IndividualSetVoucher.objects.filter(individual_set=self.id)
        voucher_str= ':'.join([str(v) for v in vouchers])
        if voucher_str != '':
            return ' | '.join([str(self.id), self.taxon.scientific_name,
                                voucher_str])
        return ' | '.join([str(self.id), self.taxon.scientific_name])


class IndividualSetIntersection(models.Model):
    """Overlapping sets of individual organisms."""
    
    individual_set = models.ForeignKey(
        IndividualSet, related_name='individualsetintersection_childset',
        on_delete=models.PROTECT)
        
    intersects_with = models.ForeignKey(
        IndividualSet, related_name='individualsetintersection_parentset',
        on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_individual_set_intersection'
        verbose_name = 'intersection'

    def __str__(self):
        return ''

class IndividualSetMeasurement(models.Model):
    """Measurements made on sets of individual organisms."""
    
    individual_set = models.ForeignKey(
        IndividualSet, on_delete=models.PROTECT)
        
    measurement_type = models.ForeignKey(
        OntologyTerm, related_name='individualsetmeasurement_measurementtypeset',
        on_delete=models.PROTECT)
        
    measurement_value = models.DecimalField(
        max_digits=10, decimal_places=3)
        
    measurement_unit = models.ForeignKey(
        OntologyTerm, related_name='individualsetmeasurement_measurementunitset',
        on_delete=models.PROTECT)
        
    verbatim_value = models.CharField(
        max_length=255)

    class Meta:
        db_table = 'sb_individual_set_measurement'
        verbose_name = 'measurement'

    def __str__(self):
        return ''

class IndividualSetVoucher(models.Model):
    """Voucher specimens associated with individual organisms."""
    
    individual_set = models.ForeignKey(
        IndividualSet, on_delete=models.PROTECT)
        
    voucher = models.ForeignKey(
        Voucher, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_individual_set_voucher'
        verbose_name = 'voucher'
        
    def __str__(self):
        return str(self.voucher)


class FoodRecord(models.Model):
    """Predator-Prey observations.
    
        .. py:attribute:: basis
            
            What is the evidence supporting this trophic interaction? 
            
        .. py:attribute:: context
            
            Was the predation event observed or inferred from evidence?
            
        .. py:attribute:: conditions
        
            Did this predation event occur under natural conditions
            or captive conditions?
            
        .. py:attribute:: outcome
        
            What was the outcome of this predation event? 
            Was the predator successful, was the attempt abandoned, was 
            the event interrupted, or did the predator die in its attempt?
            
        .. py:attribute:: ingestion_direction
        
            What orientation was the prey swallowed from?
    """
    wb = models.ForeignKey(
        Workbench, blank=True, null=True, on_delete=models.SET_NULL)
    
    ref = models.ForeignKey(
        Ref, blank=True, null=True, on_delete=models.PROTECT)
        
    predator = models.ForeignKey(
        IndividualSet, related_name='foodrecord_predatorset',
        help_text='search on id, latin name, or voucher code',
        on_delete=models.PROTECT)
        
    prey = models.ForeignKey(
        IndividualSet, related_name='foodrecord_preyset',
        help_text='search on id, latin name, or voucher code',
        on_delete=models.PROTECT)
        
    basis = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_evidenceset',
        on_delete=models.PROTECT)

    alimentary_pos = models.CharField(
        max_length=255, blank=True, null=True)
        
    context = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_contextset',
        on_delete=models.PROTECT)
        
    conditions = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_conditionset',
        on_delete=models.PROTECT)
        
    outcome = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_outcomeset',
        on_delete=models.PROTECT)
        
    ingestion_direction = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_ingestedset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    locality = models.ForeignKey(
        Locality, related_name='foodrecord_localityset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    event_date = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_date])
        
    start_time = models.CharField(
        max_length=255, blank=True, null=True,
        validators=[validate_time])
        
    end_time = models.CharField(
        max_length=255, blank=True, null=True,
        validators=[validate_time])
        
    habitat = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_habitatset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    verbatim_habitat = models.CharField(
        max_length=255, blank=True, null=True)
    
    prey_capture_mode = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_preycaptureset',
        blank=True, null=True, on_delete=models.PROTECT)

    prey_handle_mode = models.ForeignKey(
        OntologyTerm, related_name='foodrecord_preyhandleset',
        blank=True, null=True, on_delete=models.PROTECT)

    remark = models.TextField(
        blank=True, null=True)

    class Meta:
        db_table = 'sb_foodrecord'
    
    def __str__(self):
        foodrecord_str = ' -> '.join([self.predator.taxon.scientific_name,
                                      self.prey.taxon.scientific_name])
        return '. '.join([str(self.id), foodrecord_str, str(self.ref)])


class FoodRecordMedia(models.Model):
    """External files associated with food records."""
    
    filepath = models.CharField(
        max_length=255)
        
    foodrecord = models.ForeignKey(
        FoodRecord, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_foodrecord_media'
        
    def __str__(self):
        return ''
        
        
class DataSet(models.Model):
    """Collection of food records."""
    
    ref = models.ForeignKey(
        Ref, blank=True, null=True, on_delete=models.PROTECT)
    
    n_predators_examined = models.IntegerField(
        blank=True, null=True,
        help_text='number of predators examined for prey')
        
    n_predators_ate = models.IntegerField(
        blank=True, null=True, help_text='number of predators containing prey')
    
    n_prey_eaten = models.IntegerField(
        blank=True, null=True, help_text='number of prey items recovered')
        
    mass_prey_eaten = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True,
        help_text='total biomass of prey items recovered')
        
    mass_unit = models.ForeignKey(
        OntologyTerm, related_name='dataset_massunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    volume_prey_eaten = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True,
        help_text='total volume of prey items recovered')
    
    volume_unit = models.ForeignKey(
        OntologyTerm, related_name='dataset_volumeunitset',
        blank=True, null=True, on_delete=models.PROTECT)
    
    start_date = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_date])
            
    end_date = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_date])
        
    class Meta:
        db_table = 'sb_dataset'
        
    def __str__(self):
        return str(self.ref)
        
        
class DataSetLocality(models.Model):
    """Locations from which observations originate."""
    
    dataset = models.ForeignKey(
        DataSet, on_delete=models.PROTECT)
    
    locality = models.ForeignKey(
        Locality, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_dataset_locality'
        verbose_name_plural = 'data set localities'

    def __str__(self):
        return str(self.locality)
        
        
class DataSetMethod(models.Model):
    """Methods used to compile observations for data set."""
    
    dataset = models.ForeignKey(
        DataSet, on_delete=models.PROTECT)
        
    basis = models.ForeignKey(
        OntologyTerm, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_dataset_method'

    def __str__(self):
        return str(self.basis)
        
        
class DataSetFoodRecord(models.Model):
    """Predator-Prey observations associated with data sets."""
    
    dataset = models.ForeignKey(
        DataSet, on_delete=models.PROTECT)
        
    foodrecord = models.ForeignKey(
        FoodRecord, help_text='search on latin name of predator or prey',
        on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_dataset_foodrecord'
        
    def __str__(self):
        return str(self.foodrecord)
