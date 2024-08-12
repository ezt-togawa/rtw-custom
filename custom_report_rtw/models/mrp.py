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
  
  mrp_production_order_line = fields.One2many(
      'sale.order.line',
      compute="_compute_mrp_production_order_line"
  )
  
  mrp_product_product_qty = fields.Char(string="mrp product product qty" , compute="_compute_mrp_product_product_qty")
  
  mrp_workorder_state = fields.Char(
      compute="_compute_mrp_workorder_state"
  )
  
  def _compute_mrp_workorder_state(self):
    for record in self:
        wk_001 = self.env['mrp.workcenter'].search([('code','=','wk_001')], limit=1)
        wk_002 = self.env['mrp.workcenter'].search([('code','=','wk_002')], limit=1)
        mrp_workorder_state = False
        for workorder in record.workorder_ids:
            if workorder.workcenter_id.id == wk_001.id:
                mrp_workorder_state = 'wk_001'
                break
            if workorder.workcenter_id.id == wk_002.id: 
                mrp_workorder_state = 'wk_002'
                break
        record.mrp_workorder_state = mrp_workorder_state
  
  def _compute_mrp_production_order_line(self):
     for record in self:      
       sale_order_line = False
       search_criteria = [ #limit 10 times
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
           ('move_ids', 'in', [move_id.id for move_id in record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
       ]

       for search in search_criteria: #find sale_order_line
           if self.env['sale.order.line'].search([search]):
               sale_order_line = self.env['sale.order.line'].search([search])
               break
           
       if sale_order_line:
           record.mrp_production_order_line = sale_order_line
       else:
          record.mrp_production_order_line = False
  
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
      for record in self:
        sale_order = self.env['sale.order'].search([('name','=',record.origin)])
        order_lines = self.env["sale.order.line"].search([("order_id", "in", sale_order.ids)])

        record.order_line = order_lines
      
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
            mrp_prod_detail =  ''   
            type = line.mrp_product_type
            config = ""

            if line.origin and line.origin.startswith('S'):
                so = self.env['sale.order'].search([("name", '=', line.sale_reference)])
                if so:
                    sol = self.env['sale.order.line'].search([("order_id", '=', so[0].id)])
                    if sol:
                        for l in sol:
                            if l.config_session_id.custom_value_ids:
                                for cfg in l.config_session_id.custom_value_ids:
                                    config += "● " + cfg.display_name  + ":" + cfg.value  + "\n"
                                config = config.rstrip('\n')
                
            if type and config:
                mrp_prod_detail = type + '\n' + config
            elif type :
                mrp_prod_detail = type 
            elif config:
                mrp_prod_detail = config
                    
            line.mrp_product_config_cus_excel = mrp_prod_detail.strip()
            
  def _compute_mrp_product_type(self):
      for line in self:
          p_type = ""
          if line.origin and line.origin.startswith('S'):
            so = self.env['sale.order'].search([("name",'=',line.sale_reference)])
            if so:
                sol = self.env['sale.order.line'].search([("order_id",'=',so[0].id)])
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
        prod = line.product_id
        
        detail = ""
        name = ""
        summary = ""
        size = ""
        type = ""
        if prod: 
            prod_tmpl = prod.product_tmpl_id
            if prod_tmpl:
                if prod_tmpl.config_ok :  
                    if prod_tmpl.product_no :
                        name = prod_tmpl.product_no
                    else: 
                        name = prod_tmpl.name   
                else:
                    name = prod_tmpl.name
            if prod.summary:
                summary = prod.summary
                
        if line.mrp_production_order_line and line.mrp_production_order_line.product_size:
            size += line.mrp_production_order_line.product_size
            
        type = line.mrp_product_type
            
        if name and summary and type :
            detail += name +'\n' + summary +'\n' + type
        elif name and summary:
            detail += name +'\n' + summary
        elif name and type:
            detail += name +'\n' + type
        elif summary and type:
            detail += summary +'\n' + type
        elif name :
            detail += name 
        elif name :
            summary += summary
        elif type :
            detail += type 
                
        if size:
            detail += "\n" + size
                
        line.mrp_product_name_excel = detail 

  def _compute_mrp_production_parent_id(self):
      for record in self:
        if record.origin and '/MO/' in record.origin:
            mrp_parent_id = self.env['mrp.production'].search([('name','=',record.origin)],limit=1)
            if mrp_parent_id:
                record.mrp_production_parent_id = mrp_parent_id
            else:
                record.mrp_production_parent_id = False
        else:
            record.mrp_production_parent_id = False
  
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
      for record in self:
        if record.date_planned_start:
            record.mrp_production_date_planned_start = record.date_planned_start.date()
        else:
            record.mrp_production_date_planned_start = ''
  def _compute_mrp_product_attribute(self):
      for line in self:
            attr_column1 = ""
            attr_column2 = ""
            attr_all = ""
            
            if line.product_id and line.product_id.product_template_attribute_value_ids:
                attributes = line.product_id.product_template_attribute_value_ids 
                len_attributes = len(attributes)

                if len_attributes <= 6:
                    for attr in attributes:
                        attr_column1 += f"● {attr.display_name}\n"                    
                else:
                    for attr in attributes[:6]:
                        attr_column1 += f"● {attr.display_name}\n"
                    for attr in attributes[6:12]:
                        attr_column2 += f"● {attr.display_name}\n"
                        
                for attr in attributes:
                    attr_all += f"● {attr.display_name}\n"                    
                        
                attr_column1 = attr_column1.rstrip()
                attr_column2 = attr_column2.rstrip()
            
            line.mrp_product_attribute = attr_column1
            line.mrp_product_attribute2 = attr_column2

