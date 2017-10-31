from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    data = fields.Serialized()
    test_integer = fields.Integer(sparse='data', allow_search=True)
    test_char = fields.Char(sparse='data', allow_search=True)
    test_text = fields.Text(sparse='data', allow_search=True)
    test_float = fields.Float(sparse='data', allow_search=True)
    test_many2one = fields.Many2one('product.product', sparse='data', allow_search=True)
    test_many2many = fields.Many2many('product.product', sparse='data', allow_search=True)
    test_selection = fields.Selection(sparse='data', allow_search=True)
    test_boolean = fields.Boolean(sparse='data', allow_search=True)
