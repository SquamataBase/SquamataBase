from django.shortcuts import render
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.utils.translation import ugettext as _
from dal import autocomplete
from .models import Journal, Book, BookChapter, JournalArticle, Person


class JournalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Journal.objects.none()

        qs = Journal.objects.all()

        if self.q:
            return qs.filter(Q(**{'journal_name__istartswith': self.q}))
                    
        return qs


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
            qs = Person.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
            return qs.filter(full_name__unaccent__icontains=self.q)

        return Person.objects.none()


    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

        if display_create_option and self.has_add_permission(self.request):
            vals = q.strip().split(',')
            last_name = ' '.join([w.capitalize() for w in vals[0].strip().split(' ')])
            try:
                first_name = first_name = ' '.join([w.capitalize() for w in vals[1].strip().split(' ')])
            except IndexError:
                first_name = ''
            full_name = ', '.join([last_name, first_name])
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': full_name},
                'create_id': True,
            }]
        return create_option


    def create_object(self, text):
        """Create a person given last name, first name."""
        vals = text.strip().split(',')
        assert len(vals) == 2
        first_name = ' '.join([w.capitalize() for w in vals[1].strip().split(' ')])
        last_name = ' '.join([w.capitalize() for w in vals[0].strip().split(' .')])
        return self.get_queryset().create(**{'first_name': first_name, 'last_name': last_name})

