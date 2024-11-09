# Make a package

import unittest

def skipIfNoPlone(func):
    try:
        import plone.i18n # pylint:disable=unused-import
        return func
    except ModuleNotFoundError:
        return unittest.skip("plone.i18n not available")(func)
