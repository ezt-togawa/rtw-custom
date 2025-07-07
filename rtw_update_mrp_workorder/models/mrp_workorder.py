from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "mrp.workorder"
    
    implementation_plan_date = fields.Date('Implementation Plan Date')
    mrp_workorder_order_status = fields.Boolean('Mrp Order Status', compute="_compute_workorder_status")

    def _compute_workorder_status(self):
        for record in self:
            if record.production_id:
                record.mrp_workorder_order_status = record.production_id.mrp_order_status
            else:
                record.mrp_workorder_order_status = False
