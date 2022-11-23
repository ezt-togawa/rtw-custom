# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_dm_crm(models.Model):
    _inherit = 'crm.lead'

    last_name = fields.Char(related="partner_id.last_name")
    first_name = fields.Char(related="partner_id.first_name")
    in_has = fields.Char(related="partner_id.in_has")
    mailing_postal_code = fields.Char(related="partner_id.mailing_postal_code")
    mailing_state = fields.Char(related="partner_id.mailing_state")
    mailing_city = fields.Char(related="partner_id.mailing_city")
    mailing_street = fields.Char(related="partner_id.mailing_street")
    fax = fields.Char(related="partner_id.fax")
    parent_id = fields.Many2one(related="partner_id.parent_id")
    department = fields.Char(related="partner_id.department")
    title = fields.Many2one(related="partner_id.title")
    calender = fields.Boolean(related="partner_id.calender")
    ny_card = fields.Boolean(related="partner_id.ny_card")

