#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for locale data.
"""
__docformat__ = "restructuredtext en"

import unittest

from zope.component.testlayer import ZCMLFileLayer
from zope import component

import nti.i18n
from nti.i18n.locales.interfaces import ICcTLDInformation

from . import skipIfNoPlone

class TestConfiguredTLDUtility(unittest.TestCase):

    layer = ZCMLFileLayer(nti.i18n, zcml_file='configure.zcml')

    def test_full_domain_list(self):
        info = component.getUtility(ICcTLDInformation)
        available = info.getAvailableTLDs()
        with_lang = info.getTLDs()
        for cc in available:
            self.assertIn(cc, with_lang)

        self.assertEqual(["en"], info.getLanguagesForTLD('us'))
        self.assertIsInstance(info.getLanguagesForTLD('us')[0], str)

        # Bad tlds
        self.assertRaises(KeyError, info.getLanguagesForTLD, __name__)

    @skipIfNoPlone
    def test_lookup_utility_with_plone_iface(self):
        # pylint:disable=import-error
        from plone.i18n.locales.interfaces import ICcTLDInformation as IPlone
        from nti.i18n.locales.cctld import CcTLDInformation
        utility = component.getUtility(IPlone)
        self.assertIsInstance(utility, CcTLDInformation)
