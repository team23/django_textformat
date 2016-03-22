def test_imports():
    import django_textformat  # noqa
    from django_textformat import TextFormatField  # noqa

    assert TextFormatField is not None


def test_has_version():
    import django_textformat

    assert django_textformat.__version__.count('.') >= 2
