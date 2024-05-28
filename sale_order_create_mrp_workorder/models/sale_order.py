# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super(sale_order, self).action_confirm()
        self.refresh()
        
        mrp_ids = self.env['mrp.production'].search(
            [('sale_reference', '=', self.name)])
        overseas = self.overseas
        for mrp in mrp_ids:
            workorder_code = False
            p_type = False
            sale_order_line = False
            search_criteria = [ #limit 10 times
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ('move_ids', 'in', [move_id.id for move_id in mrp.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
            ]
            for search in search_criteria: #find sale_order_line
                if self.env['sale.order.line'].search([search]):
                    sale_order_line = self.env['sale.order.line'].search([search])
                    break

            if sale_order_line:
                p_type = sale_order_line.p_type
            
                if overseas and p_type == 'custom':
                    workorder_code = 'wk_001'
                elif overseas:
                    workorder_code = 'wk_001'
                elif p_type == 'custom':
                    workorder_code = 'wk_002'
                else:
                    workorder_code = False
            
            if workorder_code:
                name = False
                if workorder_code == 'wk_001':
                    name='検品（糸島）'
                elif workorder_code == 'wk_002':
                    name='検品（品質管理部）'
                workcenter = self.env['mrp.workcenter'].search([('code','=',workorder_code),('name','=',name)])
                if workcenter:
                    self.env['mrp.workorder'].create({
                        'name':workcenter.name,
                        'workcenter_id':workcenter.id,
                        'production_id':mrp.id,
                        'product_uom_id':mrp.product_uom_id.id,
                        'consumption':'flexible'
                    })
        return result   
