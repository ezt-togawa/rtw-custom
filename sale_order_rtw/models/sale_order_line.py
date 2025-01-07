# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_rtw(models.Model):
    _inherit = "sale.order.line"

    memo = fields.Char('memo')
    item_sale_attach_ids = fields.Many2many("item.attach", string="attach", copy=True)
    item_sale_attach_count = fields.Integer(
        "attach Count", compute="_compute_item_attach_count"
    )
    
    instruction_status = fields.Boolean(string='Instruction Status')

    def _compute_item_attach_count(self):
        for line in self:
            line.item_sale_attach_count = len(line.item_sale_attach_ids)

    def action_get_item_sale_attach_view(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_order_rtw.action_item_attach"
        )
        res["domain"] = [("sale_line_ids", "in", self.id)]
        res["context"] = {
            # "default_name": "図" + str(self.order_id.image_count+1),
            "default_product_id": self.product_id.id if self.product_id else False,
            "default_sale_line_ids": [(4, self.id)],
        }
        return res

    # 明細行の並び順担保処理（OCAのモジュール前提：sale_order_line_sequence）
    def write(self, vals):
        res = super(sale_order_line_rtw, self).write(vals)
        for record in self:
            # visible_sequence はOCAの項目、表示上の順番の番号、初期値9999
            # 複数行追加後に並び順を変えると、Odoo側でsequenceの+1をして、10000以上の数値なり以降の追加行が間に入るので順番が狂うのを調整する
            vals['sequence'] = record.visible_sequence
        return res
