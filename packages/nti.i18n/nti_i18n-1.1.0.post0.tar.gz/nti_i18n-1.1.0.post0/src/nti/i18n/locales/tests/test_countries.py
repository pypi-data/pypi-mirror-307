#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for locale data.
"""

__docformat__ = "restructuredtext en"

import unittest

from zope.component.testlayer import ZCMLFileLayer
from zope import component

import nti.i18n.locales
from nti.i18n.locales.interfaces import ICountryAvailability

from . import skipIfNoPlone


class TestConfiguredCountryUtility(unittest.TestCase):

    layer = ZCMLFileLayer(nti.i18n.locales, zcml_file='configure.zcml')

    def test_country_availability(self):
        availability = component.getUtility(ICountryAvailability)
        self.assertIn('us', availability.getAvailableCountries())
        self.assertIn("us", availability.getCountries())
        self.assertIn('us', [x[0] for x in availability.getCountryListing()] )

        self.assertIsInstance(
            availability.getCountries()['us']['name'],
            str)

    @skipIfNoPlone
    def test_lookup_utility_with_plone_iface(self):
        # pylint:disable=import-error
        from plone.i18n.locales.interfaces import ICountryAvailability as IPlone
        from nti.i18n.locales.countries import CountryAvailability
        utility = component.getUtility(IPlone)
        self.assertIsInstance(utility, CountryAvailability)
