# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    show_details = fields.Boolean(
        string="Show details",
        default=True)
    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)

class AccountMoveCus(models.Model):
    _inherit = 'account.move'

    send_to_company = fields.Char(string="send to company", compute="_compute_send_to")
    send_to_people = fields.Char(string="send to people", compute="_compute_send_to")

    def _compute_send_to(self):
        for line in self:
            partner_name = ''
            company_name = ''
            if line.lang_code == 'en_US' and line.partner_id:
                res_partner = self.env['res.partner'].search([('id', '=', line.partner_id.id)])
                if res_partner:
                    for partner in res_partner:
                        partner_name = ('Mr./Mrs. ' + partner.last_name) if partner.last_name else ''
                        company_name = ('御中 ' + partner.parent_id.name + ' 株式会社') if partner.parent_id else ''
            elif line.lang_code != 'en_US' and line.partner_id:
                res_partner = self.env['res.partner'].search([('id', '=', line.partner_id.id)])
                if res_partner:
                    for partner in res_partner:
                        partner_name = (partner.last_name + ' 様') if partner.last_name else ''
                        company_name = ('株式会社 ' + partner.parent_id.name + ' 御中') if partner.parent_id else ''
            
            if 'send_to_people' in line:
                line.send_to_people = partner_name
            if 'send_to_company' in line:
                line.send_to_company = company_name
