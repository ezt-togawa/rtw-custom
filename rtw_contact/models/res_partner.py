# # -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
    
    @api.model
    def init(self):
        super(rtw_sf_partner, self).init()
        self.update_jp_name()

    # update jp_name for fields: transactions ,payment_terms_1 ,payment_terms_2 
    def update_jp_name(self):
        jp_name_list = self.env['ir.translation'].search([('module','=','rtw_sf'),('lang','=','ja_JP'),('src', 'in', ['transactions', 'payment_terms_1', 'payment_terms_2']) ])
        for line in jp_name_list:
            if line.value.strip() == "支払条件":
                line.value = "取引条件"
            if line.value.strip() == "支払い条件１":
                line.value = "取引条件1"
            if line.value.strip()  == "支払い条件2":
                line.value = "取引条件2"
