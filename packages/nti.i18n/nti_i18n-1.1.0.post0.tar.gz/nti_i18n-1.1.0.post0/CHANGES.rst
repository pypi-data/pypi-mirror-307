=========
 Changes
=========


1.1.0.post0 (2024-11-08)
========================

- Nothing changed yet.


1.1.0 (2024-11-06)
==================

- Drop support for Python < 3.10.
- Add support for Python versions up to 3.13, the current version.
- Use native namespace packages.
- Make ``plone.i18n`` an optional dependency with the ``plone`` extra.
- Update included data files (TLDs and languages) to the current versions.


1.0.0 (2017-07-06)
==================

- Initial PyPI release. This implements a subset of the ``plone.i18n``
  APIs (not including flag resources) but with updated data and
  reduced dependencies.

- Python 3 and PyPy compatibility.

- Data live in external files so that they are hopefully easier to update.
