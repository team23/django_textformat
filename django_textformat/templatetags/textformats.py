from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def apply_filter(value, filter_name):
    from ..registry import registry, InvalidTextFilter
    try:
        return registry.apply(filter_name, value)
    except InvalidTextFilter:
        return u''


@register.filter
@stringfilter
def apply_format(value, format):
    from ..models import TextFormat
    if isinstance(format, basestring):
        try:
            format = TextFormat.objects.get(slug=format)
        except TextFormat.DoesNotExist:
            return u''
    return format.apply(value)

