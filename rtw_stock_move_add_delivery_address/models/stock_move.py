# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class stock_move_delivery_wizard(models.TransientModel):
    _name = "stock.move.delivery.wizard"
    _description = 'Stock Move Delivery Wizard'
    location_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
    )
    def add_delivery_address_stock_move(self):
        if not self.location_id:
            raise UserError('倉庫を選択してください。')
        current_stock_picking = False
        stock_move_ids = self.env.context.get('active_ids', [])
        moves = self.env['stock.move'].search([('id', 'in', stock_move_ids)])
        picking_ids = moves.mapped('picking_id')
        if not picking_ids:
            raise UserError("選択した配送に紐づいてる運送が存在しないため配送追加を実施することができません。")
        error_picking_names = []
        if picking_ids:
            picking_idss = [picking_id.id for picking_id in picking_ids]
            movess = self.env['stock.move'].search([('picking_id', 'in', picking_idss)])
            different_moves = movess.filtered(lambda m: m.id not in stock_move_ids)
            error_picking_names = list(set(different_moves.mapped('picking_id.name')))
            for picking in picking_ids:
                if moves:
                    if movess.ids != stock_move_ids:
                        raise UserError("運送[{error_picking_names}]に、選択されていない別のプロダクトの配送が紐づいているため実施できません。運送を分割してから実施してください。".format(
                            error_picking_names=", ".join(error_picking_names)))
                current_stock_picking = picking
        if not current_stock_picking.picking_type_id.sequence_code == 'OUT':
            raise UserError('配送オーダーしか配送先を追加できません。')
        if current_stock_picking.state in ['done' ,'cancel']:
            raise UserError('完了かキャンセル済みの配送オーダーは配送先追加することができません。')
       
        warehouse_id = self.env['stock.warehouse'].search([('lot_stock_id','=',self.location_id.id)])
        if not warehouse_id:
            raise UserError('選択したロケーションは倉庫に紐づいていないため指定できません')
        if picking_ids:
         for picking in picking_ids:
            has_next_picking = self.env['stock.picking'].search([
            ('location_id','=',picking.location_dest_id.id),
            ('group_id','=',picking.group_id.id),
            ('state', 'not in',['done','cancel'])],limit=1
        )
            picking_type_new_wh = self.env['stock.picking.type'].search([('sequence_code','=',picking.picking_type_id.sequence_code),('warehouse_id','=',warehouse_id.id)])
            new_stock_picking = picking.copy(
                {
                    'location_id': self.location_id.id,
                    'location_dest_id':picking.location_dest_id.id if not has_next_picking else has_next_picking.location_id.id,
                    'picking_type_id':picking_type_new_wh.id,
                    'state':'waiting',
                    'scheduled_date': picking.scheduled_date,
                }
            )
            new_stock_picking.carrier_price=False
            new_stock_picking.has_deadline_issue=False
            new_stock_picking.state = 'waiting'
            new_stock_picking.scheduled_date = picking.scheduled_date

            new_stock_move = self.env['stock.move'].search([('picking_id','=',new_stock_picking.id)])
            new_stock_move.state = 'waiting'
            new_stock_move.rule_id = False
            new_stock_move.created_production_id = False
            new_stock_move.next_serial_count = False
            picking.write({'location_dest_id': self.location_id.id})
            if has_next_picking:
                has_next_picking.write({'location_id': new_stock_picking.location_dest_id.id})
                next_stock_move = self.env['stock.move'].search([('picking_id' ,'=',has_next_picking.id),('product_id','=',has_next_picking.product_id.id)])
                for sm in next_stock_move:
                    new_stock_move.write({'move_dest_ids':[(4 ,sm.id)]})

            current_stock_move = self.env['stock.move'].search([('picking_id' ,'=',picking.id),('product_id','=',picking.product_id.id)])
            for sm in new_stock_move:
                current_stock_move.write({'move_dest_ids':[(6,0,[sm.id])]})
        