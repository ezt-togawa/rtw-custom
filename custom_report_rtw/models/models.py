# -*- coding: utf-8 -*-

from odoo import fields, models
import math
from bs4 import BeautifulSoup
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    calculate_shiratani_date = fields.Char('Shiratani Date' , compute="_compute_get_sale_order")
    calculate_witness = fields.Char('Witness' , compute="_compute_get_sale_order")
    calculate_witness_phone = fields.Char('Witness Phone' , compute="_compute_get_sale_order")
    pic_name = fields.Char('PIC Name' , compute="_compute_get_sale_order")
    calculate_name = fields.Char('Name' , compute="_compute_get_sale_order")
    calculate_note = fields.Char('Note' , compute="_compute_get_sale_order")
    calculate_estimated_shipping_date = fields.Char('Estimated Shipping Date' , compute="_compute_get_sale_order")
    calculate_payment_term = fields.Char('Payment term' , compute="_compute_get_sale_order")
    sale_orders=fields.One2many(
        "sale.order",
        "origin",
        string="Sale order",
        compute="_compute_get_sale_order",
    )
    

    def _compute_get_sale_order(self):
        sale_order = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        if not sale_order:
            sale_order = self.env['sale.order'].search([('name','=',self.origin)])
                    
        if sale_order:
            self.calculate_shiratani_date = sale_order.shiratani_entry_date
            self.calculate_witness = sale_order.witness
            self.calculate_witness_phone = sale_order.witness_phone
            self.pic_name = sale_order.user_id.name
            self.calculate_name = sale_order.title
            self.calculate_note = sale_order.note
            self.calculate_estimated_shipping_date = sale_order.estimated_shipping_date
            self.calculate_payment_term = sale_order.payment_term_id.name
            self.sale_orders =sale_order
        else:
            self.calculate_shiratani_date = ''
            self.calculate_witness = ''
            self.calculate_witness_phone = ''
            self.pic_name = ''
            self.calculate_name = ''
            self.calculate_note = ''
            self.calculate_estimated_shipping_date = ''
            self.calculate_payment_term = ''

