# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import math
from datetime import datetime
import base64
from PIL import Image as PILImage
from io import BytesIO
import io
import json
from PIL import Image
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    so_title = fields.Char(string="title")
    calculate_planned_date = fields.Date(string="planned date" , compute="_compute_calculate_planned_date")
    so_work_days = fields.Char(string="planned date" , compute="_compute_so_work_days")
    hr_employee_company = fields.Char(string="hr employee company" , compute="_compute_hr_employee")
    hr_employee_department = fields.Char(string="hr employee department" , compute="_compute_hr_employee")
    hr_employee_zip = fields.Char(string="hr employee zip" , compute="_compute_hr_employee")
    hr_employee_info = fields.Char(string="hr employee info" , compute="_compute_hr_employee")
    hr_employee_address1 = fields.Char(string="hr employee address1" , compute="_compute_hr_employee")
    hr_employee_address2= fields.Char(string="hr employee address2" , compute="_compute_hr_employee")
    hr_employee_country = fields.Char(string="hr employee country" , compute="_compute_hr_employee")
    hr_employee_tel = fields.Char(string="hr employee tel" , compute="_compute_hr_employee")
    hr_employee_fax = fields.Char(string="hr employee fax" , compute="_compute_hr_employee")
    hr_employee_printer = fields.Char(string="hr employee printer" , compute="_compute_hr_employee")
    send_to_company_invoice_sale = fields.Char(string="send to company invoice sale" , compute="_send_to_company_invoice_sale")
    send_to_people_invoice_sale = fields.Char(string="send to company invoice sale" , compute="_send_to_company_invoice_sale")
    dear_to_invoice_sale = fields.Char(string="send to company invoice sale" , compute="_send_to_company_invoice_sale")
    send_to_company = fields.Char(string="send to company" , compute="_compute_send_to")
    send_to_people = fields.Char(string="send to people" , compute="_compute_send_to")
    dear_to = fields.Char(string="send to people" , compute="_compute_send_to")
    sale_order_discount = fields.Char(string="sale order discount" , compute="_compute_sale_order_discount")
    registration_number = fields.Char(string="registration number" , compute="_compute_registration_number")
    current_print = fields.Char(compute="_compute_current_print")
    payment_details = fields.Char(string="payment details" , compute="_compute_payment_details")

    def _compute_payment_details(self):
        for so in self:
            if so.transactions and so.transaction_condition_1:
                so.payment_details = so.transactions.name + ' / ' + so.transaction_condition_1
            elif so.transactions:
                so.payment_details = so.transactions.name
            elif so.transaction_condition_1:
                so.payment_details = so.transaction_condition_1
            else:
                so.payment_details = None

    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            
    def _compute_send_to(self):
        for so in self:
            partner_name = ''
            company_name = ''
            if so.partner_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id', '=', so.partner_id.id)])
                if res_partner:
                    for line in res_partner:
                        if so.lang_code == 'en_US':
                            if line.company_type == 'company':
                                company_name =  "Dear " + line.name if line.name else ''
                            elif line.parent_id :
                                if line.dummy and line.last_name:
                                    partner_name =  'Mr./Mrs. ' + line.last_name
                                else:
                                    company_name =  "Dear " + line.parent_id.name + ' Co., Ltd.' if line.parent_id.name else ''
                                    partner_name =  'Mr./Mrs. ' +  line.last_name if line.last_name else ''
                            else:
                                partner_name =  'Mr./Mrs. ' + line.last_name if line.last_name else ''
                        else:   
                            if line.company_type == 'company':
                                company_name =  line.name + ' 御中' if line.name else '' 
                            elif line.parent_id :
                                if line.dummy and line.last_name:
                                    partner_name =  line.last_name+ ' 様'
                                else:
                                    company_name =  line.parent_id.name if line.parent_id.name else ''
                                    partner_name =  line.last_name + ' 様' if line.last_name else ''
                            else:
                                partner_name =  line.last_name + ' 様' if line.last_name else ''
            send = ""   
            if company_name and partner_name:
                send += company_name + '\n' + partner_name  
            elif company_name :
                send += company_name
            elif partner_name :
                send += partner_name
                
            so.send_to_company = company_name
            so.send_to_people = partner_name
            so.dear_to = send

    def _send_to_company_invoice_sale(self):
        for so in self:
            partner_name = ''
            company_name = ''
            if so.partner_invoice_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id', '=', so.partner_invoice_id.id)])
                if res_partner:
                    for line in res_partner:
                        if so.lang_code == 'en_US':
                            if line.company_type == 'company':
                                company_name =  "Dear " + line.name if line.name else ''
                            elif line.parent_id :
                                if line.dummy and line.last_name:
                                    partner_name =  'Mr./Mrs. ' + line.last_name
                                else:
                                    company_name =  "Dear " + line.parent_id.name + ' Co., Ltd.' if line.parent_id.name else ''
                                    partner_name =  'Mr./Mrs. ' +  line.last_name if line.last_name else ''
                            else:
                                partner_name =  'Mr./Mrs. ' + line.last_name if line.last_name else ''
                        else:   
                            if line.company_type == 'company':
                                company_name =  line.name + ' 御中' if line.name else '' 
                            elif line.parent_id :
                                if line.dummy and line.last_name:
                                    partner_name =  line.last_name+ ' 様'
                                else:
                                    company_name =  line.parent_id.name if line.parent_id.name else ''
                                    partner_name =  line.last_name + ' 様' if line.last_name else ''
                            else:
                                partner_name =  line.last_name + ' 様' if line.last_name else ''
            send = ""   
            if company_name and partner_name:
                send += company_name + '\n' + partner_name  
            elif company_name :
                send += company_name
            elif partner_name :
                send += partner_name
                
            so.send_to_company_invoice_sale = company_name
            so.send_to_people_invoice_sale = partner_name
            so.dear_to_invoice_sale = send

    def _compute_calculate_planned_date(self):
        max_planned_date = ''
        for line in self.order_line:
            if max_planned_date == '':
                max_planned_date = line.date_planned
            elif line.date_planned and line.date_planned > max_planned_date:
                max_planned_date = line.date_planned
        self.calculate_planned_date = max_planned_date
        
    def _compute_so_work_days(self):
        for line in self:
            if line.lang_code == "en_US":
                workdays_map = {
                    "発注後約 4週以内": "About 4 weeks or less after ordering",
                    "発注後約 5-6週間": "About 5-6 weeks after ordering",
                    "発注後約 6-7週間": "About 6-7 weeks after ordering",
                    "発注後約 7-8週間": "About 7-8 weeks after ordering",
                    "発注後約 8-10週間": "About 8-10 weeks after ordering",
                    "発注後約 10-12週間": "About 10-12 weeks after ordering",
                    "発注後約 12以上": "About 12 weeks or more after ordering"
                }
                line.so_work_days = workdays_map.get(line.workdays, False)    
            else:
                line.so_work_days = line.workdays
        
    def _compute_hr_employee(self):
        for so in self:
            hr_defaults = {
                'hr_employee_company': "株式会社リッツウェル",
                'hr_employee_department': "大阪オフィス",
                'hr_employee_zip': "〒542-0081",
                'hr_employee_info': "大阪市中央区南船場4-7-6 B1F",
                'hr_employee_address1': "大阪市中央区",
                'hr_employee_address2': "南船場4-7-6 B1F",
                'hr_employee_tel': "tel.06-4963-8777",
                'hr_employee_fax': "fax.06-4963-8778",
                'hr_employee_printer': so.sale_order_printing_staff
            }

            if so.opportunity_id:
                crm_lead = self.env['crm.lead'].search([('id','=',so.opportunity_id.id)])
                for crm in crm_lead:
                    if crm.user_id:
                        hr_employee = self.env['hr.employee'].with_context({'lang':self.lang_code}).search([('user_id','=',crm.user_id.id)])
                        if hr_employee:
                            for employee in hr_employee:
                                if employee.address_id :
                                    res = employee.address_id
                                    if res.company_type == 'company':
                                        so.hr_employee_company =  res.name if res.name else ''
                                    else:
                                        if res.parent_id :
                                            so.hr_employee_company   =  res.parent_id.name if res.parent_id.name else ''
                                        else:
                                            so.hr_employee_company =  ''
                                            
                                    if res.site:
                                        if so.lang_code == 'ja_JP':
                                            so.hr_employee_department = (res.site)
                                        else:
                                            so.hr_employee_department = (res.site)
                                    else:
                                        so.hr_employee_department = ''
                                    
                                    so.hr_employee_zip = ("〒" + res.zip) if res.zip else ''
                                    
                                    if so.lang_code == 'ja_JP':
                                        so.hr_employee_info = f"{res.state_id.name or ''}  {res.city or ''} {res.street or ''} {res.street2 or ''}"
                                        so.hr_employee_address1 = f"{res.state_id.name or ''}  {res.city or ''}"
                                        so.hr_employee_address2 = f"{res.street or ''} {res.street2 or ''}"
                                    else:
                                        so.hr_employee_info = f"{res.street or ''} {res.street2 or ''} {res.city or ''} {res.state_id.name or ''}"
                                        so.hr_employee_address1 = f"{res.street or ''} {res.street2 or ''}"
                                        so.hr_employee_address2 = f"{res.city or ''}  {res.state_id.name or ''}  "
                                        
                                    so.hr_employee_tel = ("tel." + res.phone) if res.phone != False else ''
                                    so.hr_employee_fax = ("fax." + res.fax) if res.fax != False else ''
                                    
                                    so.hr_employee_printer = employee.name  if employee.name  else ''
                                else:
                                    so.update(hr_defaults)
                        else:
                            so.update(hr_defaults)
                    else:
                        so.update(hr_defaults)
            else:
                so.update(hr_defaults)

    def _compute_registration_number(self):
        if self.env.user.lang == 'en_US':
            self.registration_number = 'Registration number: T4290001017449'
        else:
            self.registration_number = '登録番号:T4290001017449'
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)
    calculate_packages = fields.Integer(   
        string="Calculate packages",
        compute="_compute_calculate_packages"
    )

    product_img_pdf = fields.Binary(compute="_compute_image_pdf")
    attach_img_pdf = fields.Binary(compute="_compute_image_pdf")

    child_attr_imgs_pdf = fields.Text(compute='_compute_child_attr_imgs_pdf')
    child_attr_names = fields.Text(compute='_compute_child_attr_imgs_pdf')

        
    sale_order_line_product_uom_qty = fields.Char(string="sale order product uom qty" , compute="_compute_sale_order_product_uom_qty")
    
    def _compute_calculate_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.calculate_packages = math.ceil(line.product_uom_qty * line.product_id.two_legs_scale)
            else:
                line.calculate_packages = line.product_uom_qty
                
    def _compute_sale_order_product_uom_qty(self):
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section' :
                line.sale_order_line_product_uom_qty = ""
                return
            float_product_uom_qty = float(line.product_uom_qty)
            integer_part = int(line.product_uom_qty)
            decimal_part = round(float_product_uom_qty - integer_part,2)  
            decimal_part_after_dot = int(str(decimal_part).split('.')[1])
            if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
                line.sale_order_line_product_uom_qty = integer_part 
            else:
                while decimal_part_after_dot % 10 == 0:
                    decimal_part_after_dot = decimal_part_after_dot / 10
                line.sale_order_line_product_uom_qty =  integer_part + float('0.' + str(decimal_part_after_dot))


    def resize_image_for_pdf(self, image_base64, frame_w, frame_h, margin=5):
        if not image_base64:
            return False
        if isinstance(image_base64, bytes):
            image_base64 = image_base64.decode('utf-8')
        img_bytes = base64.b64decode(image_base64)
        img = PILImage.open(io.BytesIO(img_bytes)).convert('RGB')
        w, h = img.size
        if w == 0 or h == 0:
            return False

        inner_frame_w = frame_w - (margin * 2)
        inner_frame_h = frame_h - (margin * 2)

        ratio = min(inner_frame_w / w, inner_frame_h / h)
        new_w = max(1, int(w * ratio))
        new_h = max(1, int(h * ratio))
        img = img.resize((new_w, new_h), PILImage.LANCZOS)

        background = PILImage.new('RGB', (frame_w, frame_h), (255, 255, 255))
        paste_x = (frame_w - new_w) // 2
        paste_y = (frame_h - new_h) // 2
        background.paste(img, (paste_x, paste_y))

        output = io.BytesIO()
        background.save(output, format='PNG')
        return base64.b64encode(output.getvalue()).decode('utf-8')


    def _compute_image_pdf(self):
            frame_w, frame_h = 250, 120
            for line in self:
                line.product_img_pdf = self.resize_image_for_pdf(line.product_id.image_256, frame_w, frame_h)
                attach_file = line.item_sale_attach_ids[0].attach_file if line.item_sale_attach_ids else False
                line.attach_img_pdf = self.resize_image_for_pdf(attach_file, frame_w, frame_h)
                

    def resize_image_to_square(self, image_base64, size):
        if not image_base64:
            return False
        if isinstance(image_base64, bytes):
            image_base64 = image_base64.decode('utf-8')

        img_bytes = base64.b64decode(image_base64)
        img = PILImage.open(io.BytesIO(img_bytes)).convert('RGB')
        w, h = img.size
        if w == 0 or h == 0:
            return False
        min_dimension = min(w, h)
        left = (w - min_dimension) // 2
        top = (h - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        img = img.crop((left, top, right, bottom))
        img = img.resize((size, size), PILImage.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='PNG')
        return base64.b64encode(output.getvalue()).decode('utf-8')



    def _compute_child_attr_imgs_pdf(self):
        square_size = 80
        for line in self:
            imgs = []
            names = []
            attrs = line.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id')
            attr_child_ids = set()
            count = 0
            for parent_attr in attrs:
                if count >= 4:
                    break
                if (parent_attr.id not in attr_child_ids and parent_attr.image and
                    all(attr not in attrs for attr in parent_attr.child_attribute_ids.mapped('child_attribute_id'))):
                    imgs.append(self.resize_image_to_square(parent_attr.image, square_size))
                    names.append(f"{parent_attr.attribute_id.name}: {parent_attr.name}")
                    count += 1
                else:
                    for child_attr in parent_attr.child_attribute_ids:
                        if count >= 4:
                            break
                        if (child_attr.image and child_attr.child_attribute_id.id in attrs.ids and
                            child_attr.child_attribute_id.id not in attr_child_ids):
                            imgs.append(self.resize_image_to_square(child_attr.image, square_size))
                            names.append(f"{child_attr.child_attribute_id.attribute_id.name}: {child_attr.child_attribute_id.name}")
                            attr_child_ids.add(child_attr.child_attribute_id.id)
                            count += 1
            while count < 4:
                imgs.append(False)
                names.append("")
                count += 1
            line.child_attr_imgs_pdf = json.dumps(imgs)
            line.child_attr_names = json.dumps(names)
        