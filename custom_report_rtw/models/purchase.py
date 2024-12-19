from odoo import fields, models
from datetime import datetime 
from collections import defaultdict

class PurchaseOrderEmployee(models.Model):
    _inherit = 'purchase.order'
  
    hr_employee_company = fields.Char(string="hr employee company" , compute="_compute_hr_employee")
    hr_employee_department = fields.Char(string="hr employee department" , compute="_compute_hr_employee")
    hr_employee_zip = fields.Char(string="hr employee zip" , compute="_compute_hr_employee")
    hr_employee_info = fields.Char(string="hr employee info" , compute="_compute_hr_employee")
    hr_employee_country = fields.Char(string="hr employee country" , compute="_compute_hr_employee")
    hr_employee_tel = fields.Char(string="hr employee tel" , compute="_compute_hr_employee")
    hr_employee_fax = fields.Char(string="hr employee fax" , compute="_compute_hr_employee")
    hr_employee_printer = fields.Char(string="hr employee printer" , compute="_compute_hr_employee")
    current_print = fields.Char(compute="_compute_current_print")
    
    def check_duplicate(self , data):
        if data:
            arr = data.split(' , ')
            arr2 = []
            for item in arr:
                items_to_add = item.split(',') if ',' in item else [item]
                for sub_item in items_to_add:
                   if sub_item not in arr2:
                        arr2.append(sub_item)
            return ' , '.join(arr2)
    def generate_pdf(self):
        data = []
        list_order_line = []
        if self:
            for po in self:
                list_order_line += po.order_line
            if list_order_line:
                for ind, line in enumerate(list_order_line):
                    purchase_order_line = line.product_id
                    if purchase_order_line:
                        name_ir_data = self.env['ir.model.data'].search([('res_id', '=', purchase_order_line.id)], limit=1)
                        if name_ir_data:
                            data.append({
                               "purchase_order_index": line.purchase_order_index,
                               "ir_model_id": name_ir_data.name,
                               "purchase_order_prod_name": line.purchase_order_prod_name,
                               "purchase_order_line_product_uom_qty": line.purchase_order_line_product_uom_qty,
                               "product_uom_name": line.product_uom.name,
                               "display_type": line.display_type,
                               "purchase_order_sell_unit_price": line.purchase_order_sell_unit_price,
                               "price_subtotal": line.price_subtotal,
                               "product_template_attribute_value_ids": line.product_id.product_template_attribute_value_ids,
                               "name": line.name
                                })
                        else:
                            data.append({
                                "purchase_order_index": line.purchase_order_index,
                                "ir_model_id": None,
                                "purchase_order_prod_name": line.purchase_order_prod_name,
                                "purchase_order_line_product_uom_qty": line.purchase_order_line_product_uom_qty,
                                "product_uom_name": line.product_uom.name,
                                "display_type": line.display_type,
                                "purchase_order_sell_unit_price": line.purchase_order_sell_unit_price,
                                "price_subtotal": line.price_subtotal,
                                "product_template_attribute_value_ids": line.product_id.product_template_attribute_value_ids,
                                "name": line.name
                            })
                    else:
                        data.append({
                            "purchase_order_index": line.purchase_order_index,
                            "ir_model_id": None,
                            "purchase_order_prod_name": line.purchase_order_prod_name,
                            "purchase_order_line_product_uom_qty": line.purchase_order_line_product_uom_qty,
                            "product_uom_name": line.product_uom.name,
                            "display_type": line.display_type,
                            "purchase_order_sell_unit_price": line.purchase_order_sell_unit_price,
                            "price_subtotal": line.price_subtotal,
                            "product_template_attribute_value_ids": line.product_id.product_template_attribute_value_ids,
                            "name": line.name
                            })
                data_with_model_id = [item for item in data if item['ir_model_id'] is not None]
                data_without_model_id = [item for item in data if item['ir_model_id'] is None]
                def aggregate_purchase_data(data):
                    aggregated_data = defaultdict(lambda: {
                    "purchase_order_index": 0,
                    "purchase_order_prod_name": "",
                    "purchase_order_line_product_uom_qty": 0,
                    "product_uom_name": "",
                    "purchase_order_sell_unit_price": "",
                    "price_subtotal": 0
                })
                    for item in data:
                        key = item["ir_model_id"]
                        qty = float(item["purchase_order_line_product_uom_qty"].replace(",", ""))
                        subtotal = float(str(item["price_subtotal"]).replace(",", ""))
                        aggregated_data[key]["purchase_order_prod_name"] = item["purchase_order_prod_name"]
                        aggregated_data[key]["product_uom_name"] = item["product_uom_name"]
                        aggregated_data[key]["purchase_order_sell_unit_price"] = item["purchase_order_sell_unit_price"]
                        aggregated_data[key]["product_template_attribute_value_ids"] = item["product_template_attribute_value_ids"]
                        aggregated_data[key]["display_type"] = item["display_type"]
                        aggregated_data[key]["name"] = item["name"]
                        aggregated_data[key]["purchase_order_line_product_uom_qty"] += qty
                        aggregated_data[key]["price_subtotal"] += subtotal
                    result = []
                    for key, value in aggregated_data.items():
                        value["purchase_order_line_product_uom_qty"] = str(value["purchase_order_line_product_uom_qty"])
                        value["price_subtotal"] = f"{value['price_subtotal']:,}"
                        value["ir_model_id"] = key
                        result.append(value)
                        
                    return result
                result = aggregate_purchase_data(data_with_model_id) + data_without_model_id
            return result



    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            
    def _compute_hr_employee(self):
        for po in self:
            hr_defaults = {
                'hr_employee_company': "株式会社リッツウェル",
                'hr_employee_department': "大阪オフィス",
                'hr_employee_zip': "〒542-0081",
                'hr_employee_info': "大阪市中央区南船場4-7-6 B1F",
                'hr_employee_tel': "tel.06-4963-8777",
                'hr_employee_fax': "fax.06-4963-8778",
                'hr_employee_printer': po.purchase_order_printing_staff
            }

            if po.user_id:
                hr_employee = self.env['hr.employee'].search([('user_id','=',po.user_id.id)])
                if hr_employee:
                    for employee in hr_employee:
                        po.hr_employee_company = employee.company_id.name if employee.company_id else ''
                        if po.lang_code == 'ja_JP':
                            po.hr_employee_department = (employee.address_id.site)  if employee.address_id.site else ''
                        else:
                            po.hr_employee_department = (employee.address_id.site)  if employee.address_id.site else ''
                            
                        po.hr_employee_printer = employee.name if employee.name else ''
                        
                        if employee.address_id:
                            res_partner = self.env['res.partner'].search([('id','=',employee.address_id.id)])
                            if res_partner:
                                for res in res_partner:
                                    po.hr_employee_zip = ("〒" + res.zip) if res.zip != False else ''
                                    if po.lang_code == 'ja_JP':
                                        po.hr_employee_info = f"{res.state_id.name or ''} {res.city or ''} {res.street or ''} { res.street2 or ''}".strip()
                                    else:
                                        po.hr_employee_info = f"{res.street or ''} { res.street2 or ''} {res.city or ''} {res.state_id.name or ''}".strip()
                                    
                                    po.hr_employee_tel = ("tel." + res.phone) if res.phone != False else ''
                                    po.hr_employee_fax = ("fax." + res.fax) if res.fax != False else ''
                            else:
                                po.hr_employee_zip= ''
                                po.hr_employee_info=''
                                po.hr_employee_tel= ''
                                po.hr_employee_fax= ''
                        else:
                            po.hr_employee_zip= ''
                            po.hr_employee_info= ''
                            po.hr_employee_tel= ''
                            po.hr_employee_fax= ''
                else:
                    po.update(hr_defaults)
            else:
                po.update(hr_defaults)

    purchase_order_address = fields.Char(string="purchase order address" , compute="_compute_purchase_order_address")
    def _compute_purchase_order_address(self):
      for po in self:
        purchase_order = self.env['purchase.order'].with_context({'lang':self.env.user.lang}).search([('id','=',po.id)])
        address = ""
        if purchase_order.picking_type_id.warehouse_id.partner_id.zip:
                address += "〒" + purchase_order.picking_type_id.warehouse_id.partner_id.zip +" "
        if self.env.user.lang == 'ja_JP':
            if purchase_order.picking_type_id.warehouse_id.partner_id.state_id.name:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.state_id.name +" "
            if purchase_order.picking_type_id.warehouse_id.partner_id.city:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.city +" "
            if purchase_order.picking_type_id.warehouse_id.partner_id.street:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.street +" "
            if purchase_order.picking_type_id.warehouse_id.partner_id.street2:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.street2 
        else:
            if purchase_order.picking_type_id.warehouse_id.partner_id.street:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.street +" "
            if purchase_order.picking_type_id.warehouse_id.partner_id.street2:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.street2 
            if purchase_order.picking_type_id.warehouse_id.partner_id.city:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.city +" "
            if purchase_order.picking_type_id.warehouse_id.partner_id.state_id.name:
                address += purchase_order.picking_type_id.warehouse_id.partner_id.state_id.name 
            
        po.purchase_order_address = address