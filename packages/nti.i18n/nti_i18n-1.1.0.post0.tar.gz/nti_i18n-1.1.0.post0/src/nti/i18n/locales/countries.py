# -*- coding: utf-8 -*-
"""
Implementation of country data.

"""

__docformat__ = "restructuredtext en"

import json
from types import MappingProxyType as FrozenMap
from importlib import resources

from zope.interface import implementer
from zope.cachedescriptors.property import Lazy

from .interfaces import ICountryAvailability

@implementer(ICountryAvailability)
class CountryAvailability(object):
    """
    Default implementation of country availability, based on
    countries.json distributed with this package.
    """

    @Lazy
    def _countrylist(self):
        # This is a dictionary of dictonaries:
        #
        # 'country-code' : {u'name' : 'English name', u'flag' : u'/++resource++country-flags/*.gif'}
        #
        # This list follows ISO 3166-1. In addition the following reservations are
        # part of the list for historical reasons: an.
        # It was initially based on data distributed with plone.i18n 5.0.3.
        # Prior to 3.12, you must use a package, not a module.
        country_str = resources.read_text(__name__.rsplit('.', 1)[0], 'countries.json')
        return FrozenMap({
            k: FrozenMap(v)
            for k, v
            in json.loads(country_str).items()
        })

    def getAvailableCountries(self):
        return self._countrylist.keys()

    def getCountries(self):
        return self._countrylist.copy()

    def getCountryListing(self):
        return [(code, data['name']) for code, data in self._countrylist.items()]
