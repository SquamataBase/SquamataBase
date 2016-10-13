from django.db import models


class OntologyCollection(models.Model):
    """Controlled terminology collections."""
    
    collection_name = models.CharField(
        max_length=255)
    
    class Meta:
        db_table = 'sb_ontology_collection'
        
    def __str__(self):
        return ' '.join(self.collection_name.split('_')).capitalize()


class OntologyRelationship(models.Model):
    """Controlled terminology relationships."""
    
    relationship_name = models.CharField(
        max_length=255)
        
    definition = models.TextField()
    
    class Meta:
        db_table = 'sb_ontology_relationship'
        
    def __str__(self):
        return ' '.join(self.relationship_name.split('_')).capitalize()


class OntologyTerm(models.Model):
    """Controlled terminology."""
    
    term = models.CharField(
        max_length=255)
        
    collection = models.ForeignKey(
        OntologyCollection, on_delete=models.PROTECT)
        
    definition = models.TextField(
        blank=True, null=True)
        
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.PROTECT)
        
    class Meta:
        db_table = 'sb_ontology_term'
    
    def __str__(self):
        return ' '.join(self.term.split('_')).capitalize()
        

class OntologyHasRelationship(models.Model):
    """Relationships among ontology terms."""
    
    ontology_from = models.ForeignKey(
        OntologyTerm, related_name='ontology_fromset',
        on_delete=models.PROTECT)
        
    ontology_to = models.ForeignKey(
        OntologyTerm, related_name='ontology_toset',
        on_delete=models.PROTECT)
        
    relationship = models.ForeignKey(
        OntologyRelationship, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_ontology_has_relationship'
        verbose_name = 'relationship'
        
    def __str__(self):
        return ' '.join([str(ontology_from), str(relationship).lower(),
                         str(ontology_to)])
        