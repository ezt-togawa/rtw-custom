# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductGroupMaster(models.Model):
    _name = 'product.group.master'
    _description = 'プロダクトグループ'
    _order = 'group_code, id'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )
    
    group_id = fields.Selection(
        [('tax_excluded_price', '税抜定価除外')],
        string='グループ',
        required=True,
        default='tax_excluded_price',
        help='Group type for products'
    )
    
    group_name = fields.Char(
        string='グループ名',
        compute='_compute_group_name',
        store=True,
        help='Group name for searching'
    )
    
    group_code = fields.Char(
        string='グループコード',
        compute='_compute_group_code',
        store=True,
        help='Group code for internal logic processing'
    )
    
    product_template_id = fields.Many2one(
        'product.template',
        string='プロダクト',
        required=True,
        help='Product template in this group (applies to all variants)'
    )
    
    @api.depends('group_id', 'product_template_id')
    def _compute_name(self):
        for record in self:
            group_name = dict(record._fields['group_id'].selection).get(record.group_id, '')
            product_name = record.product_template_id.name if record.product_template_id else ''
            record.name = f"{group_name} - {product_name}"
    
    @api.depends('group_id')
    def _compute_group_name(self):
        for record in self:
            record.group_name = dict(record._fields['group_id'].selection).get(record.group_id, '')
    
    @api.depends('group_id')
    def _compute_group_code(self):
        group_code_mapping = {
            'tax_excluded_price': 'GC001',
        }
        for record in self:
            record.group_code = group_code_mapping.get(record.group_id, '')
    
    def name_get(self):
        result = []
        for record in self:
            group_name = dict(record._fields['group_id'].selection).get(record.group_id, '')
            product_name = record.product_template_id.name if record.product_template_id else ''
            name = f"{group_name} - {record.group_code} - {product_name}"
            result.append((record.id, name))
        return result
