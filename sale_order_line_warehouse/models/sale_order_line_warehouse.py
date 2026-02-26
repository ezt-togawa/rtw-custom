# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_line_warehouse(models.Model):
     _inherit = "sale.order.line"

     warehouse_id = fields.Many2one(
         'stock.warehouse', store=True, domain="[('id' , 'in' , allowed_warehouse_ids)]"
     )

     allowed_warehouse_ids = fields.Many2many(  # THIS FIELD STORES THE APPROPRIATE WAREHOUSES
        'stock.warehouse', compute='_compute_allowed_warehouses', store=False
     )
     
     @api.onchange('warehouse_id')
     def onchange_warehouse_id(self):
        for line in self:
            product_tmpl = line.product_id.product_tmpl_id
            if not product_tmpl or not line.warehouse_id:
                continue

            result_bom_id = False
            for bom in product_tmpl.bom_ids:
                if line.warehouse_id == bom.picking_type_id.warehouse_id:
                    result_bom_id = bom
                    break
            if result_bom_id:
                line.bom_id = result_bom_id

     @api.depends('product_id')
     def _compute_allowed_warehouses(self):
        for line in self:
            if not line.product_id:
                line.allowed_warehouse_ids = [(5, 0, 0)]  # (5,0,0)は「全クリア」の意味
                continue

            warehouses = []
            for route in line.product_id.route_ids:
                for rule in route.rule_ids:
                    if rule.warehouse_id.id not in warehouses and rule.warehouse_id:
                        warehouses.append(rule.warehouse_id.id)
            line.allowed_warehouse_ids = [(6, 0, warehouses)]   # (6, 0)は入れ替えの意味
            if not line.warehouse_id and warehouses:
                line.warehouse_id = warehouses[0]

     def _prepare_add_missing_fields(self, values): # SET DEFAULT WAREHOUSE WHEN CREATE SALE ORDER LINE WITH CONFIGURE PRODUCT
        res = super(sale_order_line_warehouse, self)._prepare_add_missing_fields(values)
        if 'product_id' not in values or not values['product_id']:
            return res

        product = self.env['product.product'].browse(values['product_id'])
        if not product.exists():
            return res

        warehouse_ids = product.route_ids.mapped('rule_ids.warehouse_id').ids
        selected_wh_id = warehouse_ids[0] if warehouse_ids else False
        res['warehouse_id'] = selected_wh_id

        if selected_wh_id:
            # product.bom_ids は直接テンプレートに紐づくBOM
            bom_ids = product.bom_ids or product.product_tmpl_id.bom_ids

            result_bom_id = False
            for bom in bom_ids:
                # 倉庫ID同士で比較
                if selected_wh_id == bom.picking_type_id.warehouse_id.id:
                    result_bom_id = bom.id
                    break

            if result_bom_id:
                res['bom_id'] = result_bom_id

        return res


