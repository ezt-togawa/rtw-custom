# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    combined_field = fields.Char(
        compute="_compute_combined_field",
        string="Combined Field",
        store=True
    )

    def _compute_combined_field(self):
        for record in self:
            record.combined_field = "abcef"
