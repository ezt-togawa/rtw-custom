# -*- coding: utf-8 -*-

from odoo import fields, models

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
  
  # mrp_product_config_cus = fields.Char(
  #     "mrp product config cus",
  #     compute="_compute_mrp_product_config_cus",
  # )
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
  
  mrp_production_parent_id = fields.One2many(
      "mrp.production",
      compute="_compute_mrp_production_parent_id",
  )
  
  mrp_production_so_id = fields.One2many(
      "sale.order",
      compute="_compute_mrp_production_so_id",
  )
  
  mrp_product_product_qty = fields.Char(string="mrp product product qty" , compute="_compute_mrp_product_product_qty")
  
  def _compute_mrp_product_product_qty(self):
      for line in self:
          float_product_qty = float(line.product_qty)
          integer_part = int(line.product_qty)
          decimal_part = round(float_product_qty - integer_part,2)
          decimal_part_after_dot = int(str(decimal_part).split('.')[1])
          if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
              line.mrp_product_product_qty = integer_part
          else:
              while decimal_part_after_dot % 10 == 0:
                  decimal_part_after_dot = decimal_part_after_dot / 10
              line.mrp_product_product_qty =  integer_part + float('0.' + str(decimal_part_after_dot))

  def _compute_get_sale_order_line(self):
      sale_order = self.env['sale.order'].search([('name','=',self.origin)])
      order_lines = self.env["sale.order.line"].search([("order_id", "in", sale_order.ids)])
      
      self.order_line = order_lines
      
  def _compute_mrp_product_name(self):   
      for line in self:
          name = ""
          if line.product_id: 
              if line.product_id.product_tmpl_id.config_ok :
                  if line.product_id.product_tmpl_id.product_no :
                      name = line.product_id.product_tmpl_id.product_no
                  else: 
                      name = line.product_id.product_tmpl_id.name   
              else:
                  name = line.product_id.product_tmpl_id.name
          line.mrp_product_name = name
          

  # def _compute_mrp_product_config_cus(self):
  #     for line in self:
  #         config=""
  #         so=self.env['sale.order'].search([("name",'=',line.sale_reference)])
  #         if so:
  #             sol=self.env['sale.order.line'].search([("order_id",'=',so[0].id)])
  #             if sol:
  #                 for l in sol:
  #                     configCus=l.config_session_id.custom_value_ids
  #                     if configCus:
  #                         for cfg in configCus:
  #                             config += cfg.display_name + ":" + cfg.value + "\n"
  #                     config.rstrip("\n")
  #         line.mrp_product_config_cus = config

          
  def _compute_mrp_product_config_cus_excel(self):
      for line in self:
          if line.origin.startswith('WH'):
              line.mrp_product_config_cus_excel =""
          else:
              type = line.mrp_product_type
              config =""
              so=self.env['sale.order'].search([("name",'=',line.sale_reference)])
              if so:
                  sol=self.env['sale.order.line'].search([("order_id",'=',so[0].id)])
                  if sol:
                      for l in sol:
                          if l.config_session_id.custom_value_ids:
                              for cfg in l.config_session_id.custom_value_ids:
                                  config += cfg.display_name + ':' + cfg.value + '\n'
                              config = config.rstrip('\n')
              if type :
                  line.mrp_product_config_cus_excel = type + '\n' + config
              else:
                  line.mrp_product_config_cus_excel = config
          
  def _compute_mrp_product_type(self):
      for line in self:
          if line.origin.startswith('WH'):
              line.mrp_product_type = ""
              return
          
          p_type = ""
          so=self.env['sale.order'].search([("name",'=',line.sale_reference)])
          if so:
              sol=self.env['sale.order.line'].search([("order_id",'=',so[0].id)])
              if sol:
                  for l in sol:
                      if l.p_type:
                          if l.p_type == "special":
                              p_type = "別注"
                          elif l.p_type == "custom":
                              p_type = "特注"
          line.mrp_product_type = p_type
      
  def _compute_mrp_product_name_excel(self):   
      for line in self:
          name = ""
          if line.product_id: 
              if line.product_id.product_tmpl_id.config_ok :  
                  if line.product_id.product_tmpl_id.product_no :
                      name = line.product_id.product_tmpl_id.product_no
                  else: 
                      name = line.product_id.product_tmpl_id.name   
              else:
                  name = line.product_id.product_tmpl_id.name
                  
          type =""        
          if line.origin.startswith('WH'):
              type =""
          else:
              type = line.mrp_product_type
                  
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

  def _compute_mrp_production_parent_id(self):
      if self.origin and '/MO/' in self.origin:
          mrp_parent_id = self.env['mrp.production'].search([('name','=',self.origin)],limit=1)
          if mrp_parent_id:
              self.mrp_production_parent_id = mrp_parent_id
          else:
              self.mrp_production_parent_id = False
      else:
          self.mrp_production_parent_id = False
  
  def _get_so_from_mrp(self , mrp_production , count = 0):
        if count >= 10:
            return False
        if not mrp_production.origin:
            return False
        
        sale_order_id = False
        if '/MO/' in mrp_production.origin:
            mrp = self.env['mrp.production'].search([('name','=',mrp_production.origin)])
            if mrp:
                count += 1
                sale_order_id = self._get_so_from_mrp(mrp, count)
        else:
            sale_order_id = self.env['sale.order'].search([('name','=',mrp_production.origin)])
        return sale_order_id
  
  def _compute_mrp_production_so_id(self):
      for record in self:
        record.mrp_production_so_id = self._get_so_from_mrp(record)
        