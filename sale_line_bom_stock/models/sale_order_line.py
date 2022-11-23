# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class sale_line_bom_stock(models.Model):
    _inherit = "sale.order.line"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="BoM",
        domain="[('product_tmpl_id.product_variant_ids', '=', product_id),"
        "'|', ('product_id', '=', product_id), "
        "('product_id', '=', False)]",
    )
    bom_stock = fields.Char()


    @api.constrains("bom_id", "product_id")
    def _check_match_product_variant_ids(self):
        for line in self:
            if line.bom_id:
                bom_product_tmpl = line.bom_id.product_tmpl_id
                bom_product = bom_product_tmpl.product_variant_ids
            else:
                bom_product_tmpl, bom_product = None, None
            line_product = line.product_id
            if not bom_product or line_product == bom_product:
                continue
            raise ValidationError(
                _(
                    "Please select BoM that has matched product with the line `{}`"
                ).format(line_product.name)
            )

    @api.onchange('product_id')
    def _change_bom_id(self):
        for rec in self:
            print(rec.env['mrp.bom'].search([('product_id', '=', rec.product_id.id)]).id)
            print(rec.product_template_id.id)
            print(rec.product_id.id)


    @api.onchange('bom_id')
    def _check_bom_stock(self):
        for rec in self:
            if rec.bom_id:
                for item in rec.bom_id.bom_line_ids:
                    print(item.id)
