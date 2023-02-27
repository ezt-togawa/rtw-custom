# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_presence_image(models.Model):
    _name = 'rtw_presence.image'
    _description = 'rtw_presence.image'
    _rec_name = "name"

    name = fields.Char()
    image_1920 = fields.Image(
        "Image", max_width=1920, max_height=1920, required=True, attachment=True
    )
    image_128 = fields.Image(
        "Small Image", related="image_1920", max_width=128, max_height=128, store=True
    )
    presence_id = fields.Many2one('rtw_presence.presence')

