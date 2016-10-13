from django.shortcuts import render
from django.db.models import Q
from dal import autocomplete
from .models import Journal, Book, BookChapter, JournalArticle, Person


class JournalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Journal.objects.none()

        qs = Journal.objects.all()

        if self.q:
            return qs.filter(Q(**{'journal_name__istartswith': self.q}))
                    
        return Journal.objects.none()


class BookAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Book.objects.none()

        if self.q:
            return Book.objects.filter(Q(**{'title__istartswith': self.q}))
                    
        return Book.objects.none()


class ReferenceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Book.objects.none()
        
        ref_type = self.forwarded.get('ref_type', None)
        
        model = None
        if ref_type:
            if ref_type == 'Book':
                model = Book
            elif ref_type == 'Journal article':
                model = JournalArticle
            elif ref_type == 'Book chapter':
                model = BookChapter
            else:
                raise NotImplementedError('Implement this model before using.')
        
        if self.q:
            return model.objects.filter(Q(**{'title__istartswith': self.q}))
        
        return model.objects.none()
        
            
class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Person.objects.none()

        if self.q:
            c = Q(**{'last_name__unaccent__istartswith': self.q})
            c |= Q(**{'first_name__unaccent__istartswith': self.q})
            return Person.objects.filter(c)
                    
        return Person.objects.none()


