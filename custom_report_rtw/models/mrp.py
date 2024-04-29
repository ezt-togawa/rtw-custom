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
  
  mrp_product_attribute2 = fields.Char(
      "mrp product attribute 2",
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
  
  mrp_production_date_planned_start = fields.Date(
      string='date planned start',
      compute="_compute_mrp_production_date_planned_start"
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
          
  def _compute_mrp_product_config_cus_excel(self):
        for line in self:
            if line.origin and line.origin.startswith('WH'):
                line.mrp_product_config_cus_excel = ""
            else:
                type = line.mrp_product_type
                config = ""
                so = self.env['sale.order'].search([("name", '=', line.sale_reference)])
                if so:
                    sol = self.env['sale.order.line'].search([("order_id", '=', so[0].id)])
                    if sol:
                        for l in sol:
                            if l.config_session_id.custom_value_ids:
                                for cfg in l.config_session_id.custom_value_ids:
                                    config += cfg.display_name + ':' + cfg.value + '\n'
                                config = config.rstrip('\n')
                                
                mrp_prod_detail =  ''   
                if type and config:
                    mrp_prod_detail = type + '\n' + config
                elif type :
                     mrp_prod_detail = type 
                elif config:
                    mrp_prod_detail = config
                    
                line.mrp_product_config_cus_excel = mrp_prod_detail
            
  def _compute_mrp_product_type(self):
      for line in self:
          if line.origin and line.origin.startswith('WH'):
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
        detail = ""
        prod_id = line.product_id
        prod_tmpl_id = line.product_id.product_tmpl_id
        
        name = ""
        if prod_id and prod_tmpl_id: 
            if prod_tmpl_id.config_ok :  
                if prod_tmpl_id.product_no :
                    name = prod_tmpl_id.product_no
                else: 
                    name = prod_tmpl_id.name   
            else:
                name = prod_tmpl_id.name
                
        type = ""        
        if line.origin and line.origin.startswith('WH'):
            type = ""
        else:
            type = line.mrp_product_type
            
        if name and type :
            detail += name +'\n' + type
        elif name :
            detail += name
        elif type :
            detail += type 
                
        size = ''
        if prod_id and prod_tmpl_id:
            if prod_tmpl_id.width:
                size += "W" + str(prod_tmpl_id.width) + "*"
            if prod_tmpl_id.depth:
                size += "D" + str(prod_tmpl_id.depth) + "*"
            if prod_tmpl_id.height:
                size += "H" + str(prod_tmpl_id.height) + "*"
            if prod_tmpl_id.sh:
                size += "SH" + str(prod_tmpl_id.sh) + "*"
            if prod_tmpl_id.ah:
                size += "AH" + str(prod_tmpl_id.ah)
            size = size.rstrip("*")
            
        if size:
            detail += "\n" + size
                
        line.mrp_product_name_excel = detail 
          


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
                       
  def _compute_mrp_production_date_planned_start(self):
      if self.date_planned_start:
          self.mrp_production_date_planned_start = self.date_planned_start.date()
      else:
          self.mrp_production_date_planned_start = ''
  def _compute_mrp_product_attribute(self):
      for line in self:
            attr = ""
            attr_cfg = ""
            
            attributes = line.product_id.product_template_attribute_value_ids  #attr default
            attributes_cfg = [] 
            
            so = self.env['sale.order'].search([("name", '=', line.sale_reference)])
            if so:
                sol = self.env['sale.order.line'].search([("order_id", '=', so[0].id),("product_id", '=',line.product_id.id)])
                if sol:
                    attributes_cfg = sol[0].config_session_id.custom_value_ids #attr custom 
                    
            length_normal = len(attributes)
            
            if attributes:
                if length_normal < 6:
                    for attribute in attributes:
                        attr += ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" )                    
                    if attributes_cfg:
                        count_cfg = 0 
                        count_attr = length_normal
                        for cfg in attributes_cfg:
                            if count_attr >= 6 :
                                break
                            else:
                                count_attr +=1
                            attr += ("● " + cfg.display_name  + ":" + cfg.value  + "\n" )
                            count_cfg += 1
                            
                        for cfg2 in attributes_cfg[count_cfg:(6+count_cfg)]:
                            attr_cfg += ("● " + cfg2.display_name  + ":" + cfg2.value  + "\n" )
                elif length_normal == 6 :
                    for attribute in attributes:
                        attr += ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" )                    
                    if attributes_cfg:                            
                        for cfg in attributes_cfg:
                            attr_cfg += ("● " + cfg.display_name  + ":" + cfg.value  + "\n" )
                else:
                    for attribute in attributes[:6]:
                        attr += ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" )
                    start = 6   
                    for attribute in attributes[6:length_normal]:
                        attr_cfg +=  ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" )
                        start += 1
                    if length_normal < 12 : 
                        if attributes_cfg:
                            for cfg in attributes_cfg[:(12-start)]:
                                attr_cfg += ("● " + cfg.display_name  + ":" + cfg.value  + "\n" )
            else: 
                if attributes_cfg:                            
                    for cfg in attributes_cfg[:6]:
                        attr += ("● " +  cfg.display_name  + ":" + cfg.value  + "\n" )
                    for cfg in attributes_cfg[6:12]:
                        attr_cfg += ("● " +  cfg.display_name  + ":" + cfg.value  + "\n" )
                        
            attr = attr.rstrip()
            attr_cfg = attr_cfg.rstrip() 
            
            line.mrp_product_attribute = attr
            line.mrp_product_attribute2 = attr_cfg
    