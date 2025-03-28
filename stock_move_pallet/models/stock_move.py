# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class StockMoveLine(models.Model):
#     _inherit ='stock.move.line'

#     pallet_id = fields.Many2one('stock.move.pallet', 'パレット')

class StockMove(models.Model):
    _inherit ='stock.move'

    pallet_id = fields.Many2one('stock.move.pallet', 'パレット')
    manu_date_planned_start = fields.Datetime(string="製造開始予定日", compute="_manu_date_planned_start")
    pearl_tone_attr = fields.Char(string="パールトーン", compute="_compute_pearl_tone_attr", store=True)
    is_pearl_tone_attr = fields.Boolean()
    check_sale_id = fields.Char()
    
    @api.depends('production_id.date_planned_start')
    def _manu_date_planned_start(self):
        for rec in self:
            mrp = self.env['mrp.production'].search(
                [('origin', '=', rec.sale_id.name),('product_id','=',rec.product_id.id)],limit=1)
            if mrp:
                rec.manu_date_planned_start = mrp.date_planned_start 
            elif rec.picking_id.origin and '/MO/' in rec.picking_id.origin:
                if self.env['mrp.production'].search([('name', '=', rec.picking_id.origin)]):
                    rec.manu_date_planned_start = self.env['mrp.production'].search([('name', '=', rec.picking_id.origin)]).date_planned_start
                else:
                    rec.manu_date_planned_start = None
            elif rec.mrp_production_id:
                mrp_production = self.env['mrp.production'].search([('name','=',rec.mrp_production_id)],limit=1)
                if mrp_production:
                    rec.manu_date_planned_start = mrp_production.date_planned_start
                else:
                    rec.manu_date_planned_start = None
            else:
                rec.manu_date_planned_start = None

    @api.depends('product_id', 'product_id.product_template_attribute_value_ids', 'sale_id')
    def _compute_pearl_tone_attr(self):
        for line in self:

            # 部材の配送（stock.move）の場合のみ（購買のIN関連やChildMo関連）
            if line.product_id and not line.product_id.config_ok:
                line.is_pearl_tone_attr = False
                line.pearl_tone_attr = ''

                # stock.move が製造と紐づいていた場合のみ、親製造or子製造を判断して処理
                if line.mrp_production_id:

                    # 部材が series=張地 の場合のみパールトーン表記対象とする（'張地'の名称判断なのでシリーズの名称設定に影響うけてしまうのは注意）
                    if line.product_id and line.product_id.series == '張地':
                        attribute_name = ''
                        tmp_bom_line_id = None

                        # 配送にbom_line_idが無い場合＝部材の引当の移動ではなく純粋な配送オーダー扱いとして、連動している移動配送より処理
                        # 移動配送は製造オーダーに対する在庫の引当移動、移動配送にしかbom_line_id（部品表項目）が紐づいていない
                        if line.bom_line_id:
                            tmp_bom_line_id = line.bom_line_id
                        elif line.move_dest_ids:
                            tmp_bom_line_id = line.move_dest_ids[0].bom_line_id

                        if tmp_bom_line_id and tmp_bom_line_id.bom_product_template_attribute_value_ids:
                            # バリアントに適用情報の属性名
                            attribute_name = tmp_bom_line_id.bom_product_template_attribute_value_ids[0].attribute_id.name

                        # 製造の親が製造かどうかで、製品を取得する製造オーダーを取り分ける
                        parent_mrp = self.env['mrp.production'].search([('name', '=', line.mrp_production_id)])
                        if parent_mrp.origin and '/MO/' in parent_mrp.origin:
                            parent_mrp = self.env['mrp.production'].search([('name', '=', parent_mrp.origin)], limit=1)

                        is_pearl_tone_attr, attribute = self.get_attribute(parent_mrp.product_id, attribute_name)
                        line.is_pearl_tone_attr = is_pearl_tone_attr
                        line.pearl_tone_attr = attribute

    # プロダクト（製品）からパールトーン属性情報を取得
    def get_attribute(self, product, attribute_name):
        attribute = ''
        is_pearl_tone_attr = False
        if attribute_name and product and product.product_template_attribute_value_ids:
            for attr in product.product_template_attribute_value_ids:
                name_att = self.env['ir.model.data'].search(
                    [('model', '=', 'product.attribute'), ('res_id', '=', attr.attribute_id.id)]).name
                value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),
                                                              ('res_id', '=',
                                                               attr.product_attribute_value_id.id)]).name

                # パールトーンなしのID「951006」が変更ない前提の処理（属性マスタメンテ時は要注意）
                if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) != 951006:
                    namelist = attr.name.split('-')
                    if len(namelist) > 1 and namelist[1] in attribute_name:
                        is_pearl_tone_attr = True
                        attribute = attr.name
                    elif len(namelist) <= 1:
                        is_pearl_tone_attr = True
                        attribute = attr.name

        return is_pearl_tone_attr, attribute
