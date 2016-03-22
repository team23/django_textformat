def autoload_filters():
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            import_module('%s.text_filters' % app)
        except:
            if module_has_submodule(mod, 'text_filters'):
                raise
