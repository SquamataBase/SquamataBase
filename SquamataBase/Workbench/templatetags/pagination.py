from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

DOT = '.'

@register.simple_tag
def paginator_number(cl, i, query):
    if cl.paginator.num_pages == 1:
        return '';
    if i == DOT:
        return format_html('<li class="page-item"><a class="page-link disabled">...</a></li> ')
    elif i == cl.number-1:
        return format_html('<li class="page-item active"><a class="page-link">{} <span class="sr-only">(current)</span></a></li> ', i+1);
    else:
        return format_html('<li class="page-item"><a class="page-link" href="?taxon={}&page={}">{}</a></li> ',
                           query,
                           i+1,
                           i+1);
                                

@register.inclusion_tag('site/pagination.html')
def pagination(cl, query):
    paginator, page_num = cl.paginator, cl.number-1;
    
    ON_EACH_SIDE = 3;
    ON_ENDS = 2;

    # If there are 10 or fewer pages, display links to every page.
    # Otherwise, do some fancy
    if paginator.num_pages <= 10:
        page_range = range(paginator.num_pages);
    else:
        # Insert "smart" pagination links, so that there are always ON_ENDS
        # links at either end of the list of pages, and there are always
        # ON_EACH_SIDE links at either end of the "current page" link.
        page_range = [];
        if page_num > (ON_EACH_SIDE + ON_ENDS):
            page_range.extend(range(0, ON_ENDS));
            page_range.append(DOT);
            page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1));
        else:
            page_range.extend(range(0, page_num + 1));
        if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
            page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1));
            page_range.append(DOT);
            page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages));
        else:
            page_range.extend(range(page_num + 1, paginator.num_pages));

    return { 'cl' : cl, 'page_range' : page_range, 'query' : query}; 
