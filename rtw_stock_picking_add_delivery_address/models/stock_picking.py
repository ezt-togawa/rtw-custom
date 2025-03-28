# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class stock_picking_delivery_wizard(models.TransientModel):
    _name = "stock.picking.delivery.wizard"

    location_id = fields.Many2one(
    'stock.location', "Destination Location",
    default=lambda self: self.env['stock.location'].search([('complete_name', '=', '製品保管/白谷')], limit=1).id or False,
)

    def add_delivery_address(self, picking=False):
        current_stock_picking = False
        if picking:
            current_stock_picking = picking
        else:
            if not self.location_id:
                raise UserError('倉庫を選択してください。')
            current_stock_picking = self.env['stock.picking'].search([('id','=',self.env.context['active_id'])],limit=1)
            if not current_stock_picking.picking_type_id.sequence_code == 'OUT':
                raise UserError('配送オーダーしか配送先を追加できません。')
            if current_stock_picking.state in ['done' ,'cancel']:
                raise UserError('完了かキャンセル済みの配送オーダーは配送先追加することができません。')
        has_next_picking = self.env['stock.picking'].search([
            ('location_id','=',current_stock_picking.location_dest_id.id),
            ('group_id','=',current_stock_picking.group_id.id),
            ('state', 'not in',['done','cancel'])],limit=1)
        stock_location = self.env['stock.location'].search([('id','=',self.location_id.id)])
        warehouse_id = self.env['stock.warehouse'].search([('view_location_id','=',stock_location.location_id.id)])
        if not warehouse_id:
            raise UserError('選択したロケーションは倉庫に紐づいていないため指定できません')
        picking_type_new_wh = self.env['stock.picking.type'].search([('sequence_code','=',current_stock_picking.picking_type_id.sequence_code),('warehouse_id','=',warehouse_id.id)])
        
        new_stock_picking = current_stock_picking.copy(
            {
                'location_id': stock_location.id,
                'location_dest_id':current_stock_picking.location_dest_id.id if not has_next_picking else has_next_picking.location_id.id,
                'picking_type_id':picking_type_new_wh.id,
                'state':'waiting',
                'scheduled_date': current_stock_picking.scheduled_date,
            }
        )
        new_stock_picking.carrier_price=False
        new_stock_picking.has_deadline_issue=False
        new_stock_picking.state = 'waiting'
        new_stock_picking.scheduled_date = current_stock_picking.scheduled_date

        new_stock_move = self.env['stock.move'].search([('picking_id','=',new_stock_picking.id)])
        new_stock_move.state = 'waiting'
        new_stock_move.rule_id = False
        new_stock_move.created_production_id = False
        new_stock_move.next_serial_count = False
        # new_stock_move.procure_method = 'make_to_stock'
        
        # self.env['stock.move.line'].create({
        #     'picking_id':new_stock_picking.id,
        #     'move_id':new_stock_move.id,
        #     'product_id':new_stock_move.product_id.id,
        #     'product_uom_id':new_stock_move.product_uom.id,
        #     # 'product_qty':new_stock_move.product_qty,
        #     'product_uom_qty':new_stock_move.product_uom_qty,
        #     'location_id':new_stock_move.location_id.id,
        #     'location_dest_id':new_stock_move.location_dest_id.id,
        #     'reference':new_stock_picking.name,
        #     'state':'assigned'
        # })
        current_stock_picking.write({'location_dest_id': stock_location.id})
        
        if has_next_picking:
            has_next_picking.write({'location_id': new_stock_picking.location_dest_id.id})
            next_stock_move = self.env['stock.move'].search([('picking_id' ,'=',has_next_picking.id),('product_id','=',has_next_picking.product_id.id)])
            for sm in next_stock_move:
                new_stock_move.write({'move_dest_ids':[(4 ,sm.id)]})

        current_stock_move = self.env['stock.move'].search([('picking_id' ,'=',current_stock_picking.id),('product_id','=',current_stock_picking.product_id.id)])
        for sm in new_stock_move:
            current_stock_move.write({'move_dest_ids':[(6,0,[sm.id])]})
        