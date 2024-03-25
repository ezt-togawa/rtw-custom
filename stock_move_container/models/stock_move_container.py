# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMoveContainer(models.Model):
    _name = 'stock.move.container'
    _description = 'stock.move.container'

    @api.model
    def create(self, vals):
        result = super(StockMoveContainer, self).create(vals)
        return result

    name = fields.Char('Name', required=True, translate=True)
    pallet_ids = fields.One2many(
        comodel_name="stock.move.pallet",
        inverse_name="container_id",
        string="PalletId", )
    status = fields.Char('ステータス', compute="_compute_status")
    note = fields.Text('備考', translate=True)

    def _compute_status(self):
        for record in self:
            status = "未完了"
            stock_container_move_lines = []
            stock_move_pallet_ids = self.env['stock.move.pallet'].search(
                [('container_id', '=', record.id)])
            if stock_move_pallet_ids:
                for pallet in stock_move_pallet_ids:
                    stock_move_lines = self.env['stock.move.line'].search(
                        [('pallet_id', '=', pallet.id)])
                    for line in stock_move_lines:
                        stock_container_move_lines.append(line)

                all_done = all(
                    line.state == 'done' for line in stock_container_move_lines)
                if all_done:
                    status = "完了"
            record.status = status


class stock_move_line_container(models.Model):
    _inherit = 'stock.move.line'

    container_id = fields.Many2one(
        'stock.move.container', string='コンテナ', compute='_compute_container_ids', store=True)

    @api.depends('pallet_id')
    def _compute_container_ids(self):
        for line in self:
            if line.pallet_id.container_id:
                line.container_id = line.pallet_id.container_id
            else:
                line.container_id = False


class stock_picking_container(models.Model):
    _inherit = 'stock.picking'

    container_id = fields.Many2one(
        'stock.move.container',
        string='コンテナ',
        compute='_compute_container_ids',
        )

    @api.depends('move_line_ids')
    def _compute_container_ids(self):
        for picking in self:
            pallet_ids = picking.move_line_ids.mapped('pallet_id')
            if pallet_ids:
                picking.container_id = pallet_ids[0].container_id
            else:
                picking.container_id = False
