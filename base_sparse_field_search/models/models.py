from odoo import models, fields, api


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    allow_search = fields.Boolean()

    def _reflect_field_params(self, field):
        params = super(IrModelFields, self)._reflect_field_params(field)
        params['allow_search'] = False
        if getattr(field, 'sparse', None) and getattr(field, 'allow_search', None):
            params['allow_search'] = True
        return params

    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelFields, self)._instanciate_attrs(field_data)
        if field_data.get('serialization_field_id') and field_data.get('allow_search'):
            attrs['allow_search'] = True
        return attrs
