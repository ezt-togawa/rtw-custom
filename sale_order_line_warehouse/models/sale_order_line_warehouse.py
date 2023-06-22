# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_line_warehouse(models.Model):
     _inherit = "sale.order.line"

     warehouse_id = fields.Many2one(
         'stock.warehouse' , store=True , domain= "[('id' , 'in' , allowed_warehouse_ids)]"
     )

     allowed_warehouse_ids = fields.Many2many( # THIS FIELD STORES THE APPROPRIATE WAREHOUSES
        'stock.warehouse', compute='_compute_allowed_warehouses'
     )

     @api.depends('product_id','warehouse_id')
     def _compute_allowed_warehouses(self):
        for line in self:
            product = self.env['product.product'].search([('id' , '=' , line.product_id.id)])
            warehouses = []
            if product:
                for route in product.route_ids:
                    for rule in route.rule_ids:
                        if rule.warehouse_id.id not in warehouses and rule.warehouse_id:
                            warehouses.append(rule.warehouse_id.id)
            line.allowed_warehouse_ids = warehouses
            if not line.warehouse_id: #SET DEFAULT WAREHOUSE
               if line.allowed_warehouse_ids:
                    line.warehouse_id = line.allowed_warehouse_ids[0]
               else:
                    line.warehouse_id = None

     def _prepare_add_missing_fields(self , values): # SET DEFAULT WAREHOUSE WHEN CREATE SALE ORDER LINE WITH CONFIGURE PRODUCT
          res = super(sale_order_line_warehouse, self)._prepare_add_missing_fields(values)
          warehouses = []
          product = self.env['product.product'].search([('id' , '=' , values['product_id'])])
          for route in product.route_ids:
                    for rule in route.rule_ids:
                        if rule.warehouse_id.id not in warehouses and rule.warehouse_id:
                            warehouses.append(rule.warehouse_id.id)
          if warehouses:
               res['warehouse_id'] = warehouses[0]
          return res


