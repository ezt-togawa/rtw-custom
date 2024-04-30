# # -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api
import re

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
    
    @api.onchange('multiplier_green')
    def check_combo_box_price_list_multiplier_green(self):
        for partner in self:
            if partner.multiplier_green:
                
                check = False
                price_list = self.env['product.pricelist'].search([])
                for line in price_list:
                    if re.search(str(int(partner.multiplier_green)) , line.name):
                        check = True
                        break
                if check:
                    partner.property_product_pricelist = line.id
                    
                else:
                    dummy_price_list = self.env['product.pricelist'].search([('name', '=', '※未指定')])
                    
                    if dummy_price_list and dummy_price_list[0].currency_id.name == "JPY" :
                        
                        partner.property_product_pricelist = dummy_price_list[0].id 
                        
                    else:
                        currency = self.env['res.currency'].search([('name', '=', 'JPY')])
                        new_price_list = self.env['product.pricelist'].create({'name': '※未指定','currency_id':currency[0].id})
                        partner.property_product_pricelist = new_price_list.id
                        
    @api.onchange('property_product_pricelist')
    def check_property_product_pricelist(self):
        for partner in self:
            if not partner.property_product_pricelist :
                dummy_price_list = self.env['product.pricelist'].search([('name', '=', '※未指定')])
                    
                if dummy_price_list:
                    partner.property_product_pricelist = dummy_price_list[0].id 
                    
                else:
                    currency = self.env['res.currency'].search([('name', '=', 'JPY')])
                    new_price_list = self.env['product.pricelist'].create({'name': '※未指定','currency_id':currency[0].id})
                    partner.property_product_pricelist = new_price_list.id
