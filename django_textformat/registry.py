class InvalidTextFilter(Exception):
    pass


class FilterRegistry(object):
    def __init__(self):
        self.text_filters = {}

    def register(self, name=None, filter_func=None, **flags):
        if name is None and filter_func is None:
            # @register.text_filter()
            def dec(func):
                return self._register_function(func, **flags)
            return dec

        elif name is not None and filter_func is None:
            if callable(name):
                # @register.text_filter
                return self._register_function(name, **flags)
            else:
                # @register.text_filter('name') or @register.text_filter(name='name')
                def dec(func):
                    return self.register(name, func, **flags)
                return dec

        elif name is not None and filter_func is not None:
            # @register.text_filter('name', function)
            self.text_filters[name] = filter_func
            filter_func._filter_name = name
            return filter_func

        else:
            # something wrong...
            raise InvalidTextFilter("Unsupported filter!")

    def _register_function(self, func, **flags):
        name = getattr(func, "_decorated_function", func).__name__
        return self.register(name, func, **flags)

    def autoload(self):
        from .utils import autoload_filters
        autoload_filters()

    def apply(self, name, text):
        if not name in self.text_filters:
            raise InvalidTextFilter("Unsupported filter!")
        return self.text_filters[name](text)

    def get_filter_choices(self):
        return [(f, f) for f in registry.text_filters]


registry = FilterRegistry()
