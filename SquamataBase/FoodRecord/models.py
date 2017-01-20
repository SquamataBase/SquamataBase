from django.db import models
from SquamataBase.Bibliography.models import Ref
from SquamataBase.Geography.models import Locality
from SquamataBase.Glossary.models import OntologyTerm
from SquamataBase.Specimen.models import Specimen, Voucher
from SquamataBase.Taxonomy.models import Taxon
from SquamataBase.Workbench.models import Workbench
from .validators import *


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
        Specimen, related_name='foodrecord_predatorset',
        help_text='search on id, latin name, or voucher code',
        on_delete=models.PROTECT)
        
    prey = models.ForeignKey(
        Specimen, related_name='foodrecord_preyset',
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
        return self.predator.taxon.scientific_name.upper() + '. DIET: ' + self.prey.taxon.scientific_name.upper()

    @property
    def point(self):
        try:
            return self.locality.get_point()
        except AttributeError:
            # if there is no locality there might be one associated
            # with a dataset
            try:
                d = DataSetFoodRecord.objects.get(foodrecord=self).dataset
                return d.point
            except:
                return None

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
        db_table = 'sb_frdataset'
        
    def __str__(self):
        return str(self.ref)

    @property
    def point(self):
        """Choose a uniform random point from set of dataset localities."""
        from numpy import random
        localities = DataSetLocality.objects.filter(dataset=self)
        p = None
        for i, l in enumerate(localities):
            if not random.randint(i+1):
                p = l.locality.get_point()
        return p
        
        
class DataSetLocality(models.Model):
    """Locations from which observations originate."""
    
    dataset = models.ForeignKey(
        DataSet, on_delete=models.PROTECT)
    
    locality = models.ForeignKey(
        Locality, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_frdataset_locality'
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
        db_table = 'sb_frdataset_method'

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
        db_table = 'sb_frdataset_foodrecord'
        
    def __str__(self):
        return str(self.foodrecord)
