# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    show_details = fields.Boolean(
        string="Show details",
        default=True)
    show_subtotal = fields.Boolean(        string="Show subtotal",
        default=True)
    
    acc_move_line_qty = fields.Char(string="acc_move_line_qty" , compute="_compute_acc_move_line_qty")
                
    def _compute_acc_move_line_qty(self):
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.acc_move_line_qty = ""
                return
            float_product_uom_qty = float(line.quantity)
            integer_part = int(line.quantity)
            decimal_part = round(float_product_uom_qty - integer_part,2)
            decimal_part_after_dot = int(str(decimal_part).split('.')[1])
            if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
                line.acc_move_line_qty = integer_part 
            else:
                while decimal_part_after_dot % 10 == 0:
                    decimal_part_after_dot = decimal_part_after_dot / 10
                line.acc_move_line_qty =  integer_part + float('0.' + str(decimal_part_after_dot))

class AccountMoveCus(models.Model):
    _inherit = 'account.move'

    send_to_company = fields.Char(string="send to company", compute="_compute_send_to")
    send_to_people = fields.Char(string="send to people", compute="_compute_send_to")

    def _compute_send_to(self):
        for line in self:
            partner_name = ''
            company_name = ''
            if line.lang_code == 'en_US' and line.partner_id:
                res_partner = self.env['res.partner'].search([('id', '=', line.partner_id.id)])
                if res_partner:
                    for partner in res_partner:
                        partner_name = ('Mr./Mrs. ' + partner.last_name) if partner.last_name else ''
                        company_name = ('御中 ' + partner.parent_id.name + ' 株式会社') if partner.parent_id else ''
            elif line.lang_code != 'en_US' and line.partner_id:
                res_partner = self.env['res.partner'].search([('id', '=', line.partner_id.id)])
                if res_partner:
                    for partner in res_partner:
                        partner_name = (partner.last_name + ' 様') if partner.last_name else ''
                        company_name = ('株式会社 ' + partner.parent_id.name + ' 御中') if partner.parent_id else ''
            
            if 'send_to_people' in line:
                line.send_to_people = partner_name
            if 'send_to_company' in line:
                line.send_to_company = company_name
                
    hr_employee_company = fields.Char(string="hr employee company" , compute="_compute_hr_employee")
    hr_employee_department = fields.Char(string="hr employee department" , compute="_compute_hr_employee")
    hr_employee_zip = fields.Char(string="hr employee zip" , compute="_compute_hr_employee")
    hr_employee_info = fields.Char(string="hr employee info" , compute="_compute_hr_employee")
    hr_employee_country = fields.Char(string="hr employee country" , compute="_compute_hr_employee")
    hr_employee_tel = fields.Char(string="hr employee tel" , compute="_compute_hr_employee")
    hr_employee_fax = fields.Char(string="hr employee fax" , compute="_compute_hr_employee")
    hr_employee_printer = fields.Char(string="hr employee printer" , compute="_compute_hr_employee")
    
    def _compute_hr_employee(self):
        for ac in self:
            hr_defaults = {
                'hr_employee_company': "株式会社リッツウェル",
                'hr_employee_department': "大阪オフィス",
                'hr_employee_zip': "〒542-0081",
                'hr_employee_info': "大阪市中央区南船場4-7-6 B1F",
                'hr_employee_tel': "tel.06-4963-8777",
                'hr_employee_fax': "fax.06-4963-8778",
                'hr_employee_printer': ac.acc_move_print_staff
            }

            if ac.invoice_user_id:
                hr_employee = self.env['hr.employee'].search([('user_id','=',ac.invoice_user_id.id)])
                if hr_employee:
                    for employee in hr_employee:
                        ac.hr_employee_company = employee.company_id.name if employee.company_id else ''
                        if ac.lang_code == 'ja_JP':
                            ac.hr_employee_department = (employee.address_id.site +' オフィス')  if employee.address_id.site else ''
                        else:
                            ac.hr_employee_department = (employee.address_id.site +' Office')  if employee.address_id.site else ''

                        if employee.name:
                            if ac.lang_code == 'en_US':
                                ac.hr_employee_printer = employee.name +" Seal" 
                            else:
                                ac.hr_employee_printer = employee.name +" 印" 
                        else:
                            ac.hr_employee_printer = ''
                            
                        if employee.address_id:
                            res_partner = self.env['res.partner'].search([('id','=',employee.address_id.id)])
                            if res_partner:
                                for res in res_partner:
                                    ac.hr_employee_zip = ("〒" + res.zip) if res.zip != False else ''
                                    if ac.lang_code == 'ja_JP':
                                        ac.hr_employee_info = f"{res.state_id.name or ''} {res.city or ''} {res.street or ''} { res.street2 or ''}".strip()
                                    else:
                                        ac.hr_employee_info = f"{res.street or ''} { res.street2 or ''} {res.city or ''} {res.state_id.name or ''}".strip()
                                    
                                    ac.hr_employee_tel = ("tel." + res.phone) if res.phone != False else ''
                                    ac.hr_employee_fax = ("fax." + res.fax) if res.fax != False else ''
                            else:
                                ac.hr_employee_zip= ''
                                ac.hr_employee_info=''
                                ac.hr_employee_tel= ''
                                ac.hr_employee_fax= ''
                        else:
                            ac.hr_employee_zip= ''
                            ac.hr_employee_info= ''
                            ac.hr_employee_tel= ''
                            ac.hr_employee_fax= ''
                else:
                    ac.update(hr_defaults)
            else:
                ac.update(hr_defaults)
        
    account_move_hr_employee = fields.Char(string="account move hr employee" , compute="_compute_account_move_hr_employee")
    def _compute_account_move_hr_employee(self):
      for record in self:
        hr_employee_detail = ""
        if record.hr_employee_company:
            hr_employee_detail += record.hr_employee_company + "\n"
        if record.hr_employee_department:
            hr_employee_detail += record.hr_employee_department + "\n"
        if record.hr_employee_zip:
            hr_employee_detail += record.hr_employee_zip + "\n"
        if record.hr_employee_info:
            hr_employee_detail += record.hr_employee_info + "\n"
        if record.hr_employee_tel:
            hr_employee_detail += record.hr_employee_tel + "\n"
        if record.hr_employee_fax:
            hr_employee_detail += record.hr_employee_fax + "\n"
        if record.hr_employee_printer:
            hr_employee_detail += record.hr_employee_printer 
        
        record.account_move_hr_employee= hr_employee_detail
