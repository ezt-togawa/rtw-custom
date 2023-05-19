# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    sale_order_ids = fields.Char("sale order", compute='_compute_sale_order')
    sale_order_names = fields.Char("sale order title")

    # @api.model
    def action_purchase_form(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action")
        form = self.env.ref("purchase.purchase_order_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = self.id
        return action

    @api.depends('order_line.move_dest_ids.group_id.mrp_production_ids')
    def _compute_sale_order(self):
        for purchase in self:
            purchase.sale_order_ids = False
            move_dest_ids = purchase.order_line.move_dest_ids.group_id.mrp_production_ids
            move_ids = purchase.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                order = []
                name = []
                for rec in move_dest_ids:
                    order.append(rec.origin)
                    if self.env['sale.order'].search([('name', '=', rec.origin)]).title:
                        name.append(self.env['sale.order'].search([('name', '=', rec.origin)]).title)
                    purchase.sale_order_ids = ','.join(order)
                    purchase.sale_order_names = ','.join(name)
            else:
                purchase.sale_order_ids = False
                purchase.sale_order_names = False
                # sale_order = self.env['sale.order'].search([('name', '=', move_dest_ids)])
                # print(sale_order)
            # move_dest_ids.write({
            #     'name': self.invoice_id.name,
            #     'warranty_request_ids': [(4, self.id, {
            #     })]
            #     })