Geospatial Platform Dataset plugin
===========

* `Installation`_
* `Configuration`_

Installation
------------

**This plugin dependencies ckanext-spatial Plugin.**

The current version of ckanext-basemaps has been developed and tested again
**CKAN 2.2.1**. We assume a running CKAN 2.2.1 instance.

The installation has the following steps, assuming you have a running
copy of CKAN:

#. Install the extension from git repository

    $ git clone git@github.com:gsplatform/ckanext-gspf-dataset.git


    Configuration
    -------------
    (pyenv)$ python setup.py develop

    Then add gspf_dataset to plugin setting

    ckan.plugins = text_preview
                   recline_preview
                   pdf_preview
                   spatial_metadata
                   spatial_query
                   resource_proxy
                   geojson_preview
                   mapbases_layer
                   datesearch
                   gspf_theme
                   gspf_dataset



