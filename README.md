# Geospatial Platform Dataset plugin

## Requirements

* Tested against **CKAN 2.2.1**
* Requires **ckanext-spatial* Plugin

## Installation

The installation has the following steps, assuming you have a running copy of CKAN:

* Install the extension from git repository

```
git clone git@github.com:gsplatform/ckanext-gspf-dataset.git
```

## Configuration

```
(pyenv)$ python setup.py develop
```

Then add gspf_dataset to plugin setting

```
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
```

## License

This extension is open and licensed under the GNU Affero General Public License (AGPL) v3.0 whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
