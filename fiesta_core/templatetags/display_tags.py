from django import template

register = template.Library()
from django.core.urlresolvers import reverse
from fiesta_core.defaults import FIESTA_NEWSLINE_ENTITY_SLUGTYPES


def get_parameters(parser, token):
    """
    {% get_parameters except_field %}
    """

    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "get_parameters tag takes at least 1 argument")
    return GetParametersNode(args[1].strip())

@register.simple_tag
def navactive(request, url, id):
    if id != '':
        if request.path == reverse(url, args=[id]) or (id in FIESTA_NEWSLINE_ENTITY_SLUGTYPES and request.path == reverse(url, args=[FIESTA_NEWSLINE_ENTITY_SLUGTYPES[id]])):
            return "current"
        elif request.path.startswith(reverse(url, args=[id])) or (id in FIESTA_NEWSLINE_ENTITY_SLUGTYPES and request.path.startswith(reverse(url, args=[FIESTA_NEWSLINE_ENTITY_SLUGTYPES[id]]))):
            return "current"
    else:
        if request.path == reverse(url):
            return "current"
    return ""
@register.simple_tag
def subnavactive(request, url, id, actualize):
    if id != '' and actualize != '':
        if request.path == reverse(url, args=[id, actualize]) or (id in FIESTA_NEWSLINE_ENTITY_SLUGTYPES and request.path == reverse(url, args=[FIESTA_NEWSLINE_ENTITY_SLUGTYPES[id], actualize])):
            return "current"
    else:
        if request.path == reverse(url):
            return "current"
    return ""
@register.filter(name='start_with')
def start_with(str, sub_str):
    return str.startswith(sub_str)

@register.filter(name='paging_slice')
def paging_slice(p):
    first = p.number - 5;
    last = p.number + 5;
    first = None if first <= 0 else first
    last = last if  p.paginator.num_pages > last else None
    l = p.paginator.page_range[first:last]
    return p.paginator.page_range[first:last]


class GetParametersNode(template.Node):
    """
    Renders current get parameters except for the specified parameter
    """
    def __init__(self, field):
        self.field = field

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()

        if self.field in getvars:
            del getvars[self.field]

        if len(getvars.keys()) > 0:
            get_params = "%s&" % getvars.urlencode()
        else:
            get_params = ''

        return get_params

get_parameters = register.tag(get_parameters)
