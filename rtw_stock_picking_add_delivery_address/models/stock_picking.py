# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class stock_picking_delivery_wizard(models.TransientModel):
    _name = "stock.picking.delivery.wizard"

    warehouse_id = fields.Many2one('stock.warehouse')
    
    def add_delivery_address(self):
        if not self.warehouse_id:
            raise UserError('dmm add warehouse vào')
        
        current_stock_picking = self.env['stock.picking'].search([('id','=',self.env.context['active_id'])],limit=1)
        if not current_stock_picking.picking_type_id.sequence_code == 'OUT':
            raise UserError('ko phai Delivery Order')
        has_next_picking = self.env['stock.picking'].search([
            ('location_id','=',current_stock_picking.id),
            ('group_id','=',current_stock_picking.group_id.id),
            ('state', 'not in',['done','cancel'])]
        )
        picking_type_new_wh = self.env['stock.picking.type'].search([('sequence_code','=',current_stock_picking.picking_type_id.sequence_code),('warehouse_id','=',self.warehouse_id.id)])
        new_stock_picking = current_stock_picking.copy(
            {
                'location_id': picking_type_new_wh.default_location_src_id.id,
                'location_dest_id':current_stock_picking.location_dest_id.id if not has_next_picking else current_stock_picking.location_id.id,
                'picking_type_id':picking_type_new_wh.id,
                'state':'waiting',
                'scheduled_date': current_stock_picking.scheduled_date
            }
        )
        new_stock_picking.state = 'waiting'
        new_stock_picking.scheduled_date = current_stock_picking.scheduled_date

        current_stock_picking.write({'location_dest_id': picking_type_new_wh.default_location_src_id.id})
        if has_next_picking:
            has_next_picking.write({'location_id': current_stock_picking.location_dest_id.id if has_next_picking else current_stock_picking.location_id.id})
        
        
        