from odoo import models, fields, api

class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    call_rate = fields.Float('Call Rate')
    change_discount_bool = fields.Boolean(compute="_compute_change_discount", store=True)
    change_callrate_bool = fields.Boolean(compute="_compute_change_call_rate", store=True)
    
    @api.depends('discount')
    def _compute_change_discount(self):
        for line in self:
            line.change_discount_bool = bool(line.discount)

    @api.depends('call_rate')
    def _compute_change_call_rate(self):
        for line in self:
            line.change_callrate_bool = bool(line.call_rate)

    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self:
            line.call_rate = 100 - line.discount or 0

    @api.onchange('call_rate')
    def _onchange_call_rate(self):
        for line in self:
            line.discount = 100 - line.call_rate or 0

    def write(self, vals):
        self = self.with_context(skip_write=True)

        res = super(SaleOrderLineExtend, self).write(vals)

        if not self.env.context.get('skip_write'):
            for line in self:
                update_vals = {}
                if line.change_discount_bool and 'discount' in vals:
                    update_vals['call_rate'] = 100 - line.discount
                elif line.change_callrate_bool and 'call_rate' in vals:
                    update_vals['discount'] = 100 - line.call_rate
                if update_vals:
                    super(SaleOrderLineExtend, line).write(update_vals)

        return res
