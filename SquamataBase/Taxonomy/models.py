from django.db import models
from django.db.models import F

class Taxon(models.Model):
    """Skeleton taxon concept from Catalogue of Life."""
    
    col_taxon_id = models.IntegerField(
        primary_key=True)
    
    col_identifier = models.CharField(
        max_length=255, blank=True, null=True)
        
    scientific_name = models.CharField(
        max_length=255, db_index=True)
    
    taxon_rank = models.CharField(
        max_length=255, blank=True, null=True)
    
    taxon_status = models.CharField(
        max_length=255, db_index=True, blank=True, null=True)
        
    accepted_name = models.ForeignKey(
        'self', related_name='taxon_acceptednameset', db_index=True,
        blank=True, null=True, on_delete=models.PROTECT)
        
    parent_name = models.ForeignKey(
        'self', related_name='taxon_parentnameset',
        blank=True, null=True, on_delete=models.PROTECT)
        
    author = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sb_taxon'
        verbose_name_plural = 'taxa'

    def __str__(self):
        return self.scientific_name

    def get_ancestors(self):
        if self.parent_name is None:
            return Taxon.objects.none()
        return Taxon.objects.filter(col_taxon_id=self.parent_name.col_taxon_id).select_related('parent_name') | self.parent_name.get_ancestors()

    def get_descendants(self):
        for child in Taxon.objects.filter(parent_name=self.col_taxon_id):
            yield child
            for d in child.get_descendants():
                yield d


class TaxonView(models.Model):
    """SQL view of a subset of taxa.

        These are materialized views created in the underlying
        database for the sole purpose of improving query
        performance for autocompletion on scientific names.
    """
    
    col_taxon_id = models.IntegerField(
        primary_key=True)
    
    col_identifier = models.CharField(
        max_length=255, blank=True, null=True)
        
    scientific_name = models.CharField(
        max_length=255)
    
    taxon_rank = models.CharField(
        max_length=255, blank=True, null=True)
    
    taxon_status = models.CharField(
        max_length=255, blank=True, null=True)
        
    accepted_name = models.ForeignKey(
        'self', related_name='taxonview_acceptednameset',
        blank=True, null=True, on_delete=models.DO_NOTHING)
        
    parent_name = models.ForeignKey(
        'self', related_name='taxonview_parentnameset',
        blank=True, null=True, on_delete=models.DO_NOTHING)
        
    author = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
        managed = False

    def __str__(self):
        return self.scientific_name
        
class TaxonAmphibian(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_amphibian'
        
class TaxonBird(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_bird'

class TaxonFish(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_fish'

class TaxonMammal(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_mammal'

class TaxonReptile(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_reptile'
        
class TaxonAnnelid(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_annelid'

class TaxonArthropod(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_arthropod'

class TaxonMollusk(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_mollusk'
        
class TaxonOnychophoran(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_onychophoran'
        
class TaxonAnimal(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_animal'
        
class TaxonFungus(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_fungus'

class TaxonPlant(TaxonView):
    class Meta(TaxonView.Meta):
        db_table = 'sb_taxon_plant'
