from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "mrp.workorder"
    
    implementation_plan_date = fields.Date('Implementation Plan Date')
    mrp_workorder_order_status = fields.Boolean('Mrp Order Status', compute="_compute_workorder_status")
    planned_production_start_date = fields.Date('Planned Production Start Date',compute="_compute_planned_production_start_date", store=True)
    quantity = fields.Float('Quantity', compute='_compute_quantity')
    work_notes = fields.Char('作業メモ')


    def _compute_workorder_status(self):
        for record in self:
            if record.production_id:
                record.mrp_workorder_order_status = record.production_id.mrp_order_status
            else:
                record.mrp_workorder_order_status = False

    @api.depends('production_id.date_planned_start')
    def _compute_planned_production_start_date(self):
        for record in self:
            if record.production_id:
                record.planned_production_start_date = record.production_id.date_planned_start
            else:
                record.planned_production_start_date = False

    def _compute_quantity(self):
        for record in self:
            if record.production_id:
                record.quantity = record.production_id.product_qty
            else:
                record.quantity = 0.0