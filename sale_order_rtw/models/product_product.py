# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_in_tax_excluded_group = fields.Boolean(
        string='In Tax Excluded Group',
        compute='_compute_is_in_tax_excluded_group',
        store=False,
        help='Check if product is in GC001 (税抜定価除外) group'
    )

    @api.depends('product_tmpl_id')
    def _compute_is_in_tax_excluded_group(self):
        for product in self:
            product.is_in_tax_excluded_group = self._check_in_group('GC001')

    def _check_in_group(self, group_code):
        self.ensure_one()
        domain = [('group_code', '=', group_code), ('product_template_id', '=', self.product_tmpl_id.id)]
        group_master = self.env['product.group.master'].search(domain, limit=1)
        
        return bool(group_master)
    
    def is_tax_excluded_price_product(self):
        return self._check_in_group('GC001')
