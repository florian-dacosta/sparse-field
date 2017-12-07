from odoo import fields
from odoo.addons.base_sparse_field.models.fields import monkey_patch
from odoo.osv.expression import expression, ExtendedLeaf


@monkey_patch(fields.Field)
def _get_attrs(self, model, name):
    attrs = _get_attrs.super(self, model, name)
    if attrs.get('sparse') and attrs.get('sparse_search'):
        attrs['search'] = self._search_sparse
    return attrs


@monkey_patch(fields.Field)
def _search_sparse(self, records, operator, value):
    return [(self.name, operator, value)]


@monkey_patch(expression)
def parse(self):
    self.stack = [ExtendedLeaf(leaf, self.root_model)
                  for leaf in self.expression]
    # process from right to left; expression is from left to right
    ##########################
    fields_unstore = []
    for leaf in self.stack:

        # Get working variables
        if leaf.is_operator():
            left, operator, right = leaf.leaf, None, None
        elif leaf.is_true_leaf() or leaf.is_false_leaf():
            # because we consider left as a string
            left, operator, right = ('%s' % leaf.leaf[0], leaf.leaf[1],
                                     leaf.leaf[2])
        else:
            left, operator, right = leaf.leaf
        path = left.split('.', 1)

        model = leaf.model
        field = model._fields.get(path[0])
        if field and hasattr(field, 'sparse') and field.sparse:
            field.store = True
            fields_unstore.append(field)

    parse.super(self)
    for field_to_unstore in fields_unstore:
        field_to_unstore.store = False


@monkey_patch(expression)
def _leaf_to_sql(self, eleaf):
    model = eleaf.model
    leaf = eleaf.leaf
    left, operator, right = leaf
    table_alias = '"%s"' % (eleaf.generate_alias())
    query, params = _leaf_to_sql.super(self, eleaf)
    if hasattr(model._fields[left], 'sparse') and model._fields[left].sparse:
        replaced_str = '%s."%s"' % (table_alias, left)
        replacing_str = "%s.%s ->> '%s'" % (table_alias,
                                            model._fields[left].sparse, left)
        if isinstance(right, bool):
            replacing_str = "(%s.%s ->> '%s')::boolean" % (
                table_alias, model._fields[left].sparse, left)
        query = query.replace(replaced_str, replacing_str)
        params = ['%s' % p for p in params]
    return query, params
