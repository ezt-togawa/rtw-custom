# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_case(models.Model):
    _inherit = 'sale.order'

    case_id = fields.Many2one('rtw_sf_case' , string='Case')
    crm_id = fields.Many2one('crm.lead' , string='CRM')

    @api.model
    def create(self, vals):
        print('active_id' in self._context)
        if 'active_id' in self._context:
            if self._context['active_id'] and self._context['active_model'] == 'rtw_sf_case':
                vals['case_id'] = self._context.get('active_id')
                rtw_sf_case = self.env['rtw_sf_case'].search([('id' , '=' , self._context.get('active_id'))])
                vals['case_id'] = self._context.get('active_id')
                vals['crm_id'] = rtw_sf_case.crm_id.id
        return super(sale_order_case, self).create(vals)

    def open_form_view(self):
        self.ensure_one()
        return {
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
        }

class mrp_production_case(models.Model):
    _inherit = 'mrp.production'

    case_id = fields.Many2one('rtw_sf_case',string='Case',compute='_compute_case_crm')
    crm_id = fields.Many2one('crm.lead',string='CRM',compute='_compute_case_crm')
    inspected_status = fields.Boolean('Inspected Status',default=0)
    inspected_button = fields.Char('Inspected Button' , compute='_compute_inspected_button' , store=True)
    is_linked_to_crm = fields.Boolean('Is Linked To Crm',default=False, compute='_compute_is_linked_to_crm' , store=True)

    def toggle_inspected_btn(self):
        for record in self:
            record.inspected_status = not record.inspected_status

    @api.depends('inspected_status')
    def _compute_is_linked_to_crm(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name' , '=' , record.origin)])
            if sale_order and sale_order.case_id:
                record.is_linked_to_crm = True
            else:
                record.is_linked_to_crm = False

    @api.depends('inspected_status')
    def _compute_inspected_button(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name' , '=' , record.origin)])
            if sale_order and sale_order.case_id:
                if record.inspected_status:
                    record.inspected_button = '検品済'
                else:
                    record.inspected_button = '未検品'
            else:
                record.inspected_button = ''

    def _compute_case_crm(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name' , '=' , record.origin)])
            if sale_order:
                record.case_id = sale_order.case_id
                record.crm_id = sale_order.crm_id
            else:
                record.case_id = False
                record.crm_id = False

class rtw_sf_case_claim(models.Model):
    _inherit = 'rtw_sf_case'

    claim_no = fields.One2many('sale.order','case_id')
