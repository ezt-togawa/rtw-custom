# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    shipping_due_date = fields.Datetime(
        "Shipping Due Date",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        help="The date the customer is expected to shipping the delivery.",
    )

    confirmed_shipping_date = fields.Date(
        "Confirmed shipping Date",
        compute="_compute_date_shipped",
        store=True,

    )

    scheduled_date = fields.Datetime(
        '予定日',
    )

    @api.depends("shipping_due_date")
    def _compute_date_shipped(self):
        for pick in self.filtered(lambda x: x.shipping_due_date):
            pick.confirmed_shipping_date = fields.Date.to_date(
                fields.Datetime.context_timestamp(pick, pick.shipping_due_date)
            )

    # @api.model
    # def fields_view_get(
    #     self, view_id=None, view_type="form", toolbar=False, submenu=False
    # ):
    #     if view_type == "tree":
    #         pick_type_id = self._context.get("default_picking_type_id")
    #         if (
    #             not pick_type_id
    #             or pick_type_id
    #             and self.env["stock.picking.type"].browse([pick_type_id]).code
    #             in "outgoing"
    #         ):
    #             view_id = self.env.ref(
    #                 "confirmed_shipping_date.vpicktree_outgoing"
    #             ).id
    #     return super(StockPicking, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
    #     )

    def action_picking_form(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_form")
        form = self.env.ref("stock.view_picking_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = self.id
        return action
