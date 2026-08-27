# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
from datetime import datetime
from markupsafe import Markup, escape

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
    registration_number = fields.Char(string="registration number", compute="_compute_registration_number")
    current_print = fields.Char(compute="_compute_current_print")
    payment_details_invoice = fields.Char(string="payment details invoice" , compute="_compute_payment_details")
    sale_order_hr_employee_invoice = fields.Char(
        compute="_compute_sale_order_hr_employee",
        string="Sale order hr employee invoice",
    )

    dear_to_invoice = fields.Char(string="send to people" , compute="_compute_send_to_invoice")
    send_to_people_invoice = fields.Char(string="send to people", compute="_compute_send_to_invoice")
    send_to_company_invoice = fields.Char(string="send to company", compute="_compute_send_to_invoice")
    
    def _compute_send_to_invoice(self):
        for so in self:
            partner_name = ''
            company_name = ''
            if so.partner_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id', '=', so.partner_id.id)])
                if res_partner:
                    for line in res_partner:
                        if so.lang_code == 'en_US':
                            if line.company_type == 'company':
                                company_name = "Dear " + line.name if line.name else ''
                            elif line.parent_id:
                                if line.dummy and line.last_name:
                                    partner_name = 'Mr./Mrs. ' + line.last_name
                                else:
                                    company_name = "Dear " + line.parent_id.name + ' Co., Ltd.' if line.parent_id.name else ''
                                    partner_name = 'Mr./Mrs. ' + line.last_name if line.last_name else ''
                            else:
                                partner_name = 'Mr./Mrs. ' + line.last_name if line.last_name else ''
                        else:   
                            if line.company_type == 'company':
                                company_name = line.name + _(' 御中') if line.name else ''
                            elif line.parent_id:
                                if line.dummy and line.last_name:
                                    partner_name = line.last_name + _(' 様')
                                else:
                                    company_name = line.parent_id.name if line.parent_id.name else ''
                                    partner_name = line.last_name + _(' 様') if line.last_name else ''
                            else:
                                partner_name = line.last_name + _(' 様') if line.last_name else ''
            send = ""   
            if company_name and partner_name:
                send += company_name + '\n' + partner_name
            elif company_name:
                send += company_name
            elif partner_name:
                send += partner_name
            so.send_to_company_invoice = company_name
            so.send_to_people_invoice = partner_name
            so.dear_to_invoice = send

    def _compute_payment_details(self):
        for invoice in self:
            if invoice.partner_id.transactions.name and invoice.partner_id.payment_terms_1:
                invoice.payment_details_invoice = invoice.partner_id.transactions.name + ' / ' + invoice.partner_id.payment_terms_1
            elif invoice.partner_id.transactions.name:
                invoice.payment_details_invoice = invoice.partner_id.transactions.name
            elif invoice.partner_id.payment_terms_1:
                invoice.payment_details_invoice = invoice.partner_id.payment_terms_1
            else:
                invoice.payment_details_invoice = None
    
    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            
    def _compute_send_to(self):
        for so in self:
            partner_name = ''
            company_name = ''
            if so.partner_id:
                res_partner= self.env['res.partner'].search([('id','=',so.partner_id.id)])
                if res_partner:
                    for line in res_partner:
                        if so.lang_code == 'en_US':
                            if line.company_type == 'company':
                                company_name = "Dear " + line.name if line.name else ''
                            else:
                                if line.parent_id:
                                    if line.dummy:
                                        partner_name = 'Mr./Mrs. ' + line.last_name if line.last_name else ''
                                    else:
                                        if line.parent_id.name:
                                            company_name = "Dear " + line.parent_id.name + ' Co., Ltd.'
                                        partner_name = 'Mr./Mrs. ' + line.last_name if line.last_name else ''
                                else:
                                    partner_name = 'Mr./Mrs. ' + line.last_name if line.last_name else ''
                        else:   
                            if line.company_type == 'company':
                                if line.name:
                                    company_name = line.name + _(' 御中')
                            else:
                                if line.parent_id:
                                    if line.dummy:
                                        if line.last_name:
                                            partner_name = line.last_name + _(' 様')
                                    else:
                                        if line.parent_id.name:
                                            company_name = line.parent_id.name
                                        if line.last_name:
                                            partner_name = line.last_name + _(' 様')
                                else:
                                    if line.last_name:
                                            partner_name = line.last_name + _(' 様')

        so.send_to_company = company_name
        so.send_to_people = partner_name
                
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
                'hr_employee_company': _("株式会社リッツウェル"),
                'hr_employee_department': _("大阪オフィス"),
                'hr_employee_zip': _("〒542-0081"),
                'hr_employee_info': _("大阪市中央区南船場4-7-6 B1F"),
                'hr_employee_tel': _("tel.06-4963-8777"),
                'hr_employee_fax': _("fax.06-4963-8778"),
                'hr_employee_printer': ac.acc_move_print_staff
            }

            if ac.invoice_user_id:
                hr_employee = self.env['hr.employee'].with_context({'lang':self.lang_code}).search([('user_id','=',ac.invoice_user_id.id)])
                if hr_employee:
                    for employee in hr_employee:
                        ac.hr_employee_company = employee.company_id.name if employee.company_id else ''
                        if ac.lang_code == 'ja_JP':
                            ac.hr_employee_department = (employee.address_id.site)  if employee.address_id.site else ''
                        else:
                            ac.hr_employee_department = (employee.address_id.site)  if employee.address_id.site else ''

                        if employee.name:
                            if ac.lang_code == 'en_US':
                                ac.hr_employee_printer = employee.name
                            else:
                                ac.hr_employee_printer = employee.name
                        else:
                            ac.hr_employee_printer = ''
                            
                        if employee.address_id:
                            res_partner = self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id','=',employee.address_id.id)])
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
        
    def _compute_registration_number(self):
        if self.env.user.lang == 'en_US':
            self.registration_number = 'Registration number: T4290001017449'
        else:
            self.registration_number = _('登録番号:T4290001017449')

    def _compute_sale_order_hr_employee(self):
        for record in self:
            record.sale_order_hr_employee_invoice = _(
                "Ritzwell & Co.\n"
                "登録番号:T4290001017449\n"
                "本社\n"
                "〒812-0888\n"
                "福岡県 福岡市博多区\n"
                "板付5-2-9\n"
                "tel.092-584-2240\n"
                "fax.092-584-2241"
            )

    def _zenkaku_width(self, text):
        if not text:
            return 0.0
        width = 0.0
        for ch in text:
            code = ord(ch)
            if (0x1100 <= code <= 0x115F) or (0x2E80 <= code <= 0xA4CF) or \
               (0xAC00 <= code <= 0xD7A3) or (0xF900 <= code <= 0xFAFF) or \
               (0xFF00 <= code <= 0xFF60) or (0xFFE0 <= code <= 0xFFE6):
                width += 1.0
            else:
                width += 0.5
        return width

    def render_fit_text(self, text, target_width_px, font_size=22, underline=False, fixed_width=False):
        text = text or ''
        if not text:
            return Markup('')
        escaped = escape(text)
        estimated_px = self._zenkaku_width(text) * font_size
        if estimated_px <= target_width_px:
            if fixed_width:
                style = ('display:inline-block; width:%dpx; white-space:nowrap;') % target_width_px
                if underline:
                    style += ' border-bottom:1px solid black;'
                return Markup('<span style="%s">%s</span>') % (style, escaped)
            if underline:
                return Markup('<span class="border-bottom2" style="white-space:nowrap;">%s</span>') % escaped
            return Markup('<span style="white-space:nowrap;">%s</span>') % escaped
        svg_height = int(font_size * 1.3)
        baseline_y = int(font_size * 0.95)
        line_svg = Markup('')
        if underline:
            line_y = svg_height - 2
            line_svg = Markup('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="1"/>') % (line_y, target_width_px, line_y)
        return Markup(
            '<svg width="%(width)dpx" height="%(height)dpx" '
            'style="display:inline-block; vertical-align:bottom;">'
            '<text x="0" y="%(baseline)d" font-size="%(font_size)dpx" '
            'textLength="%(width)d" lengthAdjust="spacingAndGlyphs">%(text)s</text>'
            '%(line)s</svg>'
        ) % {'width': target_width_px, 'height': svg_height, 'baseline': baseline_y,
             'font_size': font_size, 'text': escaped, 'line': line_svg}
