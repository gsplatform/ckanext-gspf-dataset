import ckan.plugins as p
import ckan.plugins.toolkit as tk


class GspfDatasetPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)


    def _modify_package_schema(self, schema):
        schema.update({
            'spatial': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')]
                        })
        schema.update({
            'data_quality': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')]
                        })
        schema.update({
            'restriction': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')]
                        })
        schema.update({
            'data_created_date': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')]
                        })
        schema['resources'].update({
                'metadata_type' : [ tk.get_validator('ignore_missing') ],
                'data_crs' : [ tk.get_validator('ignore_missing') ]
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

        schema.update({
            'spatial': [ tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
                    })
        schema.update({
            'data_quality': [ tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing') ]
                    })
        schema.update({
            'restriction': [ tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
                    })
        schema.update({
            'data_created_date': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
        })
        schema['resources'].update({
                'metadata_type' : [ tk.get_validator('ignore_missing') ],
                'data_crs' : [ tk.get_validator('ignore_missing') ]
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
