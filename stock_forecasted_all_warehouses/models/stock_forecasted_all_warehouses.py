# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo.http import request
from odoo import api, models
from odoo.tools import float_is_zero, format_datetime, format_date, float_round


class stock_forecasted_all_warehouses(models.AbstractModel):
    _inherit = 'report.stock.report_product_product_replenishment'
    
    def _get_report_data(self, product_template_ids=False, product_variant_ids=False):
        assert product_template_ids or product_variant_ids
        res = {}
        # Get the warehouse we're working on as well as its locations.  
        if self.env.context.get('warehouse'):
            warehouse = self.env['stock.warehouse'].browse(self.env.context['warehouse'])
        else:
            available_warehouse = []
            if 'active_id' in self.env.context:
                warehouses = self.env['stock.warehouse'].search([])
                params = self.env.context['params'] if 'params' in self.env.context else None
                active_model = ''
                if params:
                    if 'model' in params:
                        active_model = self.env.context['params']['model']
                    elif 'active_model' in params:
                        active_model = self.env.context['params']['active_model']
                else:
                    active_model = self.env.context['active_model']
                    
                if active_model == 'product.product':
                    product_product = self.env['product.product'].search([('id','=',self.env.context['active_id'])])
                else:
                    product_product = self.env['product.product'].search([('product_tmpl_id','=',self.env.context['active_id'])])
                    
                for warehouse in warehouses:
                    stored_product = 0
                    stored_virtual_available = 0
                    for product in product_product:
                        quants = self.env['stock.quant'].search([
                            ('product_id', '=', product.id),
                            ('location_id', 'child_of', warehouse.lot_stock_id.id)
                        ])
                        stored_virtual_available += product.with_context({'warehouse' : warehouse.id}).virtual_available
                        stored_product = stored_product + sum(quant.quantity for quant in quants)

                    if not stored_product == 0 or not stored_virtual_available == 0:
                        available_warehouse.append(warehouse.id)
                        
            itoshima_warehouse = self.env['stock.warehouse'].search([('code','=','糸島')]).id   
            if itoshima_warehouse in available_warehouse:
                warehouse = self.env['stock.warehouse'].search([
                    ('company_id', '=', self.env.company.id),
                    ('id', '=', itoshima_warehouse)
                ], limit=1)
            elif available_warehouse:
                warehouse = self.env['stock.warehouse'].search([
                    ('company_id', '=', self.env.company.id),
                    ('id', '=', available_warehouse[0])
                ], limit=1)
            else:
                warehouse = self.env['stock.warehouse'].search([
                    ('company_id', '=', self.env.company.id)
                ], limit=1)
            self.env.context = dict(self.env.context, warehouse=warehouse.id)
            
        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id)],
            ['id'],
        )]
        res['active_warehouse'] = warehouse.display_name

        # Get the products we're working, fill the rendering context with some of their attributes.
        if product_template_ids:
            product_templates = self.env['product.template'].browse(product_template_ids)
            res['product_templates'] = product_templates
            res['product_variants'] = product_templates.product_variant_ids
            res['multiple_product'] = len(product_templates.product_variant_ids) > 1
            res['uom'] = product_templates[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_templates.mapped('qty_available'))
            res['virtual_available'] = sum(product_templates.mapped('virtual_available'))
        elif product_variant_ids:
            product_variants = self.env['product.product'].browse(product_variant_ids)
            res['product_templates'] = False
            res['product_variants'] = product_variants
            res['multiple_product'] = len(product_variants) > 1
            res['uom'] = product_variants[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_variants.mapped('qty_available'))
            res['virtual_available'] = sum(product_variants.mapped('virtual_available'))
        res.update(self._compute_draft_quantity_count(product_template_ids, product_variant_ids, wh_location_ids))
        res['lines'] = self._get_report_lines(product_template_ids, product_variant_ids, wh_location_ids)
        return res

    @api.model
    def get_filter_state(self):
        res = {}
        available_warehouse = []
        if 'active_id' in self.env.context:
            warehouses = self.env['stock.warehouse'].search([])
            params = self.env.context['params'] if 'params' in self.env.context else None
            active_model = ''
            if params:
                if 'model' in params:
                    active_model = self.env.context['params']['model']
                elif 'active_model' in params:
                    active_model = self.env.context['params']['active_model']
            else:
                active_model = self.env.context['active_model']
                
            if active_model == 'product.product':
                product_product = self.env['product.product'].search([('id','=',self.env.context['active_id'])])
            else:
                product_product = self.env['product.product'].search([('product_tmpl_id','=',self.env.context['active_id'])])
                
            for warehouse in warehouses:
                stored_product = 0
                stored_virtual_available = 0
                for product in product_product:
                    quants = self.env['stock.quant'].search([
                        ('product_id', '=', product.id),
                        ('location_id', 'child_of', warehouse.lot_stock_id.id)
                    ])
                    stored_virtual_available += product.with_context({'warehouse' : warehouse.id}).virtual_available
                    stored_product = stored_product + sum(quant.quantity for quant in quants)
                if not stored_product == 0:
                    available_warehouse.append(warehouse.id)
                elif not stored_virtual_available == 0:
                    available_warehouse.append(warehouse.id)
                    
        if available_warehouse:
            warehouse = self.env['stock.warehouse'].search_read([('id','in',available_warehouse)],fields=['id', 'name', 'code'])
            warehouse.sort(key=lambda x: x['code'] != '糸島')
            res['warehouses'] = warehouse
        else:
            res['is_not_available_warehouse'] = True
            res['warehouses'] = []
        
        res['active_warehouse'] = self.env.context.get('warehouse', False)
        if not res['active_warehouse']:
            company_id = self.env.context.get('allowed_company_ids')[0]
            res['active_warehouse'] = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).id
        if len(res['warehouses']) > 0 and res['warehouses'][0]['code'] == '糸島':
            self.env.context = dict(self.env.context, warehouse=res['warehouses'][0]['id'])
            res['active_warehouse'] = res['warehouses'][0]['id']
        return res
