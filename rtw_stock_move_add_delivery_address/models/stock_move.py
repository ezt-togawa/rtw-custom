# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

from odoo.addons.rtw_stock_picking_add_delivery_address.models.stock_picking import stock_picking_delivery_wizard


class stock_move_delivery_wizard(models.TransientModel):
    _name = "stock.move.delivery.wizard"
    _description = 'Stock Move Delivery Wizard'
    location_id = fields.Many2one(
    'stock.location', "Destination Location",
    default=lambda self: self.env['stock.location'].search([('complete_name', '=', '製品保管/白谷')], limit=1).id or False,
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
                    if sorted(movess.ids) != sorted(stock_move_ids):
                        if error_picking_names:
                            raise UserError("運送[{error_picking_names}]に、選択されていない別のプロダクトの配送が紐づいているため実施できません。運送を分割してから実施してください。".format(
                            error_picking_names=", ".join(error_picking_names)))
                        else:
                            raise UserError('選択した配送に紐づいてる運送が存在しないため配送追加を実施することができません。')
                if not picking.picking_type_id.sequence_code == 'OUT':
                    raise UserError('配送オーダーしか配送先を追加できません。')
                if picking.state in ['done' ,'cancel']:
                    raise UserError('完了かキャンセル済みの配送オーダーは配送先追加することができません。')
        stock_location = self.env['stock.location'].search([('id','=',self.location_id.id)])
        warehouse_id = self.env['stock.warehouse'].search([('view_location_id','=',stock_location.location_id.id)])
        if not warehouse_id:
            raise UserError('選択したロケーションは倉庫に紐づいていないため指定できません')
        if picking_ids:
            for picking in picking_ids:
                stock_picking_delivery_wizard.add_delivery_address(self, picking)
   
        