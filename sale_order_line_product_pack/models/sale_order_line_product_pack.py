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

     is_pack_outside = fields.Boolean('帳票出力外' ,default=False)

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
              "is_pack_outside":True
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
