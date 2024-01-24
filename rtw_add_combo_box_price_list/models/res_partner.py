# # -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
    
    @api.onchange('multiplier_green')
    def check_combo_box_price_list_multiplier_green(self):
        for partner in self:
            if partner.multiplier_green:
                price_list = self.env['product.pricelist'].search([])
                for line in price_list:
                    if str(int(partner.multiplier_green)) in line.name:
                        partner.property_product_pricelist = line.id
                        return
                    else:
                        partner.property_product_pricelist = False
                        
                        
