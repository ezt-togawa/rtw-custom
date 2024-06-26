# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime , timedelta
import math

class stock_location_route_delivery_lead(models.Model):
    _inherit = 'stock.location.route'

    delivery_lead_time = fields.Float(
        '配送リードタイム', default=0.0
    )

class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id','product_uom_qty')
    def _onchange_product_id(self):
        for line in self:
            product = self.env['product.product'].search([('id' , '=' , line.product_id.id)])
            supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , product.product_tmpl_id.id)])
            bom_ids = self.env['mrp.bom'].search([('product_tmpl_id', '=' , product.product_tmpl_id.id)])
            product_routes = product.route_ids
            supplier_delay = 0
            total_delivery_lead_time = 0
            is_route_buy = False
            bom_lead_time_list = []
            product_quantity = product.qty_available
            template_attribute_value_ids = product.product_template_attribute_value_ids
            
            # for route in product.route_ids:
            #     for rule in route.rule_ids:
            #         if rule.action == 'buy':
            #             is_route_buy = True

            if bom_ids: #CALCULATE FOR MATERIALS
                for bom in bom_ids:
                    for bom_line in bom.bom_line_ids:
                        if (not bom_line.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in bom_line.bom_product_template_attribute_value_ids.ids)) and bom_line.product_id.product_tmpl_id.type == 'product':
                            bom_product = self.env['product.product'].search([('id' , '=' , bom_line.product_id.id)])
                            bom_product_routes = bom_product.route_ids
                            bom_supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , bom_product.product_tmpl_id.id)])
                            bom_total_lead_time = 0
                            bom_supplier_delay = 0
                            is_bom_route_buy = False
                            bom_product_quantity = bom_product.qty_available
                            sale_order_line_product_qty = line.product_uom_qty
                            amount_consumed = bom_line.available_quantity - (sale_order_line_product_qty * bom_line.product_qty)
                            # for route in bom_product_routes:
                            #     for rule in route.rule_ids:
                            #         if rule.action == 'buy':
                            #             is_bom_route_buy = True
                                        
                            if amount_consumed < 0: # DELIVERY LEAD TIME CALCULATED ONLY WHEN QUANTITY <0      
                                bom_child_ids = self.env['mrp.bom'].search([('product_tmpl_id', '=' , bom_product.product_tmpl_id.id)])
                                for child_bom in bom_child_ids:
                                    for child_bom_line in child_bom.bom_line_ids:
                                        if (not child_bom_line.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in child_bom_line.bom_product_template_attribute_value_ids.ids)) and child_bom_line.product_id.product_tmpl_id.type == 'product':
                                            child_bom_product = self.env['product.product'].search([('id' , '=' , child_bom_line.product_id.id)])
                                            child_bom_product_routes = child_bom_product.route_ids
                                            child_bom_supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , child_bom_line.product_tmpl_id.id)])
                                            child_bom_total_lead_time = 0
                                            child_bom_supplier_delay = 0
                                            child_amount_consumed = child_bom_line.available_quantity - (sale_order_line_product_qty * child_bom_line.product_qty)
                                            if child_amount_consumed < 0:
                                                for route in child_bom_product_routes:
                                                    if route.delivery_lead_time:
                                                        child_bom_total_lead_time += route.delivery_lead_time
                                                for bom_supplier in child_bom_supplier_info:
                                                    if bom_supplier.delay and bom_supplier.delay > child_bom_supplier_delay:
                                                        child_bom_supplier_delay = bom_supplier.delay
                                                if bom_supplier_delay < child_bom_total_lead_time + child_bom_supplier_delay + child_bom_product.product_tmpl_id.produce_delay:
                                                    bom_supplier_delay = child_bom_total_lead_time + child_bom_supplier_delay + child_bom_product.product_tmpl_id.produce_delay
                                    
                                for route in bom_product_routes:
                                    if route.delivery_lead_time:
                                        bom_total_lead_time += route.delivery_lead_time

                                for bom_supplier in bom_supplier_info:
                                    if bom_supplier.delay and bom_supplier.delay > bom_supplier_delay:
                                        bom_supplier_delay = bom_supplier.delay

                                bom_total_lead_time = bom_total_lead_time + bom_supplier_delay + bom_product.product_tmpl_id.produce_delay
                                bom_lead_time_list.append(bom_total_lead_time)

            if bom_lead_time_list:
                supplier_delay = max(bom_lead_time_list)

            if product_quantity <= 0:
                for route in product_routes:
                    if route.delivery_lead_time:
                        total_delivery_lead_time += route.delivery_lead_time

                for supplier in supplier_info:
                    if supplier.delay and supplier.delay > supplier_delay:
                        supplier_delay = supplier.delay

            additional_time = math.ceil(supplier_delay + total_delivery_lead_time + product.product_tmpl_id.produce_delay)
            line.date_planned = datetime.today() + timedelta(days=additional_time)

    @api.model
    def _prepare_add_missing_fields(self , values):
          res = super(sale_order_line, self)._prepare_add_missing_fields(values)
          product = self.env['product.product'].search([('id' , '=' , values['product_id'])])
          supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , product.product_tmpl_id.id)])
          bom_ids = self.env['mrp.bom'].search([('product_tmpl_id', '=' , product.product_tmpl_id.id)])
          product_routes = product.route_ids
          supplier_delay = 0
          total_delivery_lead_time = 0
          is_route_buy = False
          bom_lead_time_list = []
          product_quantity = product.qty_available
          template_attribute_value_ids = product.product_template_attribute_value_ids
        #   for route in product.route_ids:
        #             for rule in route.rule_ids:
        #                 if rule.action == 'buy':
        #                     is_route_buy = True
          if bom_ids:
                for bom in bom_ids:
                    for bom_line in bom.bom_line_ids:
                        if (not bom_line.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in bom_line.bom_product_template_attribute_value_ids.ids)) and bom_line.product_id.product_tmpl_id.type == 'product':
                            bom_product = self.env['product.product'].search([('id' , '=' , bom_line.product_id.id)])
                            bom_product_routes = bom_product.route_ids
                            bom_supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , bom_product.product_tmpl_id.id)])
                            bom_total_lead_time = 0
                            bom_supplier_delay = 0
                            is_bom_route_buy = False
                            bom_product_quantity = bom_product.qty_available
                            sale_order_line_product_qty = 1 
                            if 'product_uom' in res:
                                sale_order_line_product_qty = res['product_uom']
                            amount_consumed = bom_line.available_quantity - (sale_order_line_product_qty * bom_line.product_qty)
                            # for route in bom_product_routes:
                            #     for rule in route.rule_ids:
                            #         if rule.action == 'buy':
                            #             is_bom_route_buy = True

                            if amount_consumed < 0: # DELIVERY LEAD TIME CALCULATED ONLY WHEN QUANTITY <0
                                bom_child_ids = self.env['mrp.bom'].search([('product_tmpl_id', '=' , bom_product.product_tmpl_id.id)])
                                for child_bom in bom_child_ids:
                                    for child_bom_line in child_bom.bom_line_ids:
                                        if (not child_bom_line.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in child_bom_line.bom_product_template_attribute_value_ids.ids)) and child_bom_line.product_id.product_tmpl_id.type == 'product':
                                            child_bom_product = self.env['product.product'].search([('id' , '=' , child_bom_line.product_id.id)])
                                            child_bom_product_routes = child_bom_product.route_ids
                                            child_bom_supplier_info = self.env['product.supplierinfo'].search([('product_tmpl_id' , '=' , child_bom_line.product_tmpl_id.id)])
                                            child_bom_total_lead_time = 0
                                            child_bom_supplier_delay = 0
                                            child_amount_consumed = child_bom_line.available_quantity - (sale_order_line_product_qty * child_bom_line.product_qty)
                                            if child_amount_consumed < 0:
                                                for route in child_bom_product_routes:
                                                    if route.delivery_lead_time:
                                                        child_bom_total_lead_time += route.delivery_lead_time
                                                for bom_supplier in child_bom_supplier_info:
                                                    if bom_supplier.delay and bom_supplier.delay > child_bom_supplier_delay:
                                                        child_bom_supplier_delay = bom_supplier.delay
                                                if bom_supplier_delay < child_bom_total_lead_time + child_bom_supplier_delay + child_bom_product.product_tmpl_id.produce_delay:
                                                    bom_supplier_delay = child_bom_total_lead_time + child_bom_supplier_delay + child_bom_product.product_tmpl_id.produce_delay
                                
                                for route in bom_product_routes:
                                    if route.delivery_lead_time:
                                        bom_total_lead_time += route.delivery_lead_time

                                for bom_supplier in bom_supplier_info:
                                    if bom_supplier.delay and bom_supplier.delay > bom_supplier_delay:
                                        bom_supplier_delay = bom_supplier.delay

                                bom_total_lead_time = bom_total_lead_time + bom_supplier_delay + bom_product.product_tmpl_id.produce_delay
                                bom_lead_time_list.append(bom_total_lead_time)
          if bom_lead_time_list:
              supplier_delay = max(bom_lead_time_list)
          if product_quantity <= 0:
            for route in product_routes:
                if route.delivery_lead_time:
                    total_delivery_lead_time += route.delivery_lead_time

            for supplier in supplier_info:
                if supplier.delay and supplier.delay > supplier_delay:
                    supplier_delay = supplier.delay

          additional_time = math.ceil(supplier_delay + total_delivery_lead_time + product.product_tmpl_id.produce_delay)

          res['date_planned'] = datetime.today() + timedelta(days=additional_time)

          return res
