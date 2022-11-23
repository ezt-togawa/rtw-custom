# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSpecRtw(models.Model):
    _inherit = "product.template"
    _description = 'product_spec_rtw.product_spec_rtw'
    summary = fields.Char(
        name="summary",
        string="summary"
    )
    product_no = fields.Char(
        name="product_no",
        string="product no"
    )
    width = fields.Integer(
        name="width",
        string="width"
    )
    height = fields.Integer(
        name="height",
        string="height"
    )
    depth = fields.Integer(
        name="depth",
        string="depth"
    )
    sh = fields.Integer(
        name="sh",
        string="sheet height"
    )
    ah = fields.Integer(
        name="ah",
        string="arm height"
    )
    cloth = fields.Float('cloth A(m)')
    cloth_b = fields.Float('cloth B(m)')
    leather = fields.Float('leather(sheet)')
    leather_ds = fields.Float('leather(ds)')
    shipping_cost_unit_price = fields.Integer('shipping cost unit price')
    leather_ds = fields.Float('leather(ds)')
    sai = fields.Float('sai')
    # shipping_cost = fields.Integer('sipping cost', compute="_shipping_cost_calc")
    lx_key_figure = fields.Integer('LX Key Figure')
    #部材情報
    classification = fields.Many2one(
        comodel_name="product.classification",
        string="Classification",
        required=False,
        ondelete="set null",
    )
    storage_location = fields.Many2many(
        comodel_name="stock.warehouse",
        string="storage location",
    )

    minimum_scale = fields.Float("Minimum scale")
    two_legs_scale = fields.Boolean("2Legs Scale")
    necessary_length_of_the_cloth_a = fields.Float("necessary length of the cloth A")
    necessary_length_of_the_cloth_b = fields.Float("necessary length of the cloth B")
    catalog = fields.Many2many("product.catalog", string="Catalog")
    series = fields.Char("series", Translate=True)
    kubun = fields.Selection([
        ('bom', '構成品'),
        ('product', '製品'),
    ], default='',
        string="kubun", )

    @api.depends('shipping_cost_unit_price', 'sai')
    def _shipping_cost_calc(self):
        cost = 0
        if self.shipping_cost_unit_price > 0 and self.sai:
            cost = self.shipping_cost_unit_price * self.sai
        return round(cost)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'print_description'
    print_description = fields.Text(name="print_description", string="print description")

    @api.onchange('product_id', 'config_session_id')
    def product_id_change(self):
        if self.product_id:
            res = super(SaleOrderLine, self).product_id_change()
            string = ""
            if self.product_id.product_no != False:
                string += '品番/' + str(self.product_id.product_no) + '\n'
            if self.product_id.height > 0:
                string += 'H/' + str(self.product_id.height) + 'mm\n'
            if self.product_id.depth > 0:
                string += 'D/' + str(self.product_id.depth) + 'mm\n'
            if self.product_id.width > 0:
                string += 'w/' + str(self.product_id.width) + 'mm\n'
            self.print_description = string
            return res


