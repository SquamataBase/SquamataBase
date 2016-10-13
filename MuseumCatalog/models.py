from django.db import models


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
                         