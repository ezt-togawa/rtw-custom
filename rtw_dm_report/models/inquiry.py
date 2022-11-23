# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_dm_inq(models.Model):
    _inherit = 'rtw_sf.inquiry'

    user_id = fields.Many2one(related="contact_person.user_id")
    last_name = fields.Char(related="contact_person.last_name")
    first_name = fields.Char(related="contact_person.first_name")
    in_has = fields.Char(related="contact_person.in_has")
    zip = fields.Char(related="contact_person.zip")
    state_id = fields.Many2one(related="contact_person.state_id")
    city = fields.Char(related="contact_person.city")
    street = fields.Char(related="contact_person.street")
    street2 = fields.Char(related="contact_person.street2")
    mailing_postal_code = fields.Char(related="contact_person.mailing_postal_code")
    mailing_state = fields.Char(related="contact_person.mailing_state")
    mailing_city = fields.Char(related="contact_person.mailing_city")
    mailing_street = fields.Char(related="contact_person.mailing_street")
    phone = fields.Char(related="contact_person.phone")
    mobile = fields.Char(related="contact_person.mobile")
    fax = fields.Char(related="contact_person.fax")
    parent_id = fields.Many2one(related="contact_person.parent_id")
    department = fields.Char(related="contact_person.department")
    title = fields.Many2one(related="contact_person.title")
    calender = fields.Boolean(related="contact_person.calender")
    ny_card = fields.Boolean(related="contact_person.ny_card")
