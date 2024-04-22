# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import math

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    so_title = fields.Char(string="title")
    calculate_planned_date = fields.Date(string="planned date" , compute="_compute_calculate_planned_date")
    so_work_days = fields.Char(string="planned date" , compute="_compute_so_work_days")
    hr_employee_company = fields.Char(string="hr employee company" , compute="_compute_hr_employee")
    hr_employee_department = fields.Char(string="hr employee department" , compute="_compute_hr_employee")
    hr_employee_zip = fields.Char(string="hr employee zip" , compute="_compute_hr_employee")
    hr_employee_info = fields.Char(string="hr employee info" , compute="_compute_hr_employee")
    hr_employee_country = fields.Char(string="hr employee country" , compute="_compute_hr_employee")
    hr_employee_tel = fields.Char(string="hr employee tel" , compute="_compute_hr_employee")
    hr_employee_fax = fields.Char(string="hr employee fax" , compute="_compute_hr_employee")
    hr_employee_printer = fields.Char(string="hr employee printer" , compute="_compute_hr_employee")
    send_to_company = fields.Char(string="send to company" , compute="_compute_send_to")
    send_to_people = fields.Char(string="send to people" , compute="_compute_send_to")
    dear_to = fields.Char(string="send to people" , compute="_compute_send_to")
    sale_order_discount = fields.Char(string="sale order discount" , compute="_compute_sale_order_discount")
    registration_number = fields.Char(string="registration number" , compute="_compute_registration_number")

    def _compute_send_to(self):
        for so in self:
            partner_name = ''
            company_name = ''
            if so.partner_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id','=',so.partner_id.id)])
                if res_partner:
                    for line in res_partner:
                        if so.lang_code == 'en_US':
                            if line.company_type == 'company':
                                company_name =  "Dear " + line.name if line.name else ''
                            else:
                                if line.parent_id :
                                    if line.dummy:
                                        partner_name =  'Mr./Mrs. ' + line.last_name if line.last_name else ''
                                    else:
                                        if line.parent_id.name:
                                            company_name =  "Dear " + line.parent_id.name + ' Co., Ltd.'
                                        partner_name =  'Mr./Mrs. ' +  line.last_name if line.last_name else ''
                                else:
                                    partner_name =  'Mr./Mrs. ' + line.last_name if line.last_name else ''
                        else:   
                            if line.company_type == 'company':
                                if line.name:
                                    company_name =  line.name+ ' 御中'
                            else:
                                if line.parent_id :
                                    if line.dummy:
                                        if line.last_name:
                                            partner_name =  line.last_name+ ' 様'
                                    else:
                                        if line.parent_id.name:
                                            company_name =  line.parent_id.name
                                        if line.last_name:
                                            partner_name =  line.last_name+ ' 様'
                                else:
                                    if line.last_name:
                                            partner_name =  line.last_name+ ' 様'
            send = ""   
            if company_name:
                send += company_name
                if partner_name:
                    send += '\n' + partner_name  
            else:
                if partner_name :
                    send += partner_name
            so.send_to_company = company_name
            so.send_to_people = partner_name
            so.dear_to = send
                        
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
                                        so.hr_employee_info = f"{res.state_id.name or ''} {res.city or ''} {res.street or ''} {res.street2 or ''}"
                                    else:
                                        so.hr_employee_info = f"{res.street or ''} {res.street2 or ''} {res.city or ''} {res.state_id.name or ''}"
                                    
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
        if self.env.context['lang'] == 'ja_JP':
            self.registration_number = '登録番号:T4290001017449'
        else:
            self.registration_number = 'Registration number: T4290001017449'
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)
    calculate_packages = fields.Integer(   
        string="Calculate packages",
        compute="_compute_calculate_packages"
    )
    
    sale_order_line_product_uom_qty = fields.Char(string="sale order product uom qty" , compute="_compute_sale_order_product_uom_qty")
    
    def _compute_calculate_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.calculate_packages = math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
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
                