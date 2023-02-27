# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_presence(models.Model):
    _name = 'rtw_presence.presence'
    _description = 'rtw_presence.rtw_presence'

    name = fields.Char('Name')
    done = fields.Boolean('Done')
    date = fields.Date('Date')
    owner_id = fields.Many2many('res.users', string="Owner ID")
    presence_person_id = fields.Many2one('rtw_presence.person', "Presence Person")
    note = fields.Text('Note')
    image_ids = fields.One2many(comodel_name="rtw_presence.image",
                                inverse_name="presence_id",
                                string="image")
    crm_id = fields.Many2one('crm.lead', string='CRM')
    image_count = fields.Integer("Image Count", compute="_compute_image_count")

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    def _compute_image_count(self):
        for line in self:
            line.image_count = len(line.image_ids)
