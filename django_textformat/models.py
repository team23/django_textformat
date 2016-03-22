# coding: utf-8
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.lru_cache import lru_cache

from .registry import registry


class TextFormat(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u'Name'))
    slug = models.SlugField(unique=True, verbose_name=_(u'Machine Name'))

    def __unicode__(self):
        return self.name

    @lru_cache()
    def get_filters(self):
        return self.filters.order_by('sort')

    def apply(self, text):
        for filter in self.get_filters():
            text = filter.apply(text)
        return mark_safe(text)  # A format is considered safe, while one filter will not be considered safe


class TextFilter(models.Model):
    # create choice field with text filter from registered filters from library
    # TODO: Make this more rubust and dynamic (other aps should be able to extend the filters after initial loading)
    FILTER_CHOICES = registry.get_filter_choices()

    format = models.ForeignKey(TextFormat, related_name='filters')
    sort = models.SmallIntegerField(verbose_name=_(u'Sort'))
    name = models.CharField(choices=FILTER_CHOICES, max_length=50, verbose_name=_(u'Select Filter'))

    def __unicode__(self):
        return self.name

    def apply(self, text):
        return registry.apply(self.name, text)
