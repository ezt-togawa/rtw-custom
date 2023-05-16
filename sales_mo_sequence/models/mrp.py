from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round
from datetime import datetime
from dateutil.relativedelta import relativedelta


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('origin')
    def _compute_reference_value(self):
        for value in self:
            sale_ids = self.env['sale.order'].search([('name', '=', value.origin)])
            #             print(sale_ids,'mrp')
            if sale_ids:
                value.sale_reference = sale_ids.name
            else:
                mrp_ids = self.env['mrp.production'].search([('name', '=', value.origin)])
                value.sale_reference = mrp_ids.sale_reference
            #             print(value.sale_reference,'sale')

    @api.depends('name')
    def _compute_reference_mo(self):
        for value in self:
            if value.state == 'draft':
                sale_ids = self.env['sale.order'].search([('name', '=', value.origin)])
                if sale_ids:
                    value.mrp_reference = value.name
                #                     print(value.mrp_reference,'mrp_reference')

                else:
                    mrp_ids = self.env['mrp.production'].search([('name', '=', value.origin)])
                    value.mrp_reference = mrp_ids.mrp_reference
            #                     print(value.mrp_reference,'MO')

            if not value.origin:
                value.mrp_reference = value.name

            else:
                mrp_ids = self.env['mrp.production'].search([('name', '=', value.mrp_reference)])
                for ele in mrp_ids:
                    value.mrp_reference = ele.mrp_reference

    def _compute_production_type(self):
        for record in self:
            sale_order_line = self.env['sale.order.line'].search([('bom_id', '=', record.bom_id.id)])
            if sale_order_line:
                record.production_type = sale_order_line.p_type
                record.production_memo = sale_order_line.memo
            else:
                record.production_type = ''
                record.production_memo = ''

    sale_reference = fields.Char('SO Reference', compute='_compute_reference_value', store=True)
    mrp_reference = fields.Char('MO Reference', compute='_compute_reference_mo', store=True)
    production_type = fields.Char('製品タイプ' , compute='_compute_production_type')
    production_memo = fields.Char('memo' , compute='_compute_production_type')

class Workorder(models.Model):
    _inherit = 'mrp.workorder'

    sale_reference = fields.Char('SO Reference', related='production_id.sale_reference')
    mrp_reference = fields.Char('MO Reference', related='production_id.mrp_reference')
