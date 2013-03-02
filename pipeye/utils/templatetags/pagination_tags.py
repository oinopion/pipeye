from django import template

register = template.Library()

BEFORE_CURRENT_PAGES = 2
AFTER_CURRENT_PAGES = 2


@register.inclusion_tag('utils/_pagination.html')
def pagination(page, url, **params):
    paginator = page.paginator
    start = max(page.number - BEFORE_CURRENT_PAGES, 1)
    end = min(page.number + AFTER_CURRENT_PAGES, paginator.num_pages)
    return {
        'url': url,
        'params': params,
        'page': page,
        'paginator': paginator,
        'page_range': range(start, end + 1),
        'show_first': start > 1,
        'show_last': end < paginator.num_pages,
    }
