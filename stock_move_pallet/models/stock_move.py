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
        for line in self:
            check_sale_id = line.sale_id
            # 製品をもつ配送（stock.move）の場合
            if line.product_id and line.product_id.config_ok:
                is_pearl_tone_attr, attribute = self.get_attribute(line.product_id)
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
                # stock.move が製造と紐づいていた場合は親製造or子製造を判断して処理
                if line.mrp_production_id:

                    # 製造の親が製造かどうかで、製品を取得する製造オーダーを取り分ける
                    parent_mrp = self.env['mrp.production'].search([('name', '=', line.mrp_production_id)])
                    if parent_mrp.origin and '/MO/' in parent_mrp.origin:
                        parent_mrp = self.env['mrp.production'].search([('name', '=', parent_mrp.origin)], limit=1)

                    is_pearl_tone_attr, attribute = self.get_attribute(parent_mrp.product_id)
                    line.is_pearl_tone_attr = is_pearl_tone_attr
                    line.pearl_tone_attr = attribute

                else:
                    line.is_pearl_tone_attr = False
                    line.pearl_tone_attr = ''
            else:
                line.is_pearl_tone_attr = False
                line.pearl_tone_attr = ''

    # プロダクト（製品）からパールトーン属性情報を取得
    def get_attribute(self, product):
        attribute = ''
        is_pearl_tone_attr = False
        if product and product.product_template_attribute_value_ids:
            for attr in product.product_template_attribute_value_ids:
                name_att = self.env['ir.model.data'].search(
                    [('model', '=', 'product.attribute'), ('res_id', '=', attr.attribute_id.id)]).name
                value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),
                                                              ('res_id', '=',
                                                               attr.product_attribute_value_id.id)]).name
                if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) != 951006:
                    is_pearl_tone_attr = True
                    attribute = attr.name
        return is_pearl_tone_attr, attribute
