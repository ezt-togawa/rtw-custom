# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class StockMoveLine(models.Model):
#     _inherit ='stock.move.line'

#     pallet_id = fields.Many2one('stock.move.pallet', 'パレット')

class StockMove(models.Model):
    _inherit ='stock.move'

    pallet_id = fields.Many2one('stock.move.pallet', 'パレット')
    manu_date_planned_start = fields.Datetime(string="製造開始予定日", compute="_manu_date_planned_start")
    pearl_tone_attr = fields.Char(string="パールトーン", compute="_compute_pearl_tone_attr",store=True)
    is_pearl_tone_attr = fields.Boolean()
    check_sale_id = fields.Char()
    
    @api.depends('production_id.date_planned_start')
    def _manu_date_planned_start(self):
        for rec in self:
            mrp = self.env['mrp.production'].search(
                [('origin', '=', rec.sale_id.name)], limit=1)
            if mrp:
                rec.manu_date_planned_start = mrp.date_planned_start 
            elif rec.picking_id.origin and '/MO/' in rec.picking_id.origin:
                if self.env['mrp.production'].search([('name','=',rec.picking_id.origin)]):
                    rec.manu_date_planned_start = self.env['mrp.production'].search([('name','=',rec.picking_id.origin)]).date_planned_start
                else:
                    rec.manu_date_planned_start = None
            else:
                rec.manu_date_planned_start = None
    @api.depends('product_id', 'product_id.product_template_attribute_value_ids', 'sale_id')
    def _compute_pearl_tone_attr(self):
        pearl_tone_attr_values = {}
        for line in self:
            attribute = ''
            is_pearl_tone_attr = False
            check_sale_id = line.sale_id
            # 製品をもつ配送（stock.move）の場合
            if line.product_id and line.product_id.product_template_attribute_value_ids:
                for attr in line.product_id.product_template_attribute_value_ids:
                    name_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute'),('res_id', '=', attr.attribute_id.id)]).name
                    value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),('res_id', '=', attr.product_attribute_value_id.id)]).name
                    if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) != 951006:
                        attribute = attr.name
                        is_pearl_tone_attr = True
                        # check_sale_id = line.sale_id
                        pearl_tone_attr_values[line.mrp_production_id] = (is_pearl_tone_attr, attribute) # 製造単位でパールトーン情報保持

                if check_sale_id:
                    if line.mrp_production_id:
                        # 同じ製造オーダーを持つ配送をまとめて更新
                        records = self.env['stock.move'].search([('mrp_production_id', '=', line.mrp_production_id), ('state', '!=', 'cancel')])
                        records.write({
                            'is_pearl_tone_attr': is_pearl_tone_attr,
                            'pearl_tone_attr': attribute
                         })
                    else:
                        line.write({
                            'is_pearl_tone_attr': is_pearl_tone_attr,
                            'pearl_tone_attr': attribute
                         })

            # 製品をもたない配送（stock.move）の場合（購買のIN関連やChildMo関連）
            elif line.id:
                # stock.move が製造と紐づいていた場合すでに同じ製造に紐づいている配送から情報を得る（親の製造から作成されるため理論的にはあるはず）
                if line.mrp_production_id:
                    ref_attr_stock_move = self.env['stock.move'].search([('mrp_production_id', '=', line.mrp_production_id), ('is_pearl_tone_attr', '=', True)], limit=1)
                    if ref_attr_stock_move:  # ref_attr_stock_move は複数あってもどれも同じパールトーン情報
                        line.is_pearl_tone_attr = ref_attr_stock_move.is_pearl_tone_attr
                        line.pearl_tone_attr = ref_attr_stock_move.pearl_tone_attr
                    else:
                        # ChildMo関連のstock.moveだと仮定して親の製造までたどって処理。INもOUTも同様なので区別しない。なければブランク設定。
                        mrp = self.env['mrp.production'].search([('name', '=', line.mrp_production_id)])
                        parent_mrp = self.env['mrp.production'].search([('name', '=', mrp.origin)], limit=1).name
                        if parent_mrp:
                            ref_attr_stock_move = self.env['stock.move'].search([('mrp_production_id', '=', parent_mrp  ), ('is_pearl_tone_attr', '=', True)], limit=1)
                            line.is_pearl_tone_attr = ref_attr_stock_move.is_pearl_tone_attr
                            line.pearl_tone_attr = ref_attr_stock_move.pearl_tone_attr
                        else:
                            line.is_pearl_tone_attr = False
                            line.pearl_tone_attr = ''
                else:
                    line.is_pearl_tone_attr = False
                    line.pearl_tone_attr = ''
            else:
                line.is_pearl_tone_attr = False
                line.pearl_tone_attr = ''