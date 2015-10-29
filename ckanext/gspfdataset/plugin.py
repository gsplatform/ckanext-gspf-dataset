# -*- coding: utf-8 -*-

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.lib.plugins import DefaultOrganizationForm
import ckan.lib.base as base
from routes.mapper import SubMapper
from logging import getLogger
from ckan.common import _, c, request, response
import ckan.model as model
import ckan.logic as logic
import ckan.lib.plugins
from pylons import config
lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
get_action = logic.get_action
import ckan.lib.datapreview as datapreview
render = base.render

class GspfDatasetPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    #IRoutes
    def before_map(self, map):
        map.connect('crs', '/{text}/autocomplete/crs', controller='ckanext.gspfdataset.plugin:GspfDatasetUtilController', action='crs_json')
        map.connect('resource_agreement', '/dataset/{id}/resource/{resource_id}/agree/', controller='ckanext.gspfdataset.plugin:GspfResourceController', action='agreement')
        return map

    def _modify_package_schema(self, schema):
        default_validator = [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')]
        schema.update({
            'spatial': default_validator,
            'quality': default_validator,
            'restriction': default_validator,
            'registerd_date': default_validator,
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
                'thumbnail_url' : [ tk.get_validator('ignore_missing') ],
                'standard_price' : [ tk.get_validator('ignore_missing') ],
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
            'spatial': default_validator,
            'quality': default_validator,
            'restriction': default_validator,
            'registerd_date': default_validator,
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
                'thumbnail_url' : [ tk.get_validator('ignore_missing') ],
                'standard_price' : [ tk.get_validator('ignore_missing') ],
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
        tk.add_resource('fantastic', 'gspfdataset')


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

class GspfResourceController(base.BaseController):
    def _resource_template(self, package_type):
        # backwards compatibility with plugins not inheriting from
        # DefaultDatasetPlugin and not implmenting resource_template
        plugin = lookup_package_plugin(package_type)
        if hasattr(plugin, 'resource_template'):
            result = plugin.resource_template()
            if result is not None:
                return result
        return lookup_package_plugin().resource_template()

    def _resource_preview(self, data_dict):
        '''Deprecated in 2.3'''
        return bool(datapreview.get_preview_plugin(data_dict, return_first=True))

    def agreement(self, id, resource_id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj, "for_view":True}

        try:
            c.package = get_action('package_show')(context, {'id': id})
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read dataset %s') % id)

        for resource in c.package.get('resources', []):
            if resource['id'] == resource_id:
                c.resource = resource
                break
        if not c.resource:
            abort(404, _('Resource not found'))

        c.agreement = None
        # detect whether dataset has 利用規約
        for resource in c.package.get('resources', []):
            if resource['name'] == u'利用規約':
                c.agreement = resource
                break

        # required for nav menu
        c.pkg = context['package']
        c.pkg_dict = c.package
        dataset_type = c.pkg.type or 'dataset'

        # get package license info
        license_id = c.package.get('license_id')
        try:
            c.package['isopen'] = model.Package.\
                get_license_register()[license_id].isopen()
        except KeyError:
            c.package['isopen'] = False

        # TODO: find a nicer way of doing this
        c.datastore_api = '%s/api/action' % config.get('ckan.site_url', '').rstrip('/')

        c.related_count = c.pkg.related_count

        c.agreement['can_be_previewed'] = self._resource_preview(
            {'resource': c.agreement, 'package': c.package})

        resource_views = get_action('resource_view_list')(
            context, {'id': c.agreement['id']})
        c.agreement['has_views'] = len(resource_views) > 0

        current_resource_view = None
        view_id = request.GET.get('view_id')
        if c.agreement['can_be_previewed'] and not view_id:
            current_resource_view = None
        elif c.agreement['has_views']:
            if view_id:
                current_resource_view = [rv for rv in resource_views
                                         if rv['id'] == view_id]
                if len(current_resource_view) == 1:
                    current_resource_view = current_resource_view[0]
                else:
                    abort(404, _('Resource view not found'))
            else:
                current_resource_view = resource_views[0]

        vars = {'resource_views': resource_views,
                'current_resource_view': current_resource_view,
                'dataset_type': dataset_type}

        template = self._resource_template(dataset_type)
        #return render(template, extra_vars=vars)
        return render('package/resource_agree.html', extra_vars=vars) 
