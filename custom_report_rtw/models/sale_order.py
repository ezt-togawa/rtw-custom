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
                        hr_employee = self.env['hr.employee'].search([('user_id','=',crm.user_id.id)])
                        if hr_employee:
                            for employee in hr_employee:
                                so.hr_employee_company = employee.company_id.name if employee.company_id else ''
                                so.hr_employee_department = employee.department_id.name if employee.department_id else ''
                                if employee.name:
                                    if so.lang_code == 'en_US':
                                        so.hr_employee_printer = employee.name +" Seal" 
                                    else:
                                        so.hr_employee_printer = employee.name +" 印" 
                                else:
                                    so.hr_employee_printer = ''
                                    
                                if employee.address_id:
                                    res_partner = self.env['res.partner'].search([('id','=',employee.address_id.id)])
                                    if res_partner:
                                        for res in res_partner:
                                            so.hr_employee_zip = ("〒" + res.zip) if res.zip != False else ''
                                            so.hr_employee_info = f"{res.street or res.street2 or ''} {res.city or ''} {res.state_id.name or ''} \n {res.country_id.name or ''}".strip()
                                            so.hr_employee_tel = ("tel." + res.phone) if res.phone != False else ''
                                            so.hr_employee_fax = ("fax." + res.fax) if res.fax != False else ''
                                    else:
                                        so.hr_employee_zip= ''
                                        so.hr_employee_info=''
                                        so.hr_employee_tel= ''
                                        so.hr_employee_fax= ''
                                else:
                                    so.hr_employee_zip= ''
                                    so.hr_employee_info= ''
                                    so.hr_employee_tel= ''
                                    so.hr_employee_fax= ''
                        else:
                            so.update(hr_defaults)
                    else:
                        so.update(hr_defaults)
            else:
                so.update(hr_defaults)
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # show_details = fields.Boolean(
    #     string="Show details",
    #     default=True)
    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)
    calculate_packages = fields.Integer(
        string="Calculate packages",
        compute="_compute_calculate_packages"
    )

    def _compute_calculate_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.calculate_packages = math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
            else:
                line.calculate_packages = line.product_uom_qty

    # def _prepare_invoice_line(self, qty):
    #     res = super()._prepare_invoice_line(qty)
    #     res.update(show_details=self.show_details,
    #                show_subtotal=self.show_subtotal)
    #     return res
