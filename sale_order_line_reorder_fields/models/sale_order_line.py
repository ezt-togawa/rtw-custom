from odoo import models, fields, api

class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    call_rate = fields.Float('Call Rate')
    updating_discount  = fields.Boolean()
    updating_call_rate  = fields.Boolean()
    warehouse_count = fields.Integer(compute='_compute_warehouse_count')

    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self:
            if line.discount or line.discount == 0:
                line.call_rate = 100 - line.discount
                line.updating_discount = True

    @api.onchange('call_rate')
    def _onchange_call_rate(self):
        for line in self:
            if line.call_rate or line.call_rate == 0:
                line.discount = 100 - line.call_rate
                line.updating_call_rate = True
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.ensure_one()
        if self.updating_discount or self.updating_call_rate:
            return
        elif self.order_id and self.order_id.pricelist_id and self.order_id.pricelist_id.discount_policy == 'without_discount' and self.order_id.pricelist_id.item_ids:
            price_item = self.order_id.pricelist_id.item_ids[0]
            if price_item.percent_price:
                percent_value = price_item.percent_price
                self.discount = percent_value
                self.call_rate = 100 - self.discount
        
    def write(self, vals):
        res = super(SaleOrderLineExtend, self).write(vals)
        for line in self:
            if (line.call_rate == 100 and line.discount == 0) or (line.call_rate == 0 and line.discount == 100):
                break
            if line.call_rate and line.discount and (line.call_rate + line.discount) == 100:
                break
            elif line.discount or line.discount == 0:
                line.call_rate = 100 - line.discount
                break
        return res

    @api.onchange('product_template_id')
    #オーダー明細のプロダクトの追加でプロダクトバリアントへのOnchangeを実行させる（本番で発火しない場合の対処ロジック）
    def _fields_onchange_product_id(self):
        if self.product_template_id:
            for line in self:
                prod_id = line.product_template_id.id
                product = self.env["product.product"].search([('product_tmpl_id', '=', prod_id)])
                for record in product:
                    if not record.config_ok:
                        self.product_id = product

    # 製品毎の選択可能倉庫数
    def _compute_warehouse_count(self):
        for record in self:
            record.warehouse_count = len(record.allowed_warehouse_ids)