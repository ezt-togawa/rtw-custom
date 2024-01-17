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

    send_to_company = fields.Char(string="send to company" , compute="_compute_send_to")
    send_to_people = fields.Char(string="send to people" , compute="_compute_send_to")
    
    def _compute_send_to(self):
        for l in self:
            if l.lang_code == 'en_US':
                l.send_to_people = ('Mr./Mrs. ' + l.partner_id.name) if l.partner_id and l.partner_id.name else ''
                l.send_to_company = ('御中 ' + l.partner_id.company_id.name  + ' 株式会社') if l.partner_id and l.partner_id.company_id else ''
            else:
                l.send_to_people = (l.partner_id.name +' 様') if l.partner_id and l.partner_id.name else ''
                l.send_to_company = ('株式会社 ' + l.partner_id.company_id.name  + ' 御中') if l.partner_id and l.partner_id.company_id else ''
                