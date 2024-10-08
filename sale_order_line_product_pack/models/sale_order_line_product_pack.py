# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.fields import first


class sale_order_product_pack(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def check_pack_line_unlink(self):
        origin_line_ids = self._origin.order_line.ids
        line_ids = self.order_line.ids
        removed_line_ids = list(set(origin_line_ids) - set(line_ids))
        removed_line = self.env["sale.order.line"].browse(removed_line_ids)
        if removed_line.filtered(
            lambda x: x.pack_parent_line_id
            and not x.pack_parent_line_id.product_id.pack_modifiable
        ):
            pass


class sale_order_line_product_pack(models.Model):
    _inherit = "sale.order.line"

    is_pack_outside = fields.Boolean('帳票出力外', default=False)

    def expand_pack_line(self, write=False):
        self.ensure_one()
        vals_list = []
        if self.product_id.pack_ok and self.pack_type == "detailed":
            for subline in self.product_id.product_tmpl_id.mapped('pack_line_ids'):
                vals = subline.get_sale_order_line_vals(self, self.order_id)
                if write:
                    existing_subline = first(
                        self.pack_child_line_ids.filtered(
                            lambda child: child.product_id == subline.product_id
                        )
                    )
                    # if subline already exists we update, if not we create
                    if existing_subline:
                        if self.do_no_expand_pack_lines:
                            vals.pop("product_uom_qty", None)
                            vals.pop("discount", None)
                        existing_subline.write(vals)
                    elif not self.do_no_expand_pack_lines:
                        vals_list.append(vals)
                else:
                    vals_list.append(vals)
            if vals_list:
                self.create(vals_list)


class product_pack(models.Model):
    _inherit = "product.pack.line"

    def get_sale_order_line_vals(self, line, order):
        self.ensure_one()
        quantity = self.quantity * line.product_uom_qty
        line_vals = {
            "order_id": order.id,
            "sequence": line.sequence,
            "product_id": self.product_id.id or False,
            "pack_parent_line_id": line.id,
            "pack_depth": line.pack_depth + 1,
            "company_id": order.company_id.id,
            "pack_modifiable": line.product_id.pack_modifiable,
            "is_pack_outside": True
        }
        sol = line.new(line_vals)
        sol.product_id_change()
        sol.product_uom_qty = quantity
        sol.product_uom_change()
        sol._onchange_discount()
        vals = sol._convert_to_write(sol._cache)
        pack_price_types = {"totalized", "ignored"}
        sale_discount = 0.0
        if line.product_id.pack_component_price == "detailed":
            sale_discount = 100.0 - (
                (100.0 - sol.discount) * (100.0 - self.sale_discount) / 100.0
            )
        elif (
            line.product_id.pack_type == "detailed"
            and line.product_id.pack_component_price in pack_price_types
        ):
            vals["price_unit"] = 0.0
        vals.update(
            {
                "discount": sale_discount,
                "name": "{}{}".format("> " * (line.pack_depth + 1), sol.name),
            }
        )
        return vals


class ProductTemplateProductPack(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        _vals = vals.copy()
        for template in self:
            list_vals = []
            child_products = []
            child_product = self.env['product.product'].search(
                [('product_tmpl_id', '=', template.id)])
            for product in child_product:
                child_products.append(product.id)
            if vals.get("pack_line_ids", False):
                for val in vals.get("pack_line_ids", False):
                    if not val[0] == 4:  # CREATE
                        list_vals.append(val)
                    if val[0] == 2:  # DELETE
                        pack_line_product_id = self.env['product.pack.line'].search(
                            [('id', '=', val[1])]).product_id.id
                        pack_line = self.env['product.pack.line'].search(
                            [('parent_product_id', 'in', child_products), ('product_id', '=', pack_line_product_id)])
                        if pack_line:
                            for pack in pack_line:
                                if [2, pack.id, False] not in list_vals:
                                    list_vals.append([2, pack.id, False])
                    if val[0] == 1:  # UPDATE
                        pack_line_product_id = self.env['product.pack.line'].search(
                            [('id', '=', val[1])]).product_id.id
                        pack_line = self.env['product.pack.line'].search(
                            [('parent_product_id', 'in', child_products), ('product_id', '=', pack_line_product_id)])
                        if pack_line:
                            for pack in pack_line:
                                if [1, pack.id, val[2]] not in list_vals:
                                    list_vals.append([1, pack.id, val[2]])
            template.product_variant_ids.write({"pack_line_ids": list_vals})
            if 'pack_line_ids' in vals:
                _vals.pop("pack_line_ids")
        return super(ProductTemplateProductPack, self).write(_vals)
