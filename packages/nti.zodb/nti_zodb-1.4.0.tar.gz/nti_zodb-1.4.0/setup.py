import codecs
from setuptools import setup
from setuptools import find_namespace_packages


TESTS_REQUIRE = [
    'nti.testing',
    'zope.testrunner',
    'coverage',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()

setup(
    name='nti.zodb',
    version='1.4.0',
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="Utilities for ZODB",
    long_description=(_read('README.rst') + '\n\n' + _read('CHANGES.rst')),
    license='Apache',
    keywords='ZODB',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Framework :: ZODB",
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/OpenNTI/nti.zodb",
    zip_safe=True,
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'nti.property', # BWC exports
        'nti.schema',
        'nti.wref',
        'perfmetrics',
        'persistent',
        'repoze.zodbconn',
        'zc.zlibstorage',
        'ZODB',
        # BTrees is a dependency of ZODB, but we use it directly here,
        # and want to make sure we have a decent version.
        'BTrees >= 4.7.2',
        # ZConfig is also a ZODB dep that we use directly here.
        'ZConfig',
        'zope.component',
        'zope.copy',
        'zope.copypastemove',
        'zope.deprecation',
        'zope.interface',
        'zope.minmax',
        'zope.processlifetime',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ]
    },
    python_requires=">=3.10",
)
