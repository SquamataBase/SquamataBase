from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from SquamataBase.Bibliography.models import *

register = template.Library()

@register.inclusion_tag('site/bibliography.html')
def bibliography(ref):
    authors = Contribution.objects.order_by('id').filter(ref=ref).select_related('person')
    if ref.ref_type.term == 'journal_article':
        item = JournalArticle.objects.get(ref=ref)
    elif ref.ref_type.term == 'book_chapter':
        item = BookChapter.objects.get(ref=ref)
    elif ref.ref_type.term == 'book':
        item = Book.objects.get(ref=ref)
    else:
        item = None
    authorstr = format_html("<p>{}", " ".join([authors[0].person.first_name, authors[0].person.last_name]))
    for a in range(1, len(authors)):
        authorstr = format_html("{}<br>{}", mark_safe(authorstr), " ".join([authors[a].person.first_name, authors[a].person.last_name]))
    authorstr = format_html("{}</p>", mark_safe(authorstr))
        
    return {'authorstr': authorstr,
            'authors': authors,
            'ref': ref,
            'details': item}