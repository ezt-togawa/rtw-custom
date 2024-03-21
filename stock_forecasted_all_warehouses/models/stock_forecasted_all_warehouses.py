# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo.http import request
from odoo import api, models
from odoo.tools import float_is_zero, format_datetime, format_date, float_round


class stock_forecasted_all_warehouses(models.AbstractModel):
    _inherit = 'report.stock.report_product_product_replenishment'

    @api.model
    def get_filter_state(self):
        res = {}
        available_warehouse = []
        if 'active_id' in self.env.context:
            warehouses = self.env['stock.warehouse'].search([])
            product_product = self.env['product.product'].search([('product_tmpl_id','=',self.env.context['active_id'])])
            for warehouse in warehouses:
                stored_product = 0
                for product in product_product:
                    quants = self.env['stock.quant'].search([
                        ('product_id', '=', product.id),
                        ('location_id', 'child_of', warehouse.lot_stock_id.id)
                    ])
                    stored_product = stored_product + sum(quant.quantity for quant in quants)
                if stored_product > 0:
                    available_warehouse.append(warehouse.id)
        if available_warehouse:
            warehouse = self.env['stock.warehouse'].search_read([('id','in',available_warehouse)],fields=['id', 'name', 'code'])
            warehouse.sort(key=lambda x: x['code'] != '糸島')
            res['warehouses'] = warehouse
        else:
            res['is_not_available_warehouse'] = True
            res['warehouses'] = self.env['stock.warehouse'].search_read(fields=['id', 'name', 'code'],limit=1)
        
        res['active_warehouse'] = self.env.context.get('warehouse', False)
        if not res['active_warehouse']:
            company_id = self.env.context.get('allowed_company_ids')[0]
            res['active_warehouse'] = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).id
        if res['warehouses'][0]['code'] == '糸島':
            res['active_warehouse'] = res['warehouses'][0]['id']
        return res