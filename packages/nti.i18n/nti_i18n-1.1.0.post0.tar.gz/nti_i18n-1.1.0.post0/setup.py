import codecs
from setuptools import setup
from setuptools import find_namespace_packages


TESTS_REQUIRE = [
    'zope.configuration',
    'zope.testrunner',
    'coverage',
]

def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()

setup(
    name='nti.i18n',
    version='1.1.0.post0',
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="i18n and L10n data and interfaces",
    long_description=_read('README.rst'),
    url="https://github.com/OpenNTI/nti.i18n",
    license='Apache',
    keywords='i18n l10n zope component iana data locales',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope3',
    ],
    zip_safe=True,
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'zope.component',
        'zope.interface',
        'zope.cachedescriptors',
        # plone.i18n drags in Products.CMFCore, which
        # in turn brings in a whole lot of stuff we don't want or need,
        # almost all of it legacy. Sigh.
        # 'plone.i18n',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'sphinx',
            'sphinx_rtd_theme',
            'repoze.sphinx.autointerface',
        ],
        'plone': [
            'plone.i18n',
        ]
    },
    python_requires=">= 3.10",
)
