from django.db.models.signals import post_save


def invalidate_cache(sender, instance, **kwargs):
    from . import modelfields
    from .models import TextFormat, TextFilter

    if issubclass(sender, TextFormat):
        modelfields.get_text_format.cache_clear()
        TextFormat.get_filters.cache_clear()
    elif issubclass(sender, TextFilter):
        TextFormat.get_filters.cache_clear()


def setup():
    from .models import TextFormat, TextFilter

    post_save.connect(invalidate_cache, sender=TextFormat)
    post_save.connect(invalidate_cache, sender=TextFilter)
