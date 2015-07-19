# encoding: utf-8
from django import template
from django.http import QueryDict

from .. import utils


register = template.Library()


@register.filter
def verbose_name(obj):
    """
    Returns the verbose name for a Django Model instance.
    """
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    """
    Returns the plural verbose name for a Django Model instance.
    """
    return obj._meta.verbose_name_plural


@register.inclusion_tag(
    'utensils/_order_by_controls.html', takes_context=True)
def order_by(context, field_name):
    return {
        'field_name': field_name,
        'sort_col': context['sort-col'],
        'request': context['request'],
        'sort_dir': context['sort-dir'],
        'page_obj': context.get('page_obj', ''),
        'paginator': context.get('paginator', ''),
    }


@register.inclusion_tag(
    'utensils/_pagination_controls.html', takes_context=True)
def pagination(context, adjacent_pages=2):
    current_page = context['page_obj'].number
    total_pages = context['paginator'].num_pages

    startPage = max(current_page - adjacent_pages, 1)
    if startPage <= 3:
        startPage = 1

    endPage = current_page + adjacent_pages + 1
    if endPage >= total_pages - 1:
        endPage = total_pages + 1

    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= total_pages]

    return {
        'object_model': context['view'].model,
        'page_obj': context['page_obj'],
        'paginator': context['paginator'],
        'request': context['request'],
        'sort_col': context.get('sort-col', ''),
        'sort_dir': context.get('sort-dir', ''),
        'pagination_page_sizes': context['pagination_page_sizes'],
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': total_pages not in page_numbers,
    }


class FilterQuery(template.Node):
    def __init__(self, varlist):
        self.varlist = varlist
        self.request = template.Variable('request')

    def render(self, context):
        req = self.request.resolve(context).GET.dict()
        params = QueryDict('', mutable=True)
        for k in self.varlist.keys():
            try:
                v = self.varlist[k].resolve(context)
                if v:
                    req.update({k: v})
            except:
                pass
        params.update(req)
        return '?' + params.urlencode()


def pairwise(varlist):
    l = iter(varlist)
    return zip(l, l)


@register.tag
def filter_query(parser, token):
    nlist = token.split_contents()
    nlist.pop(0)
    varlist = {}
    for k,v in pairwise(nlist):
        varlist[k[1:-1]] = template.Variable(v)
    return FilterQuery(varlist)


class NextParamNode(template.Node):
    def __init__(self):
        self.request = template.Variable('request')

    def render(self, context):
        request = self.request.resolve(context)
        return "next={}".format(request.get_full_path())


@register.tag
def next_param(parser, token):
    return NextParamNode()


@register.filter
def strip_query_string(url):
    return utils.remove_query_string(url)


class GetNextNode(template.Node):
    def __init__(self, var_name=None):
        self.request = template.Variable('request')
        self.var_name = var_name

    def render(self, context):
        request = self.request.resolve(context)
        next = request.GET.get('next')

        # Either return the next param or store in a variable.
        if self.var_name:
            context[self.var_name] = next
            return ''
        return next


@register.tag
def get_next(parser, token):
    parts = token.split_contents()
    if len(parts) not in [1, 3]:
        raise template.TemplateSyntaxError(
            "{} tag requires exactly one or three arguments".format(
            token.contents.split()[0]))
    if len(parts) == 3:
        var_name = parts[2]
    else:
        var_name = None
    return GetNextNode(var_name=var_name)


@register.filter
def seconds_to_hms(seconds):
    """
    Return string 'hh:mm:ss' or 'mm:ss'.
    """
    if not seconds:
        return '0'

    h = seconds / 3600
    s = seconds - 3600 * h
    m = s / 60
    s = s - 60 * m

    if not h:
        return "%02d:%02d" % (m, s)
    return "%02d:%02d:%02d" % (h, m, s)
