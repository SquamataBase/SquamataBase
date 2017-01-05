from django.db import models
from SquamataBase.Glossary.models import OntologyTerm
from SquamataBase.Workbench.models import Workbench

class Ref(models.Model):
    """Base model for storing references to data sources."""
    
    ref_type = models.ForeignKey(
        OntologyTerm, on_delete=models.PROTECT)

    wb = models.ForeignKey(
        Workbench, blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'sb_ref'
        verbose_name = 'Data source'
        verbose_name_plural = 'Data sources'
       
    def get_title(self):
        if self.ref_type.term == 'book':
            return str(Book.objects.get(ref=self.id))
        elif self.ref_type.term == 'book_chapter':
            return str(BookChapter.objects.get(ref=self.id))
        elif self.ref_type.term == 'journal_article':
            return str(JournalArticle.objects.get(ref=self.id))
        else:
            raise NotImplementedError('Implement this model before using.')
            
    def __str__(self):
        return self.get_title()
    

class Person(models.Model):
    """People who contribute to data sources."""
    
    last_name = models.CharField(
        max_length=255)

    last_name_ascii = models.CharField(
        max_length=255)
    
    first_name = models.CharField(
        max_length=255)

    first_name_ascii = models.CharField(
        max_length=255)

    class Meta:
        db_table = 'sb_person'
        verbose_name_plural = 'people'
        
    def __str__(self):
        return ', '.join([self.last_name, self.first_name])


class Contribution(models.Model):
    """Authorship contributions for data sources."""
    
    person_role = models.ForeignKey(
        OntologyTerm, on_delete=models.PROTECT)
    
    person = models.ForeignKey(
        Person, on_delete=models.PROTECT)
    
    ref = models.ForeignKey(Ref,
        on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'sb_contribution'
        
    def __str__(self):
        return ''


class Book(models.Model):
    ref = models.OneToOneField(
        Ref, primary_key=True, on_delete=models.CASCADE)
        
    title = models.CharField(
        max_length=255)
        
    year_published = models.IntegerField()
    
    publisher = models.CharField(
        max_length=255, blank=True, null=True)
        
    pages = models.IntegerField(
        blank=True, null=True)
        
    isbn = models.CharField(
        max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'sb_book'
    
    def __str__(self):
        return self.title
    
    
class BookChapter(models.Model):
    ref = models.OneToOneField(
        Ref, primary_key=True, on_delete=models.CASCADE)
    
    title = models.CharField(
        max_length=255)
    
    page_start = models.CharField(
        max_length=255)
    
    page_end = models.CharField(
        max_length=255)
    
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sb_book_chapter'

    def __str__(self):
        return ' in '.join([self.title, str(self.book)])


class Journal(models.Model):
    journal_name = models.CharField(
        max_length=255)
        
    issn = models.CharField(
        max_length=255, blank=True, null=True)
        
    prior_names = models.TextField(
        blank=True, null=True)
    
    class Meta:
        db_table = 'sb_journal'
    
    def __str__(self):
        return self.journal_name
        

class JournalArticle(models.Model):
    ref = models.OneToOneField(
        Ref, primary_key=True, on_delete=models.CASCADE)
        
    title = models.CharField(
        max_length=255)
        
    journal = models.ForeignKey(
        Journal, on_delete=models.PROTECT)
        
    volume = models.CharField(
        max_length=255)
    
    issue = models.CharField(
        max_length=255, blank=True, null=True)
    
    year_published = models.IntegerField()
    
    page_start = models.CharField(
        max_length=255)
    
    page_end = models.CharField(
        max_length=255)
    
    doi = models.CharField(
        max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'sb_journal_article'
        
    def __str__(self):
        v = self.volume
        if self.issue:
            v += ' ({})'.format(self.issue) 
        return '. '.join([self.title.strip('.'), ' '.join([str(self.journal), v]),
                          str(self.year_published)])