class StockMove(models.Model):
  _inherit = 'stock.move'
  calculate_packages = fields.Integer('Packages' , compute="_compute_calculate_packages")
 
  def _compute_calculate_packages(self):
    for move in self:
        if move.product_id.two_legs_scale:
            move.calculate_packages = math.ceil(move.product_uom_qty / move.product_id.two_legs_scale)
        else:
            move.calculate_packages = move.product_uom_qty

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    order_line=fields.One2many(
        "sale.order.line",
        "order_id",
        string="Sale order line",
        compute="_compute_get_sale_order_line",
    )

    mrp_product_name=fields.Char(
        "mrp product name",
        compute="_compute_mrp_product_name",
    )
    
    mrp_product_name_excel=fields.Char(
        "mrp product name",
        compute="_compute_mrp_product_name_excel",
    )
    
    mrp_product_config_cus = fields.Char(
        "mrp product config cus",
        compute="_compute_mrp_product_config_cus",
    )
    mrp_product_config_cus_excel = fields.Char(
        "mrp product config cus excel",
        compute="_compute_mrp_product_config_cus_excel",
    )
    
    mrp_product_type = fields.Char(
        "mrp product type",
        compute="_compute_mrp_product_type",
    )
    
    mrp_product_attribute = fields.Char(
        "mrp product attribute",
        compute="_compute_mrp_product_attribute",
    )
    
    mrp_product_attribute_summary = fields.Char(
        "mrp product attribute summary",
        compute="_compute_mrp_product_attribute_summary",
    )

    def _compute_get_sale_order_line(self):        
        sale_order = self.env['sale.order'].search([('name','=',self.origin)])
        order_lines = self.env["sale.order.line"].search([("order_id", "in", sale_order.ids)])
        
        self.order_line = order_lines
        
    def _compute_mrp_product_name(self):   
        for line in self:
            name = ""
            if line.product_id: 
                if line.product_id.product_tmpl_id.config_ok :  
                    if line.product_id.product_tmpl_id.categ_id.name:
                        name = line.product_id.product_tmpl_id.categ_id.name
                    elif line.product_id.product_tmpl_id.product_no :
                        name = line.product_id.product_tmpl_id.product_no
                    else: 
                        name = line.product_id.product_tmpl_id.name   
                else:
                    # case product is standard Prod 
                    name = line.product_id.product_tmpl_id.name
            line.mrp_product_name = name
            

    def _compute_mrp_product_config_cus(self):
        for line in self:
            config_cus = []
            if line.production_type:
                soup = BeautifulSoup(line.production_type, 'html.parser')
                for div in soup.find_all('div'):
                    text = div.get_text(strip=True)
                    config_cus.append(text)
            line.mrp_product_config_cus = "\n".join(config_cus)
            
    def _compute_mrp_product_config_cus_excel(self):
        for line in self:
            if line.origin.startswith('WH'):
                type =""
            else:
                if line.product_id.type=='consu':
                    type = 'Consumable'
                if line.product_id.type=='service':
                    type = 'Service'
                if line.product_id.type=='product':
                    type = 'Storable product'
            
            config_cus = []
            if line.production_type:
                soup = BeautifulSoup(line.production_type, 'html.parser')
                for div in soup.find_all('div'):
                    text = div.get_text(strip=True)
                    config_cus.append(text)
            if type :
                line.mrp_product_config_cus_excel = type + '\n' +"\n".join(config_cus)
            else:
                line.mrp_product_config_cus_excel = "\n".join(config_cus)
            
    def _compute_mrp_product_type(self):
        for line in self:
            if line.origin.startswith('WH'):
                line.mrp_product_type = ""
            else:
                type = ''
                if line.product_id.type == 'consu':
                    type = 'Consumable'
                elif line.product_id.type == 'service':
                    type = 'Service'
                elif line.product_id.type == 'product':
                    type = 'Storable product'
                line.mrp_product_type = type

            
    def _compute_mrp_product_name_excel(self):   
        for line in self:
            name = ""
            if line.product_id: 
                if line.product_id.product_tmpl_id.config_ok :  
                    if line.product_id.product_tmpl_id.categ_id.name:
                        name = line.product_id.product_tmpl_id.categ_id.name
                    elif line.product_id.product_tmpl_id.product_no :
                        name = line.product_id.product_tmpl_id.product_no
                    else: 
                        name = line.product_id.product_tmpl_id.name   
                else:
                    name = line.product_id.product_tmpl_id.name
                    
            type =""        
            if line.origin.startswith('WH'):
                type =""
            else:
                if line.product_id.type=='consu':
                    type = 'Consumable'
                if line.product_id.type=='service':
                    type = 'Service'
                if line.product_id.type=='product':
                    type = 'Storable product'
        
            size=""
            if line.product_id.product_tmpl_id.width:
                size += "W" + str(line.product_id.product_tmpl_id.width) + "*"
            if line.product_id.product_tmpl_id.depth:
                size += "D" + str(line.product_id.product_tmpl_id.depth) + "*"
            if line.product_id.product_tmpl_id.height:
                size += "H" + str(line.product_id.product_tmpl_id.height) + "*"
            if line.product_id.product_tmpl_id.sh:
                size += "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
            if line.product_id.product_tmpl_id.ah:
                size += "AH" + str(line.product_id.product_tmpl_id.ah)
                
            detail = ''
            if name :
                detail += name +'\n'
                if type :
                    detail += type + '\n'
            else:
                if type :
                    detail += type + '\n'
            detail += size
                    
            line.mrp_product_name_excel = detail 
            
    def _compute_mrp_product_attribute(self):
        for line in self:
            attribute = ''
            attribute_summary = ''
            if line.product_id.product_template_attribute_value_ids:
                for attr in line.product_id.product_template_attribute_value_ids:
                    attribute += attr.display_name + '\n'
                    attribute_summary += attr.attribute_id.name +'\n'
            line.mrp_product_attribute = attribute
            line.mrp_product_attribute_summary = attribute_summary
                        