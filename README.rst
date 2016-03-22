django-textformat
=================

|pypi-badge| |build-status|

.. |build-status| image:: https://travis-ci.org/team23/django_textformat.svg
    :target: https://travis-ci.org/team23/django_textformat

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django-textformat.svg
    :target: https://pypi.python.org/pypi/django-textformat

**django-textformat** makes it easy to configure and compose text formats.
A text format is simply a set of text filters that are applied in a defined
order. A text filter is a function that takes a markup string and returns a the
formatted string.

Built in filters are:

``html_escape``
    It's the same as Django's ``escape`` template filter, available as text
    filter.

``linebreaks_and_paragraphs``
    It's the same as Django's ``linebreaks`` template filter, available as text
    filter.

``linebreaks``
    It's the same as Django's ``linebreaksbr`` template filter, available as text
    filter.

``striptags``
    It's the same as Django's ``striptags`` template filter, available as text
    filter.

``urlize``
    It's the same as Django's ``urlize`` template filter, available as text
    filter.

django-textformat does not provide any text formats by default, but to give you
an idea, a text format might consist of the builtin filters ``html_escape``,
``urlize``, ``linebreaks_and_paragraphs``.

That would allow you to group those filters into a format and use it
consistently throuhgout your project.


Usage
-----

The default use case for django-textformat might look like this in your model:

.. code-block:: python

    from django.db import models
    from django_textformat import TextFormatField


    class Article(models.Model):
        title = models.CharField(max_length=50)
        content = models.TextField()
        content_format = TextFormatField()


Then you can use the selected format for the article in your template like
this:

.. code-block:: django

    {% load textformat %}

    {{ article.content|apply_format:article.content_format }}


Initially creating text formats
-------------------------------

In order to use a model like ``Article`` above, you already need to have a
``django_textformat.models.TextFormat`` instance defined. You can either create
the format by hand or use a data migration. We suggest using a data migration
which will make sure that all instances of your project (e.g. for all devs)
have the same formats available.

To do so, create an empty migration in one of your websites apps, like::

    python manage.py makemigrations blog --empty

Now make the newly created migration look something like this:

.. code-block:: python

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals

    from django.db import migrations, models


    def add_format(apps, schema_editor):
        TextFormat = apps.get_model('django_textformat', 'TextFormat')

        markdown_format = TextFormat.objects.create(
            slug='article',
            name='Article Format')
        markdown_format.filters.create(
            name='html_escape',
            sort=1)
        markdown_format.filters.create(
            name='urlize',
            sort=2)
        markdown_format.filters.create(
            name='linebreaks_and_paragraphs',
            sort=3)


    def remove_format(apps, schema_editor):
        TextFormat = apps.get_model('django_textformat', 'TextFormat')

        format = TextFormat.objects.get(slug='article')
        format.delete()


    class Migration(migrations.Migration):

        dependencies = [
            ('django_textformat', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(
                add_format,
                remove_format,
            ),
        ]


Adding custom text filters
--------------------------

It's easy to add custom text filters. In order to add one, you need a
``text_fitlers.py`` file in your app. Then add a function that takes a string
and returns the formatted string.

Here is an example:

.. code-block:: python

    # in your_app/text_filters.py

    from django_textformat.registry import registry
    import markdown


    @registry.register
    def markdown(value):
        return markdown.markdown(value, extensions=['extra'])

Now you have a text filter called ``'markdown'`` available for use in your text
formats.

Development
-----------

Install the dependencies (including the test dependencies) with::

    pip install -r requirements.txt

Then you can run all tests with::

    tox
