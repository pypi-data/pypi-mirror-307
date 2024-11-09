#!/usr/bin/env python
"""
Implementation of country-code language information.

"""

__docformat__ = "restructuredtext en"

import json
from importlib import resources


from zope.interface import implementer
from zope.cachedescriptors.property import Lazy

from .interfaces import ICcTLDInformation


@implementer(ICcTLDInformation)
class CcTLDInformation(object):
    """
    A list of country code top level domains their relevant languages.

    Descriptions for most TLDs a can be found at
    http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
    """

    @Lazy
    def _domain_list(self):
        # Top level domain list taken from
        # http://data.iana.org/TLD/tlds-alpha-by-domain.txt
        # This is encoded in IDNA, but python fails to decode
        # when the prefix, XN--, is capitalized (at least in old versions).
        # That's OK, we have to
        # lower-case things anyway.
        # Prior to 3.12, you must use a package, not a module.
        tlds_bytes = resources.read_binary(__name__.rsplit('.', 1)[0], 'tlds-alpha-by-domain.txt')
        tld_strs = [
            x.lower().decode('idna')
            for x
            in tlds_bytes.splitlines()
            # In 3.12+, it refuses to parse long lines, breaking
            # on the header.
            if not x.strip().startswith(b'#')
        ]
        return tuple(tld_strs)

    @Lazy
    def _language_map(self):
        language_str = resources.read_text(__name__.rsplit('.', 1)[0], 'tlds.json')
        return json.loads(language_str)

    def getAvailableTLDs(self):
        return list(self._domain_list)

    def getTLDs(self):
        all_langs = {code: () for code in self._domain_list}
        all_langs.update(self._language_map)
        return all_langs

    def getLanguagesForTLD(self, tld):
        if tld in self._domain_list:
            return self._language_map.get(tld, ())
        raise KeyError(tld)
