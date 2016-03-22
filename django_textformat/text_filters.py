from .registry import registry


@registry.register
def urlize(value):
    from django.template.defaultfilters import urlize
    # TODO: Allow usage of urlizetrunc
    return urlize(value)


@registry.register
def html_escape(value):
    from django.template.defaultfilters import escape
    return escape(value)


@registry.register
def linebreaks_and_paragraphs(value):
    from django.template.defaultfilters import linebreaks
    return linebreaks(value)


@registry.register
def linebreaks(value):
    from django.template.defaultfilters import linebreaksbr
    return linebreaksbr(value)


@registry.register
def striptags(value):
    from django.template.defaultfilters import striptags
    return striptags(value)
