from odoo import models, fields


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    sparse_search = fields.Boolean()

    def _reflect_field_params(self, field):
        params = super(IrModelFields, self)._reflect_field_params(field)
        params['sparse_search'] = False
        if getattr(field, 'sparse', None) and \
                getattr(field, 'sparse_search', None):
            params['sparse_search'] = True
        return params

    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelFields, self)._instanciate_attrs(field_data)
        if field_data.get('serialization_field_id') and \
                field_data.get('sparse_search'):
            attrs['sparse_search'] = True
        return attrs


class TestSparse(models.TransientModel):
    _inherit = 'sparse_fields.test'

    data = fields.Serialized()
    boolean = fields.Boolean(sparse='data', sparse_search=True)
    integer = fields.Integer(sparse='data', sparse_search=True)
    float = fields.Float(sparse='data', sparse_search=True)
    char = fields.Char(sparse='data', sparse_search=True)
    selection = fields.Selection(
        [('one', 'One'), ('two', 'Two')], sparse='data', sparse_search=True)
    partner = fields.Many2one(
        'res.partner', sparse='data', sparse_search=True)
