# -*- coding: utf-8 -*-

from odoo.tests import common


class TestSparseFieldsSearch(common.TransactionCase):

    def test_sparse(self):
        """ test sparse fields. """
        sparse_test_obj = self.env['sparse_fields.test']
        record = sparse_test_obj.create({})

        partner = self.env.ref('base.main_partner')
        values = [
            ('boolean', True),
            ('integer', 42),
            ('float', 3.14),
            ('char', 'John'),
            ('selection', 'two'),
            ('partner', partner.id),
        ]
        for n, (key, val) in enumerate(values):
            record.write({key: val})
            search_res = sparse_test_obj.search(
                [(key, '=', val)])
            self.assertEqual(len(search_res), 1)

        for n, (key, val) in enumerate(values):
            record.write({key: False})
            search_res = sparse_test_obj.search(
                [(key, '=', val)])
            self.assertEqual(len(search_res), 0)
