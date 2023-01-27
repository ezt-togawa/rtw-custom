# Copyright 2019-2020 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class TierValidation_rtw(models.AbstractModel):
    _inherit = "tier.validation"

    validated = fields.Boolean(
        compute="_compute_validated_rejected", search="_search_validated", store=True
    )