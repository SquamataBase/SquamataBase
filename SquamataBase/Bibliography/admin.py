from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from SquamataBase.Glossary.models import OntologyCollection, OntologyTerm
from .models import *
from .forms import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

        
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


@admin.register(Ref)
class RefAdmin(admin.ModelAdmin):
    
    inlines = (
        JournalArticleInlineAdmin,
        BookInlineAdmin,
        BookChapterInlineAdmin,
        ContributionInlineAdmin,
    )
    
    list_display = ('id', 'get_title')
    search_fields = ('journalarticle__title', 'book__title', 'bookchapter__title',)
    
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

    