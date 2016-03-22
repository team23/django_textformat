from django.test import TestCase
from .models import TextFormat, TextFilter


class FilterTestCase(TestCase):
    def test_defaultfilters(self):
        self.assertEqual(
            u'<p>test</p>',
            TextFilter(name='linebreaks_and_paragraphs').apply(u'test')
        )
        self.assertEqual(
            u'&lt;p&gt;test&lt;/p&gt;',
            TextFilter(name='html_escape').apply(u'<p>test</p>')
        )

