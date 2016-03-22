from django.db import models
from django.db.models.fields import related
from django.utils.lru_cache import lru_cache


@lru_cache()
def get_text_format(pk):
    from .models import TextFormat
    return TextFormat.objects.get(pk=pk)


class TextFormatRelatedObjectDescriptor(related.ReverseSingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        if not hasattr(instance, self.cache_name):
            format_id = getattr(instance, self.field.attname)
            text_format = get_text_format(format_id)
            setattr(instance, self.cache_name, text_format)
        return super(TextFormatRelatedObjectDescriptor, self).__get__(instance, instance_type)


class TextFormatField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        if args:
            kwargs['verbose_name'] = args[0]
            args = args[1:]
        kwargs.setdefault('to', 'django_textformat.TextFormat')
        kwargs.setdefault('on_delete', models.PROTECT)
        kwargs.setdefault('related_name', '+')
        kwargs.setdefault('default', 1)
        super(TextFormatField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(related.ForeignObject, self).contribute_to_class(cls, name, virtual_only=virtual_only)
        setattr(cls, self.name, TextFormatRelatedObjectDescriptor(self))
