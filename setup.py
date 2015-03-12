from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-gspf-dataset',
    version=version,
    description="Geospatial Platform dataset plugin",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Hal Seki',
    author_email='hal@georepublic.co.jp',
    url='http://georepublic.co.jp/',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.gspfdataset'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points='''
        [ckan.plugins]
        gspf_dataset=ckanext.gspfdataset.plugin:GspfDatasetPlugin
    ''',
)
