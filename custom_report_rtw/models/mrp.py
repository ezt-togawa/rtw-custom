from odoo import fields, models
import pytz
from datetime import datetime

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    order_line=fields.One2many(
        "sale.order.line",
        "order_id",
        compute="_compute_get_sale_order_line",
    )
    mrp_production_parent_id = fields.One2many("mrp.production",compute="_compute_mrp_production_parent_id")
    mrp_production_so_id = fields.One2many("sale.order",compute="_compute_mrp_production_so_id")
    mrp_production_order_line = fields.One2many('sale.order.line',compute="_compute_mrp_production_order_line")
    
    mrp_product_name=fields.Char("mrp product name",compute="_compute_mrp_product_name")
    mrp_product_no=fields.Char("mrp product no",compute="_compute_mrp_product_no")
    mrp_product_name_excel=fields.Char("mrp product name",compute="_compute_mrp_product_name_excel")
    mrp_product_config_cus_excel = fields.Char("mrp product config cus excel",compute="_compute_mrp_product_config_cus_excel")
    mrp_product_type = fields.Char("mrp product type",compute="_compute_mrp_product_type")
    mrp_product_attribute = fields.Char("mrp product attribute",compute="_compute_mrp_product_attribute")
    mrp_product_attribute2 = fields.Char("mrp product attribute 2",compute="_compute_mrp_product_attribute")
    mrp_product_attribute_summary = fields.Char("mrp product attribute summary",compute="_compute_mrp_product_attribute_summary")
    mrp_product_product_qty = fields.Char(compute="_compute_mrp_product_product_qty")
    mrp_workorder_state = fields.Char(compute="_compute_mrp_workorder_state")
    mrp_production_date_planned_start = fields.Date(compute="_compute_mrp_production_date_planned_start")
    current_print = fields.Char(compute="_compute_current_print")
    
    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            
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
                    sale_order_line = self.env['sale.order.line'].search([search], limit=1)
                    break
                
            record.mrp_production_order_line = sale_order_line

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
        
    def _compute_mrp_product_no(self):   
        for line in self:
            product_no = ""
            if line.product_id and line.product_id.product_tmpl_id: 
                prod_tmpl =line.product_id.product_tmpl_id
                if prod_tmpl.config_ok and prod_tmpl.product_no:
                    product_no = prod_tmpl.product_no
                else: 
                    product_no  =  ""
            line.mrp_product_no = product_no
            
    def _compute_mrp_product_name(self):   
        for line in self:
            product_name = ""
            if line.product_id and line.product_id.product_tmpl_id: 
                prod_tmpl =line.product_id.product_tmpl_id
                if prod_tmpl.name:
                    product_name = prod_tmpl.name
                else: 
                    product_name =  ""
            line.mrp_product_name = product_name      
             
    def _compute_mrp_product_config_cus_excel(self):
        for line in self:
            config = ""

            if line.origin and line.origin.startswith('S'):
                so = self.env['sale.order'].search([("name", '=', line.sale_reference)])
                if so:
                    sol = self.env['sale.order.line'].search([
                    ("order_id", "=", so.id),
                    ("product_id", "=", line.product_id.id)
                ], limit=1)
                    if sol:
                        for l in sol:
                            if l.config_session_id.custom_value_ids:
                                for cfg in l.config_session_id.custom_value_ids:
                                    if cfg.display_name:
                                        config += "●" + cfg.display_name
                                config = config.rstrip('\n')

            line.mrp_product_config_cus_excel = config.strip()
                
    def _compute_mrp_product_type(self):
        for line in self:
            p_type = ""
            if line.origin and line.origin.startswith('S'):
                so = self.env['sale.order'].search([("name",'=',line.sale_reference)])
                if so:
                    sol = self.env['sale.order.line'].search([
                    ("order_id", "=", so.id),
                    ("product_id", "=", line.product_id.id)
                ], limit=1)
                    if sol:
                        for l in sol:
                            if l.p_type:
                                if l.p_type == "special":
                                    p_type = "[別注]"
                                elif l.p_type == "custom":
                                    p_type = "[特注]"
            line.mrp_product_type = p_type
        
    def _compute_mrp_product_name_excel(self):   
        for line in self: 
            prod = line.product_id
            
            detail = ""
            product_name = ""
            type = line.mrp_product_type
            size = ""
            if prod: 
                prod_tmpl = prod.product_tmpl_id
                if prod_tmpl:
                    if prod_tmpl.config_ok :  
                        if prod_tmpl.name :
                            product_name = prod_tmpl.name
                        else: 
                            product_name = ""   
                    else:
                        product_name = prod_tmpl.name

            if line.mrp_production_order_line and line.mrp_production_order_line.product_size:
                size += line.mrp_production_order_line.product_size
            has_attribute = bool(line.mrp_product_attribute and line.mrp_product_attribute.strip())
            
            if has_attribute:
                if product_name and type:
                    detail += type + ' ' + product_name
                elif product_name:
                    detail += product_name
                if size:
                    detail += "\n\n" + size
            else:
                if product_name and type:
                    detail += type + ' ' + product_name
                elif product_name:
                    detail += product_name
                if size:
                    detail += size
            
            line.mrp_product_name_excel = detail 

    def _compute_mrp_production_parent_id(self):
        for record in self:
            mrp_parent = False
            if record.origin and '/MO/' in record.origin:
                mrp_parent_id = self.env['mrp.production'].search([('name', '=', record.origin)], limit=1)
                if mrp_parent_id:
                    mrp_parent = mrp_parent_id
                    
            record.mrp_production_parent_id = mrp_parent
    
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
                record.mrp_production_date_planned_start = record._convert_timezone(record.date_planned_start)
            else:
                record.mrp_production_date_planned_start = ''
                
    def _convert_timezone(self, date):            
        timezone = pytz.timezone(self.env.user.tz or 'UTC')
        utc_dt = fields.Datetime.from_string(date)
        return utc_dt.astimezone(timezone)
                
    def _compute_mrp_product_attribute(self):
        for line in self:
            attr_column1 = ""
            attr_column2 = ""
            
            attributes = line.product_id.product_template_attribute_value_ids  # existing attr 
            attributes_cfg = [] 
            sol = line.mrp_production_order_line
            if sol:
                attributes_cfg = sol[0].config_session_id.custom_value_ids     # custom attr
                
            attr_list = [{"attribute_id": attr.attribute_id.id, "display_name": attr.display_name} for attr in attributes]
            attr_cfg_list = [{"attribute_id": attr.attribute_id.id, "display_name": attr.display_name} for attr in attributes_cfg]
            
            # sort order by id 
            sort_order_id = []
            for sort in line.product_id.attribute_line_ids:
                sort_order_id.append(sort.attribute_id.id)
            
            attr_all = sorted(attr_list + attr_cfg_list, key=lambda x: sort_order_id.index(x['attribute_id']) if x['attribute_id'] in sort_order_id else float('inf'))
            
            if len(attr_all) < 7:
                for a in attr_all:
                    attr_column1 += ("・ " + a["display_name"] + "\n" )
            else:
                for a in attr_all[:6]:
                    attr_column1 += ("・ " + a["display_name"] + "\n" )
                for a in attr_all[6:12]:
                    attr_column2 += ("・ " + a["display_name"] + "\n" )
            
            line.mrp_product_attribute = attr_column1.rstrip("\n") 
            line.mrp_product_attribute2 = attr_column2.rstrip("\n") 

