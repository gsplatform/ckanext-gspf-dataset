import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.lib.plugins import DefaultOrganizationForm
import ckan.lib.base as base
from routes.mapper import SubMapper
from logging import getLogger
from ckan.common import _, c, request, response

class GspfDatasetPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    #IRoutes
    def before_map(self, map):
        map.connect('crs', '/{text}/autocomplete/crs', controller='ckanext.gspfdataset.plugin:GspfDatasetUtilController', action='crs_json')
        return map

    def _modify_package_schema(self, schema):
        default_validator = [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')]
        schema.update({
            '__before': [self.thumb_converter],
            'spatial': default_validator,
            'quality': default_validator,
            'restriction': default_validator,
            'created_date': default_validator,
            'charge': default_validator,
            'emergency': default_validator,
            'area': default_validator,
            'thumbnail_url': default_validator,
            'fee': default_validator,
            'license_agreement': default_validator
        })
        schema['resources'].update({
                'metadata_type' : [ tk.get_validator('ignore_missing') ],
                'data_crs' : [ tk.get_validator('ignore_missing') ],
                'acknowledgement' : [ tk.get_validator('ignore_missing') ],
                'tos' : [ tk.get_validator('ignore_missing') ],
                'selection_type' : [ tk.get_validator('ignore_missing') ]
                })
        return schema

    def create_package_schema(self):
        schema = super(GspfDatasetPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(GspfDatasetPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(GspfDatasetPlugin, self).show_package_schema()
        default_validator = [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')]
        schema.update({
            '__before': [self.thumb_converter],
            'spatial': default_validator,
            'quality': default_validator,
            'restriction': default_validator,
            'created_date': default_validator,
            'charge': default_validator,
            'emergency': default_validator,
            'area': default_validator,
            'thumbnail_url': default_validator,
            'fee': default_validator,
            'license_agreement': default_validator
        })

        schema['resources'].update({
                'metadata_type' : [ tk.get_validator('ignore_missing') ],
                'data_crs' : [ tk.get_validator('ignore_missing') ],
                'acknowledgement' : [ tk.get_validator('ignore_missing') ],
                'tos' : [ tk.get_validator('ignore_missing') ],
                'selection_type' : [ tk.get_validator('ignore_missing') ]
                })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        tk.add_public_directory(config, 'public')

    def thumb_converter(self, key, flattened_data, errors, context):
        return True


class GspfOrganizationPlugin(p.SingletonPlugin, DefaultOrganizationForm):
    p.implements(p.IGroupForm, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    #IRoutes
    def before_map(self, map):
        org_controller = 'ckan.controllers.organization:OrganizationController'
        with SubMapper(map, controller=org_controller) as m:
            m.connect('organization_activity', '/organization/activity/{id}/{offset}',
            action='activity', ckan_icon='time')
        map.connect('crs', '/autocomplete/crs', controller='ckanext.gspfdataset.GspfDatasetPlugin', action='crs_json')
        return map


    #IGroupForm
    def is_fallback(self):
        return False

    def group_types(self):
        return ['organization']

    def form_to_db_schema(self):
        default_validator = [p.toolkit.get_validator('ignore_missing'), p.toolkit.get_converter('convert_to_extras')]
        schema = super(GspfOrganizationPlugin, self).form_to_db_schema()
        schema.update({
            'department': default_validator,
            'contact': default_validator,
            'address': default_validator,
            'phone': default_validator,
            'mail': default_validator,
            'type': default_validator
        })
        return schema

class GspfDatasetUtilController(base.BaseController):
    def crs_json(self):
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return base.render('package/crs.json') 
