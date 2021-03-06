from django.contrib import admin
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .forms import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('last_name_ascii', 'first_name_ascii')
    list_display = ('id', 'last_name', 'first_name')

        
@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    pass


class JournalArticleInlineAdmin(admin.StackedInline):
    model = JournalArticle
    form = JournalArticleForm
    

class BookInlineAdmin(admin.StackedInline):
    model = Book
        
        
class BookChapterInlineAdmin(admin.StackedInline):
    model = BookChapter
    form = BookChapterForm
    
    
class ContributionInlineAdmin(admin.TabularInline):
    model = Contribution
    form = ContributionForm
    extra = 1
    show_change_link = True
    
    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0;
        return self.extra
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person_role':
            try:
                cid = OntologyCollection.objects.get(collection_name='person_roles').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(ContributionInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs) 


class RefTypeFilter(admin.SimpleListFilter):
    title = 'Publication type'
    parameter_name = 'ref_type__id__exact'

    def lookups(self, request, model_admin):

        qs = OntologyTerm.objects.filter(Q(**{'id__in': Ref.objects.distinct().values_list('ref_type_id', flat=True)}))
        
        for ref_type in qs:
            yield (str(ref_type.id), str(ref_type))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ref_type_id=self.value())
        return queryset


class RefNameFilter(RefTypeFilter):
    title = 'Publication name'
    parameter_name = 'pub__id__exact'
    pubtype = 'ref_type__id__exact'
    model = None
    def lookups(self, request, model_admin):
        import itertools
        if self.pubtype in request.GET:
            term = OntologyTerm.objects.get(id=int(request.GET[self.pubtype])).term
            if term == 'journal_article':
                self.model = Journal
            elif term == 'book':
                self.model = Book
            elif term == 'book_chapter':
                self.model = BookChapter
            else:
                self.model = None
            qs = self.model.objects.all()
        else:
            self.model = None
            qs = itertools.chain(Book.objects.all(), BookChapter.objects.all(), Journal.objects.all())
        
        for j in qs:
            yield (str(j.pk), str(j))

    def queryset(self, request, queryset):
        if self.value():
            if self.model == Journal:
                articles = JournalArticle.objects.all()
                return Ref.objects.filter(id__in=articles.filter(journal_id=self.value()).values_list('ref_id', flat=True))
            elif self.model == Book:
                articles = Book.objects.all()
                return Ref.objects.filter(id__in=articles.filter(pk=self.value()).values_list('ref_id', flat=True))
            elif self.model == BookChapter:
                articles = BookChapter.objects.all()
                return Ref.objects.filter(id__in=articles.filter(pk=self.value()).values_list('ref_id', flat=True))
            else:
                return queryset
        return queryset


@admin.register(Ref)
class RefAdmin(admin.ModelAdmin):
    
    inlines = (
        JournalArticleInlineAdmin,
        BookInlineAdmin,
        BookChapterInlineAdmin,
        ContributionInlineAdmin,
    )
    
    exclude = ('wb',)
    list_display = ('id', 'get_title',)
    search_fields = ('journalarticle__title', 'book__title', 'bookchapter__title',)
    list_filter = (RefTypeFilter, RefNameFilter)

    class Media:
        js = ('Bibliography/js/dynamic_ref_form.js',)
    
    def get_title(self, obj):
        if obj.ref_type.term == 'journal_article':
            return str(JournalArticle.objects.get(ref=obj.id))
        elif obj.ref_type.term == 'book':
            return str(Book.objects.get(ref=obj.id))
        elif obj.ref_type.term == 'book_chapter':
            return str(BookChapter.objects.get(ref=obj.id))
    get_title.short_description = 'Title'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ref_type':
            try:
                cid = OntologyCollection.objects.get(collection_name='publication_types').id
            except ObjectDoesNotExist:
                cid = 0
            kwargs['queryset'] = OntologyTerm.objects.filter(collection=cid)
        return super(RefAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    