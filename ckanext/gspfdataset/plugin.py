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
        return '''
{"ResultSet": {"Result": [
{"Format":"EPSG:4612: JGD2000"},
{"Format":"EPSG:4326: WGS 84"},
{"Format":"EPSG:4301: Tokyo"},
{"Format":"EPSG:3097: JGD2000 / UTM zone 51N"},
{"Format":"EPSG:3098: JGD2000 / UTM zone 52N"},
{"Format":"EPSG:3099: JGD2000 / UTM zone 53N"},
{"Format":"EPSG:3100: JGD2000 / UTM zone 54N"},
{"Format":"EPSG:3101: JGD2000 / UTM zone 55N"},
{"Format":"EPSG:32651: WGS 84 / UTM zone 51N"},
{"Format":"EPSG:32652: WGS 84 / UTM zone 52N"},
{"Format":"EPSG:32653: WGS 84 / UTM zone 53N"},
{"Format":"EPSG:32654: WGS 84 / UTM zone 54N"},
{"Format":"EPSG:32655: WGS 84 / UTM zone 55N"},
{"Format":"EPSG:3092: Tokyo / UTM zone 51N"},
{"Format":"EPSG:3093: Tokyo / UTM zone 52N"},
{"Format":"EPSG:3094: Tokyo / UTM zone 53N"},
{"Format":"EPSG:3095: Tokyo / UTM zone 54N"},
{"Format":"EPSG:3096: Tokyo / UTM zone 55N"},
{"Format":"EPSG:2443: JGD2000 / Japan Plane Rectangular CS I"},
{"Format":"EPSG:2444: JGD2000 / Japan Plane Rectangular CS II"},
{"Format":"EPSG:2445: JGD2000 / Japan Plane Rectangular CS III"},
{"Format":"EPSG:2446: JGD2000 / Japan Plane Rectangular CS IV"},
{"Format":"EPSG:2447: JGD2000 / Japan Plane Rectangular CS V"},
{"Format":"EPSG:2448: JGD2000 / Japan Plane Rectangular CS VI"},
{"Format":"EPSG:2449: JGD2000 / Japan Plane Rectangular CS VII"},
{"Format":"EPSG:2450: JGD2000 / Japan Plane Rectangular CS VIII"},
{"Format":"EPSG:2451: JGD2000 / Japan Plane Rectangular CS IX"},
{"Format":"EPSG:2452: JGD2000 / Japan Plane Rectangular CS X"},
{"Format":"EPSG:2453: JGD2000 / Japan Plane Rectangular CS XI"},
{"Format":"EPSG:2454: JGD2000 / Japan Plane Rectangular CS XII"},
{"Format":"EPSG:2455: JGD2000 / Japan Plane Rectangular CS XIII"},
{"Format":"EPSG:2456: JGD2000 / Japan Plane Rectangular CS XIV"},
{"Format":"EPSG:2457: JGD2000 / Japan Plane Rectangular CS XV"},
{"Format":"EPSG:2458: JGD2000 / Japan Plane Rectangular CS XVI"},
{"Format":"EPSG:2459: JGD2000 / Japan Plane Rectangular CS XVII"},
{"Format":"EPSG:2460: JGD2000 / Japan Plane Rectangular CS XVIII"},
{"Format":"EPSG:2461: JGD2000 / Japan Plane Rectangular CS XIX"},
{"Format":"EPSG:30161: Tokyo / Japan Plane Rectangular CS I"},
{"Format":"EPSG:30162: Tokyo / Japan Plane Rectangular CS II"},
{"Format":"EPSG:30163: Tokyo / Japan Plane Rectangular CS III"},
{"Format":"EPSG:30164: Tokyo / Japan Plane Rectangular CS IV"},
{"Format":"EPSG:30165: Tokyo / Japan Plane Rectangular CS V"},
{"Format":"EPSG:30166: Tokyo / Japan Plane Rectangular CS VI"},
{"Format":"EPSG:30167: Tokyo / Japan Plane Rectangular CS VII"},
{"Format":"EPSG:30168: Tokyo / Japan Plane Rectangular CS VIII"},
{"Format":"EPSG:30169: Tokyo / Japan Plane Rectangular CS IX"},
{"Format":"EPSG:30170: Tokyo / Japan Plane Rectangular CS X"},
{"Format":"EPSG:30171: Tokyo / Japan Plane Rectangular CS XI"},
{"Format":"EPSG:30172: Tokyo / Japan Plane Rectangular CS XII"},
{"Format":"EPSG:30173: Tokyo / Japan Plane Rectangular CS XIII"},
{"Format":"EPSG:30174: Tokyo / Japan Plane Rectangular CS XIV"},
{"Format":"EPSG:30175: Tokyo / Japan Plane Rectangular CS XV"},
{"Format":"EPSG:30176: Tokyo / Japan Plane Rectangular CS XVI"},
{"Format":"EPSG:30177: Tokyo / Japan Plane Rectangular CS XVII"},
{"Format":"EPSG:30178: Tokyo / Japan Plane Rectangular CS XVIII"},
{"Format":"EPSG:30179: Tokyo / Japan Plane Rectangular CS XIX"}
]}}'''
