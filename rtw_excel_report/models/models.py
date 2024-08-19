from odoo import models, fields, _
from datetime import datetime
import math
import babel.dates

class SaleOrderExcelReport(models.Model):
    _inherit = "sale.order"

    sale_order_amount_total = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount total",
    )
    sale_order_amount_untaxed = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount untax",
    )
    sale_order_amount_tax = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount tax",
    )
    sale_order_fax = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Fax",
    )
    sale_order_tel = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Tel",
    )
    sale_order_zip = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Zip",
    )
    sale_order_current_date = fields.Char(
        compute="_compute_sale_order_current_date",
        string="Current Date",
    )
    sale_order_estimated_shipping_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Estimated Shipping Date",
    )
    sale_order_date_order = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Date Order",
    )
    sale_order_validity_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Validity Date",
    )
    sale_order_special_note = fields.Char(
        compute="_compute_sale_order_special_note",
        string="Special note",
    )
    sale_order_special_note_list_price = fields.Char(
        compute="_compute_sale_order_special_note",
        string="Special note",
    )
    sale_order_company_owner = fields.Char(
        compute="_compute_sale_order_company_owner",
        string="Company Name",
    )
    sale_order_total_list_price = fields.Char(
        compute="_compute_sale_order_list_price",
        string="Total List Price",
    )
    sale_order_amount_untaxed2 = fields.Char(
        compute="_compute_sale_order_amount_untaxed2",
        string="Amount untaxed",
    )
    sale_order_total_discount = fields.Char(
        compute="_compute_sale_order_total_discount",
        string="Total Discount",
    )
    sale_order_account_number = fields.Char(
        compute="_compute_sale_order_account_number",
        string="Account Number",
    )
    sale_order_preferred_delivery_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Preferred Delivery Date",
    )
    sale_order_warehouse_arrive_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Warehouse Arrive Date",
    )
    sale_order_date_deadline = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Date deadline",
    )
    sale_order_send_to_company = fields.Char(
        compute="_compute_sale_order_send_to_company",
        string="Send to company",
    )
    sale_order_send_to_company2 = fields.Char(
        compute="_compute_sale_order_send_to_company2",
        string="Send to company2",
    )

    sale_order_detail_address_partner = fields.Char(
        compute="_compute_sale_order_detail_address_partner",
        string="Detail Address Partner",
    )

    sale_order_tel_phone_partner = fields.Char(
        compute="_compute_sale_order_tel_phone_partner",
        string="Tel And Phone Partner",
    )

    sale_order_printing_staff = fields.Char(
        compute="_compute_sale_order_printing_staff",
        string="Printing Staff",
    )

    sale_order_name_and_phone_staff = fields.Char(
        compute="_compute_sale_order_name_and_phone_staff",
        string="Name And Phone Staff",
    )

    sale_order_detail_customer_info = fields.Char(
        compute="_compute_sale_order_detail_customer_info",
        string="Detail Customer Info",
    )

    sale_order_date_planned = fields.Char(
        compute="_compute_sale_order_date_planned",
        string="Order Date Planned",
    )

    sale_order_shiratani_entry_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Shiratani Entry Date",
    )

    sale_order_ritzwell_staff = fields.Char(
        compute="_compute_sale_order_ritzwell_staff",
        string="Ritzwell staff",
    )

    sale_order_title = fields.Char(
        compute="_compute_sale_order_title",
        string="Title",
    )

    sale_order_company_name = fields.Char(
        compute="_compute_sale_order_company_name",
        string="Company name",
    )
    sale_order_name = fields.Char(
        compute="_compute_sale_order_name",
        string="Sale order name",
    )

    sale_order_info_cus = fields.Char(
        compute="_compute_sale_order_info_cus",
        string="Sale order name",
    )
    
    sale_order_hr_employee_split_street = fields.Char(
        compute="_compute_sale_order_hr_employee",
        string="Sale order hr employee split street",
    )
    
    sale_order_hr_employee = fields.Char(
        compute="_compute_sale_order_hr_employee",
        string="Sale order hr employee",
    )
    
    sale_order_hr_employee_invoice = fields.Char(
        compute="_compute_sale_order_hr_employee",
        string="Sale order hr employee invoice",
    )
    
    sale_order_preferred_delivery_period= fields.Char(
        compute="_compute_sale_order_preferred_delivery_period",
        string="Sale order preferred delivery period",
    )
    

    list_order_line = fields.One2many(
        'sale.order.line',
        compute = '_compute_list_order_line',
        string = 'List order line'
    )

    check_oversea = fields.Char(
        "checkout oversea",
        compute="_compute_check_oversea",
    )

    lang_code = fields.Char(string="Language Code", compute="_compute_lang_code")
    yearUnit = fields.Char(string="Year", compute="_compute_year_unit")
    monthUnit = fields.Char(string="Month", compute="_compute_month_unit")
    dayUnit = fields.Char(string="Day", compute="_compute_day_unit")
    
    sale_order_transactions_term = fields.Char(string="sale order transactions term", compute="_compute_sale_order_transactions_term")
    
    sale_order_print_staff = fields.Char(
        "print staff",
        compute="_compute_print_staff",
    )        
    sale_order_bank_name = fields.Char(
        "bank name",
        compute="_compute_bank",
    )        
    sale_order_bank_branch = fields.Char(
        "bank_branch",
        compute="_compute_bank",
    )        
    sale_order_number_account = fields.Char(
        "number account",
        compute="_compute_bank",
    )    
    sale_order_draff_invoice = fields.Char(
        "draff invoice",
        compute="_compute_sale_order_draff_invoice",
    )    
    sale_order_waypoint_name = fields.Char(
        "waypoint name",
        compute="_compute_sale_order_waypoint",
    )    
    sale_order_waypoint_address = fields.Char(
        "waypoint address",
        compute="_compute_sale_order_waypoint",
    )  
    sale_order_partner_info = fields.Char(
        "partner information",
        compute="_compute_sale_partner_info",
    )  
    sale_order_partner_address = fields.Char(
        "partner address",
        compute="_compute_sale_order_partner_address",
    )  
    sale_order_sipping_to = fields.Char(
        "sipping to",
        compute="_compute_sale_order_sipping_to",
    )  
    
    send_to_company_delivery = fields.Char(compute="_compute_send_to_company_delivery")  
    send_to_people_delivery = fields.Char(compute="_compute_send_to_company_delivery")  
    send_to_tel_fax = fields.Char(compute="_compute_send_to_company_delivery")  
    dear_to_delivery = fields.Char(compute="_compute_send_to_company_delivery")
    sale_witness_name_phone = fields.Char(compute="_compute_sale_witness_name_phone")
    
    def _compute_sale_witness_name_phone(self):
        for record in self:
            witness_name_phone = ""
            if record.witness:
                witness_name_phone += record.witness + " " 
            if record.witness_phone:
                witness_name_phone += record.witness_phone
            record.sale_witness_name_phone = witness_name_phone.rstrip()
            
    def _compute_send_to_company_delivery(self):
        for so in self:
            partner_name = ''
            company_name = ''
            tel = ''
            fax = ''
            send = ''
            
            if so.sipping_to == 'direct':
                send = so.shipping_to_text if so.shipping_to_text else ''
            elif so.waypoint:
                res = self.env['res.partner'].with_context({'lang':self.lang_code}).search([('id', '=', so.waypoint.id)])
                
                if so.lang_code == 'en_US':
                    if res.company_type == 'company':
                        company_name =  "Dear " + res.name if res.name else ''
                    else:
                        partner_name =  'Mr./Mrs. ' + res.last_name if res.last_name else ''
                    
                else:   
                    if res.company_type == 'company':
                        company_name =  res.name + ' 御中' if res.name else '' 
                    else:
                        partner_name =  res.last_name + ' 様' if res.last_name else ''
                
                if res.phone:
                    tel = res.phone
                elif res.mobile:
                    tel = res.mobile
                
                if res.fax:
                    fax = res.fax
                    
            if company_name and partner_name:
                send += company_name + '\n' + partner_name  
            elif company_name:
                send += company_name
            elif partner_name:
                send += partner_name 
                
            so.send_to_company_delivery = company_name
            so.send_to_people_delivery = partner_name
            so.dear_to_delivery = send
            
            if tel and fax:
                so.send_to_tel_fax = "TEL:" + tel + "/FAX:" + fax
            elif tel:
                so.send_to_tel_fax = "TEL:" + tel
            elif fax:
                so.send_to_tel_fax = "FAX:" + fax
            else:
                so.send_to_tel_fax = ""
            
    def _compute_sale_order_sipping_to(self):
        for record in self:
            sipping_to = ""
            if record.sipping_to:
                if record.sipping_to == "depo":
                    sipping_to = "デポ入れまで"
                elif record.sipping_to == "inst":
                    sipping_to = "搬入設置まで"
                elif record.sipping_to == "inst_depo":
                    sipping_to = "搬入設置（デポ入）"
                elif record.sipping_to == "direct":
                    sipping_to = "直送"
                elif record.sipping_to == 'container':
                    sipping_to = 'オランダコンテナ出荷'
                elif record.sipping_to == 'pick_up':
                    sipping_to = '引取'
                elif record.sipping_to == 'bring_in':
                    sipping_to = '持込'
            record.sale_order_sipping_to = sipping_to

    def _compute_sale_order_partner_address(self):
        for record in self:
            partner_address = ""
            partner = record.partner_id
            if partner:         
                if partner.zip:
                    partner_address += partner.zip + " "
                if record.lang_code == 'ja_JP':    
                    if partner.state_id.name:
                        partner_address += partner.state_id.name 
                    if partner.city:
                        partner_address += partner.city + " "
                    if partner.street:
                        partner_address += partner.street + " "
                    if partner.street2:
                        partner_address += partner.street2 + " "
                else:
                    if partner.street:
                        partner_address += partner.street + " "
                    if partner.street2:
                        partner_address += partner.street2 + " "
                    if partner.city:
                        partner_address += partner.city + " "
                    if partner.state_id.name:
                        partner_address += partner.state_id.name 
                    
            record.sale_order_partner_address = partner_address
            
    def _compute_sale_partner_info(self):
        for record in self:
            partner_info = ""  
            partner = record.partner_id
            if partner:         
                if partner.display_name:
                    if "," in partner.display_name:
                        partner_info += (
                            partner.display_name.split(",")[0]
                            + "-"
                            + partner.display_name.split(",")[1]
                            + _(" 様 ご依頼分"))
                    else:
                        partner_info += partner.display_name + _(" 様 ご依頼分")
                elif partner.name:
                        partner_info += partner.name + _(" 様 ご依頼分")
                        
                if partner.department:
                    partner_info += "-" + partner.department 
                if partner.site:
                    partner_info += "-" + partner.site
                    
            record.sale_order_partner_info = partner_info
            
    def _compute_bank(self):
        for record in self:
            if record.lang_code =="en_US":
                record.sale_order_bank_name = "Nippon City Bank (0190)"
                record.sale_order_bank_branch = "Chikushi Dori Branch (714)"
                record.sale_order_number_account = "(Regular) 0272585"
            elif record.lang_code =="ja_JP":
                record.sale_order_bank_name = "西日本シティ銀行 （0190）"
                record.sale_order_bank_branch = "筑紫通 （ﾁｸｼﾄﾞｵﾘ） 支店 （714）"
                record.sale_order_number_account = "（普）0272585"
            else:
                record.sale_order_bank_name = "Nippon City Bank (0190)"
                record.sale_order_bank_branch = "Chikushi Dori Branch (714)"
                record.sale_order_number_account = "(Regular) 0272585"
            
    def _compute_print_staff(self):
        for line in self:
            printing_staff = ''
            if line.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',line.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
            line.sale_order_printing_staff = printing_staff  
                   
    def _compute_sale_order_special_note(self):
        for l in self:
            if l.special_note :
                l.sale_order_special_note = l.special_note[:167] 
                l.sale_order_special_note_list_price = l.special_note[:100] 
            else:
                l.sale_order_special_note =""            
                l.sale_order_special_note_list_price =""            

    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.user.lang or 'en_US'

    def _compute_year_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.yearUnit = "-"
            else:
                record.yearUnit = "年"

    def _compute_month_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.monthUnit = "-"
            else:
                record.monthUnit = "月"

    def _compute_day_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.dayUnit = ""
            else:
                record.dayUnit = "日"
                
    def _compute_sale_order_transactions_term(self):
        for record in self:
            term = ''
            if record.partner_id.transactions:
                for transaction in record.partner_id.transactions:
                    term += str(transaction.name) + " "
            if record.partner_id.payment_terms_1:
                term += record.partner_id.payment_terms_1
            record.sale_order_transactions_term = term
            
        
    prescription_note = fields.Char(string="prescription note", compute="_compute_prescription_excel")
    prescription_note_detail = fields.Char(string="prescription note detail", compute="_compute_prescription_excel")
    
    prescription_company_name = fields.Char(string="prescription note", compute="_compute_prescription")
    prescription_address_info = fields.Char(string="prescription note detail", compute="_compute_prescription")
    prescription_address_country = fields.Char(string="prescription note", compute="_compute_prescription")
    prescription_tel_fax = fields.Char(string="prescription note detail", compute="_compute_prescription")
    prescription_email = fields.Char(string="prescription note", compute="_compute_prescription")
    
    def _compute_prescription(self):  
        for record in self:
            if record.lang_code == "it_IT":
                record.prescription_company_name = "Ritzwell Italia"
                record.prescription_address_info = "Via Bocchetto, 6"
                record.prescription_address_country = "Milano"
                record.prescription_tel_fax = "20123 (MI) Italy"
                record.prescription_email = ""
            else:
                record.prescription_company_name = "RITZWELL & CO."
                record.prescription_address_info = "5-2-9 ITAZUKE HAKATA-KU"
                record.prescription_address_country = "FUKUOKA,812-0888 JAPAN"
                record.prescription_tel_fax = "TEL: +81 92 584 2240 FAX: +81 92 584 2241"
                record.prescription_email = "E-mail: info@ritzwell.com"
    
    is_show_prescription_note_en = fields.Char(string="is show prescription note", compute="_compute_is_show_prescription_note_pdf")
    is_show_prescription_note_ita = fields.Char(string="is show prescription note", compute="_compute_is_show_prescription_note_pdf")
    is_show_prescription_note= fields.Char(string="is show prescription note", compute="_compute_prescription_excel")

    def _compute_is_show_prescription_note_pdf(self):  
        for record in self:
            is_enUS = False
            is_ita = False
            
            order_lines=self.env['sale.order.line'].search([('order_id','=',record.id)])
            if order_lines:
                for order in order_lines:
                    attributes_cfg=order.config_session_id.custom_value_ids
                    if attributes_cfg:
                        for cfg in attributes_cfg:
                            xml_id = self.env['ir.model.data'].search([
                                ('model', '=', 'product.attribute'),
                                ('res_id', '=', cfg.attribute_id.id)
                            ]).name
                            if xml_id.isdigit(): 
                                if int (xml_id) == 110 or int (xml_id) == 111 or int (xml_id) == 112:
                                    if record.lang_code =="en_US":
                                        is_enUS = True
                                    if record.lang_code =="it_IT":
                                        is_ita = True
                                    else:
                                        is_enUS = True
                                    break
            record.is_show_prescription_note_en = is_enUS
            record.is_show_prescription_note_ita = is_ita
            
    def _compute_prescription_excel(self):  
        for record in self:
            note = ""
            desc = ""
            is_show_note = False
            
            order_lines=self.env['sale.order.line'].search([('order_id','=',record.id)])
            if order_lines:
                for order in order_lines:
                    attributes_cfg=order.config_session_id.custom_value_ids
                    if attributes_cfg:
                        for cfg in attributes_cfg:
                            xml_id = self.env['ir.model.data'].search([
                                ('model', '=', 'product.attribute'),
                                ('res_id', '=', cfg.attribute_id.id)
                            ]).name
                            if xml_id.isdigit(): 
                                if int(xml_id) == 110 or int (xml_id) == 111 or int (xml_id) == 112:
                                    is_show_note = True
                                    break
                
            if is_show_note:
                if record.lang_code =="it_IT":
                    note += "NOTA"
                    desc += "*1 COL & COM" + "\n"+"L'Acquirente si impegna ad inviare COL&COM a Ritzwell in termini Incoterms DDP (resa sdoganata). Ciò significa che l'Acquirente supporta le spese di acquisto COL&COM e tutti i rischi e i costi del trasporto (tasse di esportazione, trasporto, assicurazione, spese portuali di destinazione, consegna alla destinazione finale fabbrica Ritzwell),nonché eventuali dazi doganali e dazi di importazione. L'indirizzo di consegna per COL&COM è il seguente." + "\n" + "   RITZWELL & CO. Attn. Atsuya Nakamura" + "\n" + "   NIJOYOSHII 3515-1 ITOSHIMA FUKUOKA 819-1641 JAPAN"+ "\n"+ "   TEL +81-92-326-8011"
                # if record.lang_code =="en_US":
                else:
                    note += "NOTE"
                    desc += "*1 COL & COM" + "\n"  +  "The Buyer has to send COL&COM to Ritzwell in Incoterms DDP (Delivered Duty Paid) term. This term means Buyer assumes purchasing COL&COM and all the risks and costs of transport (export fees, carriage, insurance, and destination port charges, delivery to the final destination Ritzwell factory) and pays any import customs and duty. The delivery address for COL&COM is as follows." + "\n" + "   RITZWELL & CO. Attn. Atsuya Nakamura" + "\n" + "   NIJOYOSHII 3515-1 ITOSHIMA FUKUOKA 819-1641 JAPAN"+ "\n"+ "   TEL +81-92-326-8011"
                    
            record.prescription_note = note
            record.prescription_note_detail = desc
            record.is_show_prescription_note = is_show_note
                
    def _compute_sale_order_hr_employee(self):
        for record in self:
            hr_employee_detail = ""
            hr_employee_detail_invoice = ""
            hr_employee_split_street = ""
            if record.hr_employee_company:
                hr_employee_detail += record.hr_employee_company + "\n"
                hr_employee_detail_invoice += record.hr_employee_company + "\n"
                hr_employee_split_street += record.hr_employee_company + "\n"
            if record.registration_number : 
                hr_employee_detail_invoice += record.registration_number + "\n"
            if record.hr_employee_department:
                hr_employee_detail += record.hr_employee_department + "\n"
                hr_employee_detail_invoice += record.hr_employee_department + "\n"
                hr_employee_split_street += record.hr_employee_department + "\n"
            if record.hr_employee_zip:
                hr_employee_detail += record.hr_employee_zip + "\n"
                hr_employee_detail_invoice += record.hr_employee_zip + "\n"
                hr_employee_split_street += record.hr_employee_zip + "\n"
            if record.hr_employee_info:
                hr_employee_detail += record.hr_employee_info + "\n"
                hr_employee_detail_invoice += record.hr_employee_info + "\n"
            if record.hr_employee_address1:
                hr_employee_split_street += record.hr_employee_address1 + "\n"
            if record.hr_employee_address2:
                hr_employee_split_street += record.hr_employee_address2 + "\n"
            if record.hr_employee_tel:
                hr_employee_detail += record.hr_employee_tel + "\n"
                hr_employee_detail_invoice += record.hr_employee_tel + "\n"
                hr_employee_split_street += record.hr_employee_tel + "\n"
            if record.hr_employee_fax:
                hr_employee_detail += record.hr_employee_fax + "\n"
                hr_employee_detail_invoice += record.hr_employee_fax + "\n"
                hr_employee_split_street += record.hr_employee_fax + "\n"
            if record.hr_employee_printer:
                hr_employee_detail += record.hr_employee_printer 
                hr_employee_detail_invoice += record.hr_employee_printer 
                hr_employee_split_street += record.hr_employee_printer 
            
            record.sale_order_hr_employee= hr_employee_detail.rstrip('\n')
            record.sale_order_hr_employee_invoice= hr_employee_detail_invoice.rstrip('\n')
            record.sale_order_hr_employee_split_street= hr_employee_split_street.rstrip('\n')

    def _compute_sale_order_preferred_delivery_period(self):
        for record in self:
            if record.preferred_delivery_period :
                record.sale_order_preferred_delivery_period = record.preferred_delivery_period
            else:
                record.sale_order_preferred_delivery_period = ""

    def _compute_sale_order_name(self):
        for line in self:
            if line.name:
                line.sale_order_name = line.name
            else:
                line.sale_order_name = ""

    def _compute_check_oversea(self):
        for record in self:
            if record.overseas:
                record.check_oversea = "海外 "
            else:
                record.check_oversea = ""

    def _compute_list_order_line(self):
        for record in self:
            record.list_order_line = record.order_line.filtered(lambda x: not x.is_pack_outside)

    def _compute_sale_order_title(self):
        for line in self:
            if line.title:
                line.sale_order_title = line.title
            else:
                line.sale_order_title = ""

    def _compute_sale_order_company_name(self):
        for line in self:
            company_name = ""
            partner = line.partner_id

            if partner:
                if partner.commercial_company_name:
                    company_name = partner.commercial_company_name
                elif partner.name:
                    company_name = partner.name

                if partner.department:
                    company_name += " " + partner.department

                if partner.user_id and partner.user_id.name :
                    company_name += " " + partner.user_id.name + " ご依頼分"

            line.sale_order_company_name = company_name
            
    def _compute_sale_order_waypoint(self):
        for line in self:
            waypoint = self.env["res.partner"].with_context({'lang':self.lang_code}).search([("id", "=", line.waypoint.id)], limit=1)

            company_name = ""
            address = ""

            if waypoint:
                if waypoint.company_type == "company":
                    company_name = waypoint.name
                else:
                    company_name = (waypoint.last_name + " " or '') + (waypoint.first_name or '')

                if waypoint.zip:
                    address += "〒" + waypoint.zip + " "
                    
                if line.lang_code == 'ja_JP':
                    if waypoint.state_id and waypoint.state_id.name:
                        address += waypoint.state_id.name + " "
                    if waypoint.city:
                        address += waypoint.city + " "
                    if waypoint.street:
                        address += waypoint.street + " "
                    if waypoint.street2:
                        address += waypoint.street2 
                else:
                    if waypoint.street:
                        address += waypoint.street + " "
                    if waypoint.street2:
                        address += waypoint.street2 + " "
                    if waypoint.city:
                        address += waypoint.city + " "
                    if waypoint.state_id and waypoint.state_id.name:
                        address += waypoint.state_id.name + " "

            line.sale_order_waypoint_name = company_name.strip()
            line.sale_order_waypoint_address = address.strip()

    def _compute_sale_order_info_cus(self):
        for line in self:
            info_cus = ""
            partner = line.partner_id
            if partner:
                user = partner.user_id
                if partner.name:
                    info_cus += partner.name + " "
                if partner.site:
                    info_cus += partner.site + " "
                if partner.department:
                    info_cus += partner.department + " "
                if user and user.name:
                    info_cus += user.name + " "
            info_cus = info_cus.rstrip()    
            line.sale_order_info_cus = info_cus + " ご依頼分"

    def _compute_sale_order_ritzwell_staff(self):
        for line in self:
            if line.user_id.name:
                if line.lang_code == 'ja_JP':
                    line.sale_order_ritzwell_staff = line.user_id.name + "  様宛"
                else:
                    line.sale_order_ritzwell_staff = "Mr/Mrs. " + line.user_id.name 
            else:
                line.sale_order_ritzwell_staff = ""

    def _compute_sale_order_date_planned(self):
        for line in self:
            order_lines = self.env["sale.order.line"].search(
                [("order_id", "=", line.id)]
            )
            if order_lines:
                max_date_planned = max(order_lines.mapped("date_planned"))
                if max_date_planned:
                    date_planned = (
                        str(max_date_planned.year)
                        + line.yearUnit
                        + str(max_date_planned.month)
                        + line.monthUnit
                        + str(max_date_planned.day)
                        + line.dayUnit
                    )
                    line.sale_order_date_planned = date_planned
                else:
                    line.sale_order_date_planned = ""

    def _compute_sale_order_detail_customer_info(self):
        info = ""
        for line in self:
            if line.partner_id.commercial_company_name:
                info += line.partner_id.commercial_company_name + "-"
            if line.partner_id.department:
                info += line.partner_id.department + "-"
            if line.partner_id.site:
                info += line.partner_id.site + "-"
            if line.partner_id.name:
                info += line.partner_id.name + "-"
            if line.name:
                info += line.name
            line.sale_order_detail_customer_info = info

    def _compute_sale_order_name_and_phone_staff(self):
        info = ""
        for line in self:
            if line.user_id.name:
                info += line.user_id.name
            if line.user_id.phone:
                info += " " + line.user_id.phone
            line.sale_order_name_and_phone_staff = info

    def _compute_sale_order_printing_staff(self):
        for line in self:
            printing_staff = ''
            if line.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',line.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
                        
            line.sale_order_printing_staff = printing_staff
                
    def _compute_sale_order_detail_address_partner(self):
        details = ""
        for line in self:
            if line.partner_id.zip:
                details += "〒" + line.partner_id.zip + " "
            if line.lang_code == 'ja_JP':
                if line.partner_id.state_id.name:
                    details += line.partner_id.state_id.name + " "
                if line.partner_id.city:
                    details += line.partner_id.city + " "
                if line.partner_id.street:
                    details += line.partner_id.street + " "
                if line.partner_id.street2:
                    details += line.partner_id.street2 
            else:
                if line.partner_id.street:
                    details += line.partner_id.street + " "
                if line.partner_id.street2:
                    details += line.partner_id.street2 + " "
                if line.partner_id.city:
                    details += line.partner_id.city + " "
                if line.partner_id.state_id.name:
                    details += line.partner_id.state_id.name + " "
            line.sale_order_detail_address_partner =  details

    def _compute_sale_order_tel_phone_partner(self):
        tel_phone = ""
        for line in self:
            if line.partner_id.phone and line.partner_id.mobile:
                tel_phone = line.partner_id.phone + "/" + line.partner_id.mobile
            elif line.partner_id.phone and not line.partner_id.mobile:
                tel_phone = line.partner_id.phone
            elif not line.partner_id.phone and line.partner_id.mobile:
                tel_phone = line.partner_id.mobile
            line.sale_order_tel_phone_partner = tel_phone
    
    def _compute_sale_order_missing_currency(self):
        for record in self:
            record.sale_order_amount_total = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_total) if record.amount_total else 0
            )
            record.sale_order_amount_untaxed = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_untaxed) if record.amount_untaxed else 0
            )
            record.sale_order_amount_tax = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_tax) if record.amount_tax else 0
            )

    def _compute_sale_order_missing_char(self):
        for record in self:
            record.sale_order_fax = "fax." + str(
                record.company_id.partner_id.fax
                if record.company_id.partner_id.fax
                else ""
            )
            record.sale_order_tel = "tel." + str(
                record.company_id.partner_id.phone
                if record.company_id.partner_id.phone
                else ""
            )
            record.sale_order_zip = "〒" + str(
                record.company_id.partner_id.zip
                if record.company_id.partner_id.zip
                else ""
            )

    def _compute_sale_order_current_date(self):
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        for record in self:
            record.sale_order_current_date = year + " " + record.yearUnit + " " + month + " " + record.monthUnit +" " + day + " "+ record.dayUnit

    def _compute_sale_order_format_date(self):
        for record in self:
            if record.estimated_shipping_date:
                record.sale_order_estimated_shipping_date = record._format_date(record.estimated_shipping_date, record.lang_code)
            else:
                record.sale_order_estimated_shipping_date = ""
                
            if record.date_order:
                record.sale_order_date_order = record._format_date(record.date_order, record.lang_code)
            else:
                record.sale_order_date_order = ""
                
            if record.validity_date:
                record.sale_order_validity_date = record._format_date(record.validity_date, record.lang_code)
            else:
                record.sale_order_validity_date = ""
                
            if record.shiratani_entry_date:
                record.sale_order_shiratani_entry_date = record._format_date(record.shiratani_entry_date, record.lang_code)
            else:
                record.sale_order_shiratani_entry_date = ""
                
            if record.preferred_delivery_date:
                record.sale_order_preferred_delivery_date = record._format_date(record.preferred_delivery_date, record.lang_code, True)
            else:
                record.sale_order_preferred_delivery_date = ""
                
            if record.warehouse_arrive_date:
                record.sale_order_warehouse_arrive_date = record._format_date(record.warehouse_arrive_date, record.lang_code)
            else:
                record.sale_order_warehouse_arrive_date = ""
                
            if record.date_deadline:
                record.sale_order_date_deadline = record._format_date(record.date_deadline, record.lang_code)
            else:
                record.sale_order_date_deadline = ""
                
    def _format_date(self, date, lang_code, is_preferred_delivery_date = False):
        format = 'yyyy-MM-dd'
        if lang_code == "ja_JP":
            format = 'y年M月d日'
            
        formatted_date = babel.dates.format_date(date, format=format, locale = lang_code)
        
        if is_preferred_delivery_date:
            day_of_week = babel.dates.format_date(date, format='EEE', locale = lang_code)
            return f"{formatted_date} [{day_of_week}]"
        
        return f"{formatted_date}"

    def _compute_sale_order_company_owner(self):
        for record in self:
            if record.partner_id.name:
                record.sale_order_company_owner = record.partner_id.name + " 様"
            else:
                record.sale_order_company_owner = ""

    def _compute_sale_order_list_price(self):
        for so in self:
            total_list_price = 0.0
            if so.order_line :
                for line in so.order_line:
                    total_list_price += line.price_unit * line.product_uom_qty
            so.sale_order_total_list_price =  '{0:,.0f}'.format(total_list_price)
    
    def _compute_sale_order_amount_untaxed2(self):
        for so in self:
            so.sale_order_amount_untaxed2 =  '{0:,.0f}'.format(so.amount_untaxed) if so.amount_untaxed else ''

    def _compute_sale_order_total_discount(self):
        for record in self:
            total_discount = 0.0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_discount += (
                    line.price_unit - line.price_reduce
                ) * line.product_uom_qty
            record.sale_order_total_discount = "- " + '{0:,.0f}'.format(total_discount)
            
    def _compute_sale_order_account_number(self):
        for record in self:
            if record.partner_id.bank_ids.acc_number:
                record.sale_order_account_number = "(普) " + str(
                    record.partner_id.bank_ids.acc_number
                )
            else:
                record.sale_order_account_number = ""

    def _compute_sale_order_send_to_company(self):
        for record in self:
            if record.partner_id.commercial_company_name:
                record.sale_order_send_to_company = (
                    "株式会社 " + record.partner_id.commercial_company_name + " 御中"
                )
            else:
                record.sale_order_send_to_company = (
                    "株式会社 " + record.partner_id.name + " 御中"
                )

    def _compute_sale_order_send_to_company2(self):
        for record in self:
            if record.company_id.partner_id.name:
                record.sale_order_send_to_company2 = (
                    "株式会社 " + record.company_id.partner_id.name+ " 御中"
                )
            else:
                record.sale_order_send_to_company2 =""
                
    def _compute_sale_order_draff_invoice(self):
        for line in self:
            invoice_name =''
            if line.name:
                invoice_name += line.name + '/'
            invoice_name += "Draft Invoice"
            line.sale_order_draff_invoice = invoice_name
    
class SaleOrderLineExcelReport(models.Model):
    _inherit = "sale.order.line"

    sale_order_number_and_size = fields.Char(
        compute="_compute_sale_order_number_and_size",
        string="品番・サイズ",
    )

    sale_order_product_detail = fields.Char(
        compute="_compute_sale_order_product_detail",
        string="仕様・詳細",
    )
    sale_order_product_detail_2 = fields.Char(
        compute="_compute_sale_order_product_detail",
        string="仕様・詳細",
    )
    sale_order_all_attribute = fields.Char(
        compute="_compute_sale_order_all_attribute",
        string="All attributes",
    )

    sale_order_sell_unit_price = fields.Char(
        compute="_compute_sale_order_sell_unit_price",
        string="販売単価",
    )
    sale_order_price_subtotal = fields.Char(
        compute="_compute_sale_order_price_subtotal",
        string="販売⾦額",
    )
    sale_order_amount_no_rate = fields.Char(
        compute="_compute_sale_order_amount_no_rate",
        string="販売⾦額",
    )
    
    sale_order_price_unit = fields.Char(
        compute="_compute_sale_order_price_unit",
        string="定価",
    )

    sale_order_index = fields.Integer(
        compute="_compute_sale_order_index",
        string="index",
    )

    sale_order_name = fields.Char(
        compute="_compute_sale_order_name",
        string="Name",
    )

    sale_order_product_summary = fields.Char(
        compute="_compute_sale_order_product_summary",
        string="Product summary",
    )

    sale_order_packages = fields.Char(
        compute="_compute_sale_order_packages",
        string="Packages",
    )

    sale_order_action_packages = fields.Char(
        compute="_compute_sale_order_action_packages",
        string="Action Package",
    )

    sale_order_action_assemble = fields.Char(
        compute="_compute_sale_order_action_assemble",
        string="Action Assemble",
    )

    sale_order_text_piece_leg = fields.Char(
        compute="_compute_sale_order_text_piece_leg",
        string="Text piece leg",
    )

    sale_order_date_order = fields.Char(
        compute="_compute_sale_order_date_order",
        string="Order date",
    )

    sale_order_voucher_class = fields.Char(
        compute="_compute_sale_order_voucher_class",
        string="Voucher Class",
    )

    sale_order_config_session = fields.Char(
        compute="_compute_sale_order_config_session",
        string="Config Session",
    )
    
    sale_order_line_discount = fields.Float (
        compute="_compute_sale_order_line_discount",
        string="Sale order line discount",
    )
    
    sale_line_product_uom_qty = fields.Char(string="sale_line_product_uom_qty" , compute="_compute_sale_line_product_uom_qty")
    sale_line_calculate_packages = fields.Integer('Packages' , compute="_compute_sale_line_calculate_packages")
    sale_line_product_no_delivery = fields.Char(string="Calculate product no delivery", compute="_compute_sale_line_product_no_pack")
    sale_line_product_pack_delivery = fields.Char(string="Calculate product pack delivery", compute="_compute_sale_line_product_no_pack")
    product_spec_detail = fields.Char(compute="_compute_sale_order_product_detail")
    
    def _compute_sale_line_product_no_pack(self):
        for line in self:
            prod_no = ""
            if line.product_id and line.product_id.product_no:
                prod_no = line.product_id.product_no
            
            prod_pack = ""
            pack_parent =  line.pack_parent_line_id   
            if pack_parent:
                prod = line.product_id
                if prod:
                    prod_tmplt = prod.product_tmpl_id
                    if prod_tmplt:
                        if prod_tmplt.seller_ids and line.order_partner_id.id:    
                            matching_sup = None  
                            for sup in prod_tmplt.seller_ids:
                                if sup.name.id == line.order_partner_id.id:
                                    matching_sup = sup 
                                    break
                            if matching_sup:
                                product_code = ("[" + matching_sup.product_code + "]") if matching_sup.product_code else ''
                                product_name = matching_sup.product_name if matching_sup.product_name else ''
                                prod_pack = product_code + product_name
                                
                        if not prod_pack:
                            if prod_tmplt.default_code and prod_tmplt.name:
                                prod_pack = "[" + prod_tmplt.default_code + "]" + prod_tmplt.name
                            elif prod_tmplt.default_code:
                                prod_pack = prod_tmplt.default_code 
                            elif prod_tmplt.name:
                                prod_pack = prod_tmplt.name 
                            
            line.sale_line_product_no_delivery = prod_no
            line.sale_line_product_pack_delivery = prod_pack
                
    def _compute_sale_line_calculate_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.sale_line_calculate_packages =  math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
            else:
                line.sale_line_calculate_packages = 0      
                
    def _compute_sale_line_product_uom_qty(self):
        for line in self:
            float_product_uom_qty = float(line.product_uom_qty)
            integer_part = int(line.product_uom_qty)
            decimal_part = round(float_product_uom_qty - integer_part,2)
            decimal_part_after_dot = int(str(decimal_part).split('.')[1])
            if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
                line.sale_line_product_uom_qty = integer_part 
            else:
                while decimal_part_after_dot % 10 == 0:
                    decimal_part_after_dot = decimal_part_after_dot / 10
                line.sale_line_product_uom_qty =  integer_part + float('0.' + str(decimal_part_after_dot))
                
    def _compute_sale_order_line_discount(self):
        for line in self:
            if line.discount != 0.00 or line.discount != 0.0 or line.discount != 0 :
                line.sale_order_line_discount = '{0:,.1f}'.format(100-line.discount)
            else:
                line.sale_order_line_discount = 0.0
                
            
    def _compute_sale_order_config_session(self):
        for line in self:
            config=""
            if line.p_type:
                if line.p_type =="special":
                    config += "別注" +"\n"
                if line.p_type =="custom":
                    config += "特注" +"\n"
            configCus=line.config_session_id.custom_value_ids
            if configCus:
                for cfg in configCus:
                    config += cfg.display_name + ":" + cfg.value + "\n"
            config.rstrip("\n")
            line.sale_order_config_session=config

    def _compute_sale_order_voucher_class(self):
        for line in self:
            line.sale_order_voucher_class = "受注引当"

    def _compute_sale_order_date_order(self):
        for line in self:
            if line.order_id.date_order:
                line.sale_order_date_order = line.order_id.date_order.strftime(
                    "%Y-%m-%d"
                )
            else:
                line.sale_order_date_order = ""

    def get_image_url(self, image_path, id):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        image_url = f"{base_url}/web/image?model={self._name}&field=image_256&id={id}&filename={image_path}"
        return image_url

    def _compute_sale_order_text_piece_leg(self):
        for line in self:
            line.sale_order_text_piece_leg = "脚"

    def _compute_sale_order_action_packages(self):
        for line in self:
            line.sale_order_action_packages = "有"

    def _compute_sale_order_action_assemble(self):
        for line in self:
            line.sale_order_action_assemble = "無"

    def _compute_sale_order_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.sale_order_packages = math.ceil(
                    line.product_uom_qty / line.product_id.two_legs_scale
                )
            else:
                line.sale_order_packages = line.product_uom_qty

    def _compute_sale_order_number_and_size(self):
        for line in self:
            product_no_pack_and_size = ""
            
            if line.sale_line_product_no_delivery and line.sale_line_product_pack_delivery:
                product_no_pack_and_size += line.sale_line_product_no_delivery + " / " + line.sale_line_product_pack_delivery
            elif line.sale_line_product_no_delivery:
                product_no_pack_and_size += line.sale_line_product_no_delivery
            elif line.sale_line_product_pack_delivery:
                product_no_pack_and_size += line.sale_line_product_pack_delivery
                
            product_no_pack_and_size += "\n"
            
            if line.product_size:
                product_no_pack_and_size += line.product_size
                
            line.sale_order_number_and_size = product_no_pack_and_size.rstrip("\n")

    def _compute_sale_order_product_detail(self):
        for line in self:
            attr = ""
            attr_cfg = ""
            attributes = line.product_id.product_template_attribute_value_ids  #attr default
            attributes_cfg=line.config_session_id.custom_value_ids             #attr custom 
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
                            attr += ("● " + cfg.display_name + "\n" )
                            count_cfg += 1
                            
                        for cfg2 in attributes_cfg[count_cfg:(6+count_cfg)]:
                            attr_cfg += ("● " + cfg2.display_name + "\n" )
                elif length_normal == 6 :
                    for attribute in attributes:
                        attr += ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" )                    
                    if attributes_cfg:                            
                        for cfg in attributes_cfg:
                            attr_cfg += ("● " + cfg.display_name + "\n" )
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
                                attr_cfg += ("● " + cfg.display_name + "\n" )
            else: 
                if attributes_cfg:                            
                    for cfg in attributes_cfg[:6]:
                        attr += ("● " +  cfg.display_name + "\n" )
                    for cfg in attributes_cfg[6:12]:
                        attr_cfg += ("● " +  cfg.display_name + "\n" )
                        
            attr = attr.rstrip()
            attr_cfg = attr_cfg.rstrip()
            
            line.sale_order_product_detail = attr
            line.product_spec_detail = attr.split("\n")[:6]
            line.sale_order_product_detail_2 = attr_cfg
            
    def _compute_sale_order_all_attribute(self):
        for line in self:
            attr = ""
            attributes = line.product_id.product_template_attribute_value_ids  #attr default
            attributes_cfg=line.config_session_id.custom_value_ids             #attr custom 
            
            if attributes:
                for attribute in attributes:
                    attr += ("● " + attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n" ) 
            if attributes_cfg: 
                for cfg2 in attributes_cfg:
                    attr += ("● " + cfg2.display_name  + ":" + cfg2.value  + "\n" )
                        
            attr = attr.rstrip()
            
            line.sale_order_all_attribute = attr

    def _compute_sale_order_product_summary(self):
        for line in self:
            attr = ""
            attributes = line.product_id.product_template_attribute_value_ids
            if attributes:
                for attribute in attributes:
                    attr += attribute.attribute_id.name + "\n"
            line.sale_order_product_summary = attr
                    
    def _compute_sale_order_sell_unit_price(self):
        for line in self:
            line.sale_order_sell_unit_price = '{0:,.0f}'.format(line.price_unit - line.price_unit * line.discount / 100 )
            
    def _compute_sale_order_price_subtotal(self):
        for line in self:
            line.sale_order_price_subtotal = '{0:,.0f}'.format(line.price_subtotal) if line.price_subtotal else ''
    
    def _compute_sale_order_amount_no_rate(self):
        for line in self:
            if line.product_uom_qty and line.price_unit :
                line.sale_order_amount_no_rate = '{0:,.0f}'.format(line.product_uom_qty * line.price_unit)
            else:
                line.sale_order_amount_no_rate = ''    
                
    def _compute_sale_order_price_unit(self):
        for line in self:
            line.sale_order_price_unit = '{0:,.0f}'.format(line.price_unit) if line.price_unit else ''

    def _compute_sale_order_index(self):
        index = 0
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.sale_order_index = ''
            else:
                index += 1
                line.sale_order_index = str(index)
                
    sale_order_name = fields.Text(
        compute="_compute_sale_order_name",
        string="Name",
    )
    
    sale_order_line_name_excel = fields.Text(
        compute="_compute_sale_order_line_name_detail",
        string="Name excel",
    )
    sale_order_line_name_pdf = fields.Text(
        compute="_compute_sale_order_line_name_detail",
        string="Name pdf",
    )  
    sale_order_line_summary_pdf = fields.Text(
        compute="_compute_sale_order_line_name_detail",
        string="Name pdf",
    )  
    sale_order_line_p_type_pdf = fields.Text(
        compute="_compute_sale_order_line_name_detail",
        string="Name pdf",
    )  

    def _compute_sale_order_name(self):
        for line in self:
            categ_name = ""
            if line.display_type == "line_section" or line.display_type == "line_note":
                categ_name = line.name if line.name else ""
            elif line.product_id:
                    prod_tmpl = line.product_id.product_tmpl_id
                    if prod_tmpl:
                        if prod_tmpl.config_ok :  
                            if prod_tmpl.categ_id and prod_tmpl.categ_id.name:
                                categ_name = prod_tmpl.categ_id.name
                            elif prod_tmpl.product_no :
                                categ_name = prod_tmpl.product_no
                            elif prod_tmpl.name  : 
                                categ_name = prod_tmpl.name   
                        else:
                            if prod_tmpl.seller_ids and line.order_id and line.order_id.partner_id and line.order_id.partner_id.id:
                                matching_sup = None  
                                for sup in prod_tmpl.seller_ids:
                                    if sup.name and sup.name.id and sup.name.id == line.order_id.partner_id.id:
                                            matching_sup = sup 
                                            break
                                if matching_sup:
                                    product_code = ("[" + str(matching_sup.product_code) + "]") if matching_sup.product_code else ''
                                    product_name = matching_sup.product_name if matching_sup.product_name else ''
                                    categ_name = product_code + product_name
                                else:
                                    categ_name =  prod_tmpl.name
                            else:
                                if prod_tmpl.default_code and prod_tmpl.name: 
                                    categ_name = "[" + str(prod_tmpl.default_code) + "]" + prod_tmpl.name
                                elif prod_tmpl.default_code :
                                    categ_name = "[" + str(prod_tmpl.default_code) + "]"
                                elif prod_tmpl.name :
                                    categ_name = prod_tmpl.name
                                            
            p_type = ""
            if line.p_type:
                if line.p_type == "special":
                    p_type = "別注"
                elif line.p_type == "custom":
                    p_type = "特注"

            prod = "" 
            if categ_name and p_type:
                prod += categ_name + "\n" + p_type
            elif categ_name:
                prod += categ_name
            elif p_type:
                prod += p_type
                        
            line.sale_order_name = prod   
            line.sale_order_line_name = categ_name   
            line.sale_order_line_p_type = p_type   
            
    def _compute_sale_order_line_name_detail(self):
        for line in self:
            categ_name = ""
            prod = line.product_id
            summary = ""
            if prod:
                prod_tmpl = prod.product_tmpl_id
                if prod_tmpl.config_ok:  
                    if prod_tmpl.categ_id and prod_tmpl.categ_id.name:
                        categ_name = prod_tmpl.categ_id.name
                    elif prod_tmpl.product_no:
                        categ_name = prod_tmpl.product_no
                    elif prod_tmpl.name: 
                        categ_name = prod_tmpl.name   
                elif line.name:
                    categ_name = line.name
                
                if prod_tmpl.summary:
                    summary = prod_tmpl.summary
                        
            p_type = ""
            if line.p_type == "special":
                p_type = "別注"
            elif line.p_type == "custom":
                p_type = "特注"
                    
            detail = ""
            if categ_name and summary and p_type:
                detail = categ_name + "\n" + summary + "\n" + p_type
            elif categ_name and summary:
                detail = categ_name + "\n" + summary
            elif categ_name and p_type:
                detail = categ_name + "\n" + p_type
            elif summary and p_type:
                detail = summary + "\n" + p_type 
            elif categ_name:
                detail = categ_name 
            elif summary:
                detail = summary 
            elif p_type:
                detail = p_type 

            line.sale_order_line_name_excel = detail       
            line.sale_order_line_name_pdf = categ_name       
            line.sale_order_line_p_type_pdf = p_type       
            line.sale_order_line_summary_pdf = summary       
class StockPickingExcelReport(models.Model):
    _inherit = "stock.picking"

    stock_move = fields.One2many(
        "stock.move",
        "picking_id",
        string="Stock move line",
        compute="_compute_stock_move",
    )

    stock_move_line = fields.One2many(
        "stock.move.line",
        "picking_id",
        string="Stock move line",
        compute="_compute_stock_move_line",
    )

    stock_picking_company_name = fields.Char(
        "Company name",
        compute="_compute_to_sale_order",
    )

    stock_picking_shiratani_entry_date = fields.Char(
        "Shiratani entry date",
        compute="_compute_to_sale_order",
    )

    stock_picking_scheduled_date = fields.Char(
        "Scheduled date",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_info = fields.Char(
        "Partner info",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_address = fields.Char(
        "Partner address",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_tel_phone = fields.Char(
        "Partner tel phone",
        compute="_compute_to_sale_order",
    )
    stock_picking_sipping_to = fields.Char(
        "Partner sipping to",
        compute="_compute_to_sale_order",
    )

    stock_picking_witness_name_phone = fields.Char(
        "Staff phone",
        compute="_compute_to_sale_order",
    )

    stock_picking_printing_staff = fields.Char(
        "Printing staff",
        compute="_compute_to_sale_order",
    )

    stock_picking_current_date = fields.Char(
        "Current date",
        compute="_compute_to_sale_order",
    )

    stock_estimated_shipping_date = fields.Char(
        "Estimated shipping date",
        compute="_compute_to_sale_order",
    )

    stock_scheduled_date = fields.Char(
        "Scheduled date",
        compute="_compute_to_sale_order",
    )

    stock_printing_staff = fields.Char(
        "Printing staff",
        compute="_compute_to_sale_order",
    )

    stock_shiratani_date = fields.Char(
        "Shiratani date",
        compute="_compute_to_sale_order",
    )
    
    check_oversea = fields.Char(
        "checkout oversea",
        compute="_compute_to_sale_order",
    )

    lang_code = fields.Char(string="Language Code", compute="_compute_lang_code")
    yearUnit = fields.Char(string="Year", compute="_compute_year_unit")
    monthUnit = fields.Char(string="Month", compute="_compute_month_unit")
    dayUnit = fields.Char(string="Day", compute="_compute_day_unit")
    
    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.user.lang or 'en_US'

    def _compute_year_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.yearUnit = "-"
            else:
                record.yearUnit = "年"

    def _compute_month_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.monthUnit = "-"
            else:
                record.monthUnit = "月"

    def _compute_day_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.dayUnit = ""
            else:
                record.dayUnit = "日"


    def _compute_lang_code(self):
        for sp in self:
            sp.lang_code = self.env.user.lang or 'en_US'
    
    def _compute_stock_move(self):
        for line in self:
            line.stock_move = self.env["stock.move"].search(
                [("picking_id", "=", line.id)]
            )
                
    def _compute_stock_move_line(self):
        for line in self:
            line.stock_move_line = self.env["stock.move.line"].search(
                [("picking_id", "=", line.id)]
            )

    def _compute_to_sale_order(self):
        for record in self:
            if record.sale_id.overseas:
                record.check_oversea = "海外 "
            else:
                record.check_oversea = ""

            if record.sale_id.partner_id.commercial_company_name:
                record.stock_picking_company_name = (
                    "株式会社 " + record.sale_id.partner_id.commercial_company_name + " 御中"
                )
            else:
                record.stock_picking_company_name = ""

            if record.sale_id.shiratani_entry_date:
                record.stock_picking_shiratani_entry_date = (
                    str(record.sale_id.shiratani_entry_date.year)
                    + record.yearUnit
                    + str(record.sale_id.shiratani_entry_date.month)
                    + record.monthUnit
                    + str(record.sale_id.shiratani_entry_date.day)
                    + record.dayUnit
                )
            else:
                record.stock_picking_shiratani_entry_date = ""

            xml_id = self.env['ir.model.data'].search([
                                ('model', '=', 'stock.location'),
                                ('res_id', '=', record.location_dest_id.id)
                            ]).name
            
            if xml_id == "stock_location_customers":
                if record.warehouse_arrive_date:
                    record.stock_picking_scheduled_date = (
                        str(record.warehouse_arrive_date.year)
                        + record.yearUnit
                        + str(record.warehouse_arrive_date.month)
                        + record.monthUnit
                        + str(record.warehouse_arrive_date.day)
                        + record.dayUnit
                    )
                else:
                    record.stock_picking_scheduled_date =""
            else:
                if record.shiratani_entry_date:
                    record.stock_picking_scheduled_date = (
                        str(record.shiratani_entry_date.year)
                        + record.yearUnit
                        + str(record.shiratani_entry_date.month)
                        + record.monthUnit
                        + str(record.shiratani_entry_date.day)
                        + record.dayUnit
                    )
                else:
                    record.stock_picking_scheduled_date =""

            partner_info = ""            
            if record.sale_id.partner_id.display_name:
                if "," in record.sale_id.partner_id.display_name:
                    partner_info += (
                        record.sale_id.partner_id.display_name.split(",")[0]
                        + "-"
                        + record.sale_id.partner_id.display_name.split(",")[1]
                        + (" Requesting-" if record.lang_code == "en_US" else " 様 ご依頼分-")
                                    )
                else:
                    partner_info += record.sale_id.partner_id.display_name + (" Requesting-" if record.lang_code == "en_US" else " 様 ご依頼分-")
            else:
                if record.sale_id.partner_id.name:
                    partner_info += record.sale_id.partner_id.name + (" Requesting-" if record.lang_code == "en_US" else " 様 ご依頼分-")
                    
            if record.sale_id.partner_id.department:
                partner_info += record.sale_id.partner_id.department + "-"
            if record.sale_id.partner_id.site:
                partner_info += record.sale_id.partner_id.site + "-"
            if record.sale_id.name:
                partner_info += record.sale_id.name
            record.stock_picking_partner_info = partner_info

            partner_address = ""
            if record.sale_id.partner_id.zip:
                partner_address += record.sale_id.partner_id.zip + " "
            if record.lang_code == 'ja_JP':    
                if record.sale_id.partner_id.state_id.name:
                    partner_address += record.sale_id.partner_id.state_id.name 
                if record.sale_id.partner_id.city:
                    partner_address += record.sale_id.partner_id.city + " "
                if record.sale_id.partner_id.street:
                    partner_address += record.sale_id.partner_id.street + " "
                if record.sale_id.partner_id.street2:
                    partner_address += record.sale_id.partner_id.street2 + " "
            else:
                if record.sale_id.partner_id.street:
                    partner_address += record.sale_id.partner_id.street + " "
                if record.sale_id.partner_id.street2:
                    partner_address += record.sale_id.partner_id.street2 + " "
                if record.sale_id.partner_id.city:
                    partner_address += record.sale_id.partner_id.city + " "
                if record.sale_id.partner_id.state_id.name:
                    partner_address += record.sale_id.partner_id.state_id.name 
            record.stock_picking_partner_address = ("〒" + partner_address) if partner_address else ""

            partner_tel_phone = ""
            if record.sale_id.partner_id.phone and record.sale_id.partner_id.mobile:
                partner_tel_phone = (
                    record.sale_id.partner_id.phone
                    + "/"
                    + record.sale_id.partner_id.mobile
                )
            elif (
                record.sale_id.partner_id.phone and not record.sale_id.partner_id.mobile
            ):
                partner_tel_phone = record.sale_id.partner_id.phone
            elif (
                not record.sale_id.partner_id.phone and record.sale_id.partner_id.mobile
            ):
                partner_tel_phone = record.sale_id.partner_id.mobile
            record.stock_picking_partner_tel_phone = partner_tel_phone

            sipping_to = ""
            if record.sale_id.sipping_to:
                if record.sale_id.sipping_to == "depo":
                    sipping_to = "デポ入れまで"
                elif record.sale_id.sipping_to == "inst":
                    sipping_to = "搬入設置まで"
                elif record.sale_id.sipping_to == "inst_depo":
                    sipping_to = "搬入設置（デポ入）"
                elif record.sale_id.sipping_to == "direct":
                    sipping_to = "直送"
                elif record.sale_id.sipping_to == 'container':
                    sipping_to = 'オランダコンテナ出荷'
                elif record.sale_id.sipping_to == 'pick_up':
                    sipping_to = '引取'
                elif record.sale_id.sipping_to == 'bring_in':
                    sipping_to = '持込'
            record.stock_picking_sipping_to = sipping_to
            

            witness_name_phone = ""
            if record.sale_id.witness:
                witness_name_phone += record.sale_id.witness + " " 
            if record.sale_id.witness_phone:
                witness_name_phone += record.sale_id.witness_phone
            record.stock_picking_witness_name_phone = witness_name_phone.rstrip()

            printing_staff = ""
            if record.sale_id and record.sale_id.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',record.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
            record.stock_picking_printing_staff = printing_staff

            day = str(datetime.now().day)
            month = str(datetime.now().month)
            year = str(datetime.now().year)
            record.stock_picking_current_date = (
                year + " " + record.yearUnit + " " + month + " " + record.monthUnit +" " + day + " "+ record.dayUnit
            )

            estimated_shipping_date = record.estimated_shipping_date
            if estimated_shipping_date:
                record.stock_estimated_shipping_date = (
                    str(estimated_shipping_date.year)
                    + record.yearUnit
                    + str(estimated_shipping_date.month)
                    + record.monthUnit
                    + str(estimated_shipping_date.day)
                    + record.dayUnit
                )
            else:
                record.stock_estimated_shipping_date = ""

            scheduled_date = record.scheduled_date
            if scheduled_date:
                record.stock_scheduled_date = (
                    str(scheduled_date.year)
                    + record.yearUnit
                    + str(scheduled_date.month)
                    + record.monthUnit
                    + str(scheduled_date.day)
                    + record.dayUnit
                )
            else:
                record.stock_scheduled_date = ""
                
            printing_staff = ''
            if record.sale_id and record.sale_id.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',record.sale_id.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
            record.stock_printing_staff = printing_staff  
class StockMoveExcelReport(models.Model):
    _inherit = "stock.move"
    calculate_packages = fields.Integer('Packages' , compute="_compute_calculate_packages")

    calculate_product_pack = fields.Char(
        string="Calculate product pack",
        compute="_compute_calculate_product_pack",
        default=""
    )
    calculate_product_pack_pdf = fields.Char(
        string="Calculate product pack pdf",
        compute="_compute_calculate_product_pack_pdf",
    )
    
    sale_line_instruction_status = fields.Char( compute="_compute_sale_line" )

    def _compute_sale_line(self):
        for line in self:
            status = ''
            if line.stock_move_sale_line_id and line.stock_move_sale_line_id.instruction_status:
                status = '有'
            line.sale_line_instruction_status = status
            
    def _compute_calculate_product_pack(self):
        for line in self:
            if line.stock_move_sale_line_id.pack_parent_line_id:
                line.calculate_product_pack = ' / ' + line.stock_move_sale_line_id.pack_parent_line_id.product_id.name
            else:
                line.calculate_product_pack = ''
                
    def _compute_calculate_product_pack_pdf(self):
        for line in self:
            categ_name = ""
            if line.product_id.product_tmpl_id.seller_ids and line.picking_id.partner_id.id:
                matching_sup = None  

                for sup in line.product_id.product_tmpl_id.seller_ids:
                    if sup.name.id == line.picking_id.partner_id.id:
                        matching_sup = sup 
                        break
                if matching_sup:
                    product_code = ("[" + str(matching_sup.product_code) + "]") if matching_sup.product_code else ''
                    product_name = str(matching_sup.product_name) if matching_sup.product_name else ''
                    categ_name = product_code + product_name
                else:
                    if line.product_id.product_tmpl_id.default_code:
                        categ_name = "[" +line.product_id.product_tmpl_id.default_code +"]" + line.product_id.product_tmpl_id.name
                    else:
                        categ_name =  line.product_id.product_tmpl_id.name
            else:
                if line.product_id.product_tmpl_id.default_code:
                    categ_name = "[" +line.product_id.product_tmpl_id.default_code +"]" + line.product_id.product_tmpl_id.name
                else:
                    categ_name =  line.product_id.product_tmpl_id.name
            line.calculate_product_pack_pdf =  categ_name
        

    def _compute_calculate_packages(self):
        for move in self:
            if move.product_id.two_legs_scale:
                move.calculate_packages = math.ceil(move.product_uom_qty / move.product_id.two_legs_scale)
            else:
                move.calculate_packages = move.product_uom_qty

    stock_index = fields.Char(
        "Stock index",
        compute="_compute_stock_move",
    )
    product_name = fields.Char(
        "Product name",
        compute="_compute_stock_move",
    )

    product_number_and_size = fields.Char(
        "Product number and size",
        compute="_compute_stock_move",
    )

    product_attribute = fields.Char(
        "Product attribute",
        compute="_compute_stock_move",
    )

    action_packages = fields.Char(
        "Action packages",
        compute="_compute_stock_move",
    )

    action_assemble = fields.Char(
        "Action assemble",
        compute="_compute_stock_move",
    )

    stock_sai = fields.Char(
        "Stock sai",
        compute="_compute_stock_move",
    )

    stock_warehouse = fields.Char(
        "Stock warehouse",
        compute="_compute_stock_move",
    )

    stock_shiratani_date = fields.Char(
        "Shiratani date",
        compute="_compute_stock_move",
    )
    
    stock_move_product_uom_qty = fields.Char(
        "Shiratani date",
        compute="_compute_stock_move",
    )
    
    product_pack_and_prod_no = fields.Char(
        "Product pack and prod no",
        compute="_compute_stock_move",
    )
    
    stock_product_uom_qty = fields.Char(string="stock_product_uom_qty" , compute="_compute_stock_product_uom_qty")
                
    def _compute_stock_product_uom_qty(self):
        for line in self:
            float_product_uom_qty = float(line.product_uom_qty)
            integer_part = int(line.product_uom_qty)
            decimal_part = round(float_product_uom_qty - integer_part,2)
            decimal_part_after_dot = int(str(decimal_part).split('.')[1])
            if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
                line.stock_product_uom_qty = integer_part 
            else:
                while decimal_part_after_dot % 10 == 0:
                    decimal_part_after_dot = decimal_part_after_dot / 10
                line.stock_product_uom_qty =  integer_part + float('0.' + str(decimal_part_after_dot))


    def _compute_stock_move(self):
        index = 0
        for line in self:
            product_attribute = ""
            index = index + 1
            line.stock_index = index
            
            prod = line.product_id
            categ_name = ""
            
            if prod:
                prod_tmpl = prod.product_tmpl_id
                if prod_tmpl.config_ok :  
                    categ_id = prod_tmpl.categ_id
                    prod_no = prod_tmpl.product_no
                    prod_name = prod_tmpl.name
                    if categ_id and categ_id.name:
                        categ_name = categ_id.name 
                    elif prod_no :
                        categ_name = prod_no
                    elif prod_name: 
                        categ_name = prod_name
                elif line.description_picking:
                    categ_name =  line.description_picking
                    
                if prod.product_template_attribute_value_ids:
                    for attribute_value in prod.product_template_attribute_value_ids:
                        attribute_name = attribute_value.attribute_id.name
                        attribute_value_name = attribute_value.product_attribute_value_id.name

                        if attribute_name and attribute_value_name:
                            product_attribute += (
                                f"● {attribute_name}:{attribute_value_name}\n"
                            )
            line.product_attribute = product_attribute   
            
            other_size = ""
            if line.stock_move_product_size:
                other_size = line.stock_move_product_size
                    
            p_type = ""            
            if line.p_type == "special":
                p_type = "別注"
            elif line.p_type == "custom":
                p_type = "特注"
                    
            product_name = ""
            if categ_name and p_type:
                product_name = categ_name + "\n" + p_type
            elif categ_name:
                product_name = categ_name 
            elif p_type:
                product_name = p_type         
                    
            line.product_name = product_name

            size_detail = "" 
            prod_no = ""
            prod_pack = ""
            if line.stock_move_sale_line_id:
                pack_parent =  line.stock_move_sale_line_id.pack_parent_line_id   
                if pack_parent:
                    if pack_parent.product_id and pack_parent.product_id.product_no:
                        prod_no = pack_parent.product_id.product_no
                    if line.calculate_product_pack_pdf:
                        prod_pack = line.calculate_product_pack_pdf
                    if prod_no and prod_pack:
                        size_detail += prod_no + '/' + prod_pack
                    elif prod_no:
                        size_detail = prod_no
                    elif prod_pack:
                        size_detail = prod_pack
                else:
                    size_detail += prod.product_no if prod and prod.product_no else ''

            if size_detail and other_size :
                line.product_number_and_size = size_detail + '\n' + other_size
            elif size_detail:
                line.product_number_and_size = size_detail
            elif other_size:
                line.product_number_and_size = other_size
            else:
                line.product_number_and_size = ''
            
            line.action_packages = "有"
            line.action_assemble = "無"
            line.stock_sai = prod_tmpl.sai if prod_tmpl.sai else ''
            line.stock_warehouse = line.warehouse_id.name if line.warehouse_id and line.warehouse_id.name else ''
            line.stock_shiratani_date = line.stock_move_sale_line_id.shiratani_date if line.stock_move_sale_line_id and line.stock_move_sale_line_id.shiratani_date else ''
            line.product_pack_and_prod_no = size_detail
            
    stock_move_line_name_excel = fields.Text(compute="_compute_stock_move_line_name_detail")
    stock_move_line_name_pdf = fields.Text(compute="_compute_stock_move_line_name_detail")  
    stock_move_line_summary_pdf = fields.Text(compute="_compute_stock_move_line_name_detail")  
    stock_move_line_p_type_pdf = fields.Text(compute="_compute_stock_move_line_name_detail")          
    def _compute_stock_move_line_name_detail(self):
        for line in self:
            categ_name = ""
            prod = line.product_id
            summary = ""
            if prod:
                prod_tmpl = prod.product_tmpl_id
                if prod_tmpl.config_ok:  
                    if prod_tmpl.categ_id and prod_tmpl.categ_id.name:
                        categ_name = prod_tmpl.categ_id.name
                    elif prod_tmpl.product_no:
                        categ_name = prod_tmpl.product_no
                    elif prod_tmpl.name: 
                        categ_name = prod_tmpl.name   
                elif line.name:
                    categ_name = line.name
                
                if prod_tmpl.summary:
                    summary = prod_tmpl.summary
                        
            p_type = ""
            if line.p_type == "special":
                p_type = "別注"
            elif line.p_type == "custom":
                p_type = "特注"
                    
            detail = ""
            if categ_name and summary and p_type:
                detail = categ_name + "\n" + summary + "\n" + p_type
            elif categ_name and summary:
                detail = categ_name + "\n" + summary
            elif categ_name and p_type:
                detail = categ_name + "\n" + p_type
            elif summary and p_type:
                detail = summary + "\n" + p_type 
            elif categ_name:
                detail = categ_name 
            elif summary:
                detail = summary 
            elif p_type:
                detail = p_type 

            line.stock_move_line_name_excel = detail    
            line.stock_move_line_name_pdf = categ_name   
            line.stock_move_line_p_type_pdf = p_type 
            line.stock_move_line_summary_pdf = summary
class AccountMoveExcelReport(models.Model):
    _inherit = "account.move"

    sale_order_line = fields.One2many(
        "sale.order.line",
        string="Sale order line",
        compute="_compute_sale_order_line",
    )

    account_move_line = fields.One2many(
        "account.move.line",
        string="Account move line",
        compute="_compute_account_move_line",
    )

    sale_order = fields.One2many(
        "sale.order",
        string="Sale order",
        compute="_compute_sale_order",
    )

    send_company = fields.Char(
        "Send company",
        compute="_compute_send_company",
    )

    to_receiver = fields.Char(
        "To receiver",
        compute="_compute_to_receiver",
    )

    printing_staff = fields.Char(
        "Printing staff",
        compute="_compute_printing_staff",
    )

    acc_move_payment_term = fields.Char(
        "Account move payment term",
        compute="_compute_acc_move_payment_term",
    )

    bank_acc_number = fields.Char(
            "Bank account number",
            compute="_compute_bank_acc_number",
        )
    
    acc_move_invoice_date_due = fields.Char(
        "Acc move confirm date",
        compute="_compute_acc_move_confirm_date",
    )

    acc_move_shipping_date = fields.Char(
        "Acc move confirm date",
        compute="_compute_acc_move_confirm_date",
    )

    acc_move_current_date = fields.Char(
        "Acc move confirm date",
        compute="_compute_acc_move_confirm_date",
    )

    acc_move_invoice_name = fields.Char(
        "Acc move invoice name",
        compute="_compute_acc_move_invoice_name",
    )
    
    acc_move_print_staff = fields.Char(
        "Acc move print staff",
        compute="_compute_acc_move_print_staff"
    )

    lang_code = fields.Char(string="Language Code", compute="_compute_lang_code")
    yearUnit = fields.Char(string="Year", compute="_compute_year_unit")
    monthUnit = fields.Char(string="Month", compute="_compute_month_unit")
    dayUnit = fields.Char(string="Day", compute="_compute_day_unit")
    
    acc_move_amount_total = fields.Char(
        compute="_compute_acc_move_missing_currency",
        string="Amount total",
    )
    acc_move_amount_untaxed = fields.Char(
        compute="_compute_acc_move_missing_currency",
        string="Amount untax",
    )
    acc_move_amount_tax = fields.Char(
        compute="_compute_acc_move_missing_currency",
        string="Amount tax",
    )
    
    acc_move_draff_invoice= fields.Char(
        compute="_compute_acc_move_draff_invoice",
        string="invoice name",
    )
       
    acc_move_total_list_price = fields.Char(
        compute="_compute_acc_move_list_price",
        string="Total List Price",
    )
    
    def _compute_acc_move_list_price(self):
        for move in self:
            total_list_price = 0.0
            if move.invoice_line_ids :
                for line in move.invoice_line_ids:
                    total_list_price += line.price_unit * line.quantity
            move.acc_move_total_list_price = '{0:,.0f}'.format(total_list_price)
                
    def _compute_acc_move_draff_invoice(self):
        for line in self:
            invoice_name =''
            if line.invoice_origin:
                invoice_name += line.invoice_origin + '/'
            if line.state == 'draft':
                invoice_name += 'Draft Invoice'
                if line.name != '/':
                    invoice_name += line.name              
            if line.state == 'posted':  
                invoice_name += 'Invoice ' + line.name        
            line.acc_move_draff_invoice = invoice_name

    def _compute_acc_move_missing_currency(self):
        for record in self:
            record.acc_move_amount_total = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_total) if record.amount_total else 0
            )
            record.acc_move_amount_untaxed = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_untaxed) if record.amount_untaxed else 0
            )
            record.acc_move_amount_tax = record.currency_id.symbol + str(
                '{0:,.0f}'.format(record.amount_tax) if record.amount_tax else 0
            )
    
    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.user.lang or 'en_US'

    def _compute_year_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.yearUnit = "-"
            else:
                record.yearUnit = "年"

    def _compute_month_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.monthUnit = "-"
            else:
                record.monthUnit = "月"

    def _compute_day_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.dayUnit = ""
            else:
                record.dayUnit = "日"

    def _compute_lang_code(self):
        for l in self:
            l.lang_code = self.env.user.lang or 'en_US'
            
    def _compute_acc_move_print_staff(self):
        for l in self:
            staff = ''
            if l.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',l.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        staff = res.name if res.name else ''
            l.acc_move_print_staff = staff
                
    def _compute_acc_move_invoice_name(self):
        for line in self:
            invoice_name =''
            if line.invoice_origin:
                invoice_name += line.invoice_origin + '/'
            if line.state == "draft":
                if line.name =='/':
                    invoice_name += "Draft Invoice"
                else:
                    invoice_name += "Draft Invoice " + line.name
            if line.state == "posted":
                invoice_name += "Invoice " + line.name
                
            line.acc_move_invoice_name = invoice_name
    
    def _compute_acc_move_payment_term(self):
        for line in self:
            line.acc_move_payment_term = (
                line.invoice_payment_term_id.name
                if line.invoice_payment_term_id.name
                else ""
            )
    
    def _compute_bank_acc_number(self):
        for line in self:
            line.bank_acc_number = (
                "(普) " + line.partner_id.bank_ids.acc_number
                if line.partner_id.bank_ids.acc_number
                else ""
            )

    def _compute_acc_move_confirm_date(self):
        for line in self:
            invoice_date_due = line.invoice_date_due
            ship_date = line.date
            day = str(datetime.now().day)
            month = str(datetime.now().month)
            year = str(datetime.now().year)
            line.acc_move_current_date = year + " " + line.yearUnit + " " + month + " " + line.monthUnit +" " + day + " "+ line.dayUnit

            if invoice_date_due:
                line.acc_move_invoice_date_due = (
                    str(invoice_date_due.year)
                    + line.yearUnit
                    + str(invoice_date_due.month)
                    + line.monthUnit
                    + str(invoice_date_due.day)
                    + line.dayUnit
                )
            else:
                line.acc_move_invoice_date_due = ""

            if ship_date:
                line.acc_move_shipping_date = (
                    str(ship_date.year)
                    + line.yearUnit
                    + str(ship_date.month)
                    + line.monthUnit
                    + str(ship_date.day)
                    + line.dayUnit
                )
            else:
                line.acc_move_shipping_date = ""

    def _compute_send_company(self):
        for line in self:
            if line.partner_id.commercial_company_name:
                line.send_company = (
                    "株式会社 " + line.partner_id.commercial_company_name + " 御中"
                )
            else:
                line.send_company = ""

    def _compute_to_receiver(self):
        for line in self:
            if line.partner_id.name:
                line.to_receiver = line.partner_id.name + " 様"
            else:
                line.to_receiver = ""

    def _compute_printing_staff(self):
        for line in self:
            if line.user_id.name:
                line.printing_staff = line.user_id.name + " 様"
            else:
                line.printing_staff = ""

    def _compute_sale_order(self):
        for line in self:
            line.sale_order = self.env["sale.order"].search(
                [("name", "=", line.invoice_origin)]
            )

    def _compute_sale_order_line(self):
        for line in self:
            line.sale_order_line = self.env["sale.order.line"].search(
                [("order_id.name", "=", line.invoice_origin)]
            )

    def _compute_account_move_line(self):
        for line in self:
            line.account_move_line = line.invoice_line_ids
class AccountMoveLineExcelReport(models.Model):
    _inherit = "account.move.line"

    acc_line_index = fields.Integer(
        compute="_compute_acc_line_index",
        string="Account line index",
    )

    acc_line_number_and_size = fields.Char(
        compute="_compute_acc_line_number_and_size",
        string="品番・サイズ",
    )
    
    acc_line_product_detail = fields.Char(
        compute="_compute_acc_line_product_detail",
        string="仕様・詳細",
    )
    acc_line_product_detail2 = fields.Char(
        compute="_compute_acc_line_product_detail",
        string="仕様・詳細",
    )

    acc_line_discount = fields.Char(
        compute="_compute_acc_line_discount",
        string="discount",
    )   

    acc_line_sell_unit_price = fields.Char(
        compute="_compute_acc_line_sell_unit_price",
        string="sell unit price",
    )
    
    acc_line_name = fields.Char(
        compute="_compute_acc_line_name",
        string="acc line name excel",
    )
    
    acc_line_name_pdf = fields.Char(
        compute="_compute_acc_line_name",
        string="acc line name pdf",
    )
    
    acc_line_price_subtotal = fields.Char(
        compute="_compute_acc_line_price_subtotal",
        string="販売⾦額",
    )
    
    acc_line_price_unit = fields.Char(
        compute="_compute_acc_line_price_unit",
        string="定価",
    )  
            
    def _compute_acc_line_price_subtotal(self):
        for line in self:
            line.acc_line_price_subtotal = '{0:,.0f}'.format(line.price_subtotal) if line.price_subtotal else ''
    
    def _compute_acc_line_price_unit(self):
        for line in self:
            line.acc_line_price_unit = '{0:,.0f}'.format(line.price_unit) if line.price_unit else ''

    def _compute_acc_line_name(self):
        for line in self:
            name = ""
            summary = ""
            if line.product_id: 
                prod_tmpl = line.product_id.product_tmpl_id
                if prod_tmpl:
                    if prod_tmpl.config_ok:  
                        if prod_tmpl.categ_id and prod_tmpl.categ_id.name:
                            name = prod_tmpl.categ_id.name
                        elif prod_tmpl.product_no:
                            name = prod_tmpl.product_no
                        else: 
                            name = prod_tmpl.name   
                    else:
                        # case product is standard Prod + download payment
                        if prod_tmpl.seller_ids and line.move_id and line.move_id.partner_id and line.move_id.partner_id.id:
                            matching_sup = None  
                            for sup in prod_tmpl.seller_ids:
                                if sup.name and sup.name.id and sup.name.id == line.move_id.partner_id.id:
                                        matching_sup = sup 
                                        break
                            if matching_sup:
                                product_code = ("[" + str(matching_sup.product_code) + "]") if matching_sup.product_code else ''
                                product_name = matching_sup.product_name if matching_sup.product_name else ''
                                name = product_code + product_name
                            else:
                                name =  line.name
                        else:
                            name =  line.name
                if line.product_id.summary:
                    summary = line.product_id.summary
            
            if name and summary:
                line.acc_line_name = name + "\n"+ summary
            elif name:
                line.acc_line_name = name
            elif summary:
                line.acc_line_name = summary
            
            line.acc_line_name_pdf = name
            
    def _compute_acc_line_index(self):
        index = 0
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.acc_line_index = ''
            else:
                index += 1
                line.acc_line_index = str(index)

    def _compute_acc_line_number_and_size(self):
        for line in self:
            product_number_and_size = ""
            prod = line.product_id
            if prod :
                product_tmpl = prod.product_tmpl_id
                if product_tmpl:
                    if product_tmpl.product_no:
                        product_number_and_size +=  product_tmpl.product_no + "\n"
                        
            if line.sale_line_ids and line.sale_line_ids.product_size:
                product_number_and_size += line.sale_line_ids.product_size
            
            line.acc_line_number_and_size = product_number_and_size.rstrip("\n")
                
    def _compute_acc_line_product_detail(self):
        for line in self:
            attr = ""
            attr_2= ""
            
            if line.product_id and line.product_id.product_template_attribute_value_ids :
                attribute_values = line.product_id.product_template_attribute_value_ids 
                length_attribute_values = len(attribute_values)
                
                if length_attribute_values <= 6 :
                    for l in attribute_values:
                        attr += ("● " + l.attribute_id.name + ":" + l.product_attribute_value_id.name + "\n" ) 
                else:
                    for l in attribute_values[:6]:
                        attr += ("● " + l.attribute_id.name + ":" + l.product_attribute_value_id.name + "\n" ) 
                    for l in attribute_values[6:12]:
                        attr_2 += ("● " + l.attribute_id.name + ":" + l.product_attribute_value_id.name + "\n" )
                                    
            attr = attr.rstrip()
            attr_2 = attr_2.rstrip()                        
            line.acc_line_product_detail = attr
            line.acc_line_product_detail2 = attr_2
    
    def _compute_acc_line_discount(self):
        for line in self:
            if  line.discount != 0.00 or line.discount != 0.0 or line.discount != 0 :
                line.acc_line_discount = '{0:,.1f}'.format(100-line.discount)
            else:
                line.acc_line_discount = ""
    
    acc_line_price_subtotal = fields.Char(
        compute="_compute_acc_line_price_subtotal",
        string="販売⾦額",
    )
    
    acc_line_price_unit = fields.Char(
        compute="_compute_acc_line_price_unit",
        string="定価",
    )   
    mrp_join_partner_address = fields.Char(
        "Partner info",
        compute="_compute_mrp_join_partner",
    )
    
    mrp_join_partner_company_name = fields.Char(
        "Partner info",
        compute="_compute_mrp_join_partner",
    )
    
    def _compute_mrp_join_partner(self):
        for line in self:
            address = ""
            company_name = ""
            
            picking = line.picking_type_id
            if picking:
                warehouse = picking.warehouse_id
                if warehouse :
                    partner = warehouse.partner_id
                    if partner :
                        if partner.zip:
                            address += "〒" + partner.zip + " "
                            
                        if line.lang_code == 'ja_JP':
                            if partner.state_id and partner.state_id.name:
                                address += partner.state_id.name + " "
                            if partner.city:
                                address += partner.city + " "
                            if partner.street:
                                address += partner.street + " "
                            if partner.street2:
                                address += partner.street2 
                        else:
                            if partner.street:
                                address += partner.street + " "
                            if partner.street2:
                                address += partner.street2 + " "
                            if partner.city:
                                address += partner.city + " "
                            if partner.state_id and partner.state_id.name:
                                address += partner.state_id.name + " "
                                
                        if partner.commercial_company_name:
                            company_name = partner.commercial_company_name
                        elif partner.name:
                            company_name = partner.name
                            
                        if partner.department:
                            company_name += " " + partner.department
                            
                        if partner.user_id and partner.user_id.name :
                            company_name += " " + partner.user_id.name + " ご依頼分"
                        
            line.mrp_join_partner_address = address.strip()
            line.mrp_join_partner_company_name = company_name.strip()

    def _compute_acc_line_price_subtotal(self):
        for line in self:
            line.acc_line_price_subtotal = '{0:,.0f}'.format(line.price_subtotal) if line.price_subtotal else ''
    
    def _compute_acc_line_price_unit(self):
        for line in self:
            line.acc_line_price_unit = '{0:,.0f}'.format(line.price_unit) if line.price_unit else ''

    def _compute_acc_line_sell_unit_price(self):
        for line in self:
            line.acc_line_sell_unit_price = '{0:,.0f}'.format(line.price_unit - line.price_unit * line.discount / 100 ) 
class MrpProductionExcelReport(models.Model):
    _inherit = "mrp.production"

    sale_order = fields.One2many(
        "sale.order",
        "origin",
        string="Sale order",
        compute="_compute_sale_order",
    )

    order_line = fields.One2many(
        "sale.order.line",
        "order_id",
        string="Sale order line",
        compute="_compute_order_line",
    )

    mrp_note = fields.Char(
        "Mrp note",
        compute="_compute_mrp_note",
    )
    
    lang_code = fields.Char(string="Language Code", compute="_compute_lang_code")
    
    hr_employee_company = fields.Char(compute="_compute_hr_employee")
    hr_employee_department = fields.Char(compute="_compute_hr_employee")
    hr_employee_zip = fields.Char(compute="_compute_hr_employee")
    hr_employee_info = fields.Char(compute="_compute_hr_employee")
    hr_employee_tel = fields.Char(compute="_compute_hr_employee")
    hr_employee_fax = fields.Char(compute="_compute_hr_employee")
    hr_employee_printer = fields.Char(compute="_compute_hr_employee")
    
    mrp_hr_employee = fields.Char(compute="_compute_mrp_hr_employee")  
    mrp_picking_type_warehouse_address = fields.Char(compute="_compute_mrp_picking_type_warehouse_address")
    mrp_picking_type_warehouse_company = fields.Char(compute="_compute_mrp_picking_type_warehouse_address")
    
    mrp_choose_option_find_warehouse_company_name = fields.Char(compute="_compute_mrp_choose_option_find_warehouse")
    mrp_choose_option_find_warehouse_address = fields.Char(compute="_compute_mrp_choose_option_find_warehouse")
    mrp_choose_option_find_warehouse_phone = fields.Char(compute="_compute_mrp_choose_option_find_warehouse")
    mrp_child_mo_desired_delivery_date = fields.Datetime(compute="_compute_mrp_child_mo_desired_delivery_date")
    
    def _compute_mrp_child_mo_desired_delivery_date(self):
        for line in self:
            desired_delivery_date = None
            if line.origin and '/MO/' in line.origin:
                print('line.product_id: ', line.product_id)
                source_mo = self.env["mrp.production"].search([('name', '=', line.origin)], limit=1)
                if source_mo:
                    for move in source_mo.move_raw_ids:
                        if move.product_id == line.product_id and move.forecast_expected_date:
                            desired_delivery_date = move.forecast_expected_date
            
            line.mrp_child_mo_desired_delivery_date = desired_delivery_date
                
    def _compute_mrp_choose_option_find_warehouse(self):
        for line in self:
            company_name = ""
            address = ""
            phone = ""
            
            if line.storehouse_id and line.storehouse_id.partner_id:
                partner = self.env["res.partner"].with_context({'lang':self.lang_code}).search([("id", "=", line.storehouse_id.partner_id.id)], limit=1)
                if partner :
                    if partner.company_type == "company":
                        company_name = partner.name if partner.name else ''
                    else:
                        company_name = partner.last_name if partner.last_name else ''
                        
                    if partner.zip:
                        address += "〒" + partner.zip + " "
                        
                    if line.lang_code == 'ja_JP':
                        if partner.state_id and partner.state_id.name:
                            address += partner.state_id.name + " "
                        if partner.city:
                            address += partner.city + " "
                        if partner.street:
                            address += partner.street + " "
                        if partner.street2:
                            address += partner.street2 
                    else:
                        if partner.street:
                            address += partner.street + " "
                        if partner.street2:
                            address += partner.street2 + " "
                        if partner.city:
                            address += partner.city + " "
                        if partner.state_id and partner.state_id.name:
                            address += partner.state_id.name + " "
                    
                    if partner.phone:
                        phone = partner.phone

            line.mrp_choose_option_find_warehouse_company_name = company_name.strip()
            line.mrp_choose_option_find_warehouse_address = address.strip()
            line.mrp_choose_option_find_warehouse_phone = phone.strip()
                
    def _compute_mrp_picking_type_warehouse_address(self):
        for line in self:
            address = ""
            company_name = ""
            
            picking = line.picking_type_id
            if picking:
                warehouse = picking.warehouse_id
                if warehouse :
                    partner = warehouse.partner_id
                    if partner :
                        if partner.zip:
                            address += "〒" + partner.zip + " "
                            
                        if line.lang_code == 'ja_JP':
                            if partner.state_id and partner.state_id.name:
                                address += partner.state_id.name + " "
                            if partner.city:
                                address += partner.city + " "
                            if partner.street:
                                address += partner.street + " "
                            if partner.street2:
                                address += partner.street2 
                        else:
                            if partner.street:
                                address += partner.street + " "
                            if partner.street2:
                                address += partner.street2 + " "
                            if partner.city:
                                address += partner.city + " "
                            if partner.state_id and partner.state_id.name:
                                address += partner.state_id.name + " "
                                
                        if partner.commercial_company_name:
                            company_name = partner.commercial_company_name
                        elif partner.name:
                            company_name = partner.name
                            
                        if partner.department:
                            company_name += " " + partner.department
                            
                        if partner.user_id and partner.user_id.name :
                            company_name += " " + partner.user_id.name + " ご依頼分"
                        
            line.mrp_picking_type_warehouse_address = address.strip()
            line.mrp_picking_type_warehouse_company = company_name.strip()
            
    def _compute_hr_employee(self):
        for mo in self:
            hr_defaults = {
                'hr_employee_company': "株式会社リッツウェル",
                'hr_employee_department': "大阪オフィス",
                'hr_employee_zip': "〒542-0081",
                'hr_employee_info': "大阪市中央区南船場4-7-6 B1F",
                'hr_employee_tel': "tel.06-4963-8777",
                'hr_employee_fax': "fax.06-4963-8778",
                'hr_employee_printer': mo.mrp_production_so_id and mo.mrp_production_so_id.sale_order_printing_staff or '',
            }
            
            if mo.user_id:
                lang = mo.lang_code
                hr_employee = self.env['hr.employee'].with_context({'lang':lang}).search([('user_id', '=', mo.user_id.id)])
                if hr_employee:
                    for employee in hr_employee:
                        mo.hr_employee_company = employee.company_id and employee.company_id.name or ''
                        
                        if employee.address_id:
                            res_partner = self.env['res.partner'].with_context({'lang':lang}).search([('id', '=', employee.address_id.id)])
                            if res_partner:
                                for res in res_partner:
                                    mo.hr_employee_department = res.site or ''
                                    
                                    mo.hr_employee_zip = (_("〒") + res.zip) if res.zip != False else ''
                                    
                                    if mo.lang_code == 'ja_JP':
                                        mo.hr_employee_info = f"{res.state_id.name or ''} {res.city or ''} {res.street or ''} { res.street2 or ''}".strip()
                                    else:
                                        mo.hr_employee_info = f"{res.street or ''} { res.street2 or ''} {res.city or ''} {res.state_id.name or ''}".strip()
                                    
                                    mo.hr_employee_tel = ("tel." + res.phone) if res.phone != False else ''
                                    mo.hr_employee_fax = ("fax." + res.fax) if res.fax != False else ''
                            else:
                                mo.hr_employee_zip = ''
                                mo.hr_employee_info = ''
                                mo.hr_employee_tel = ''
                                mo.hr_employee_fax = ''
                        else:
                            mo.hr_employee_zip = ''
                            mo.hr_employee_info = ''
                            mo.hr_employee_tel = ''
                            mo.hr_employee_fax = ''
                            
                        if employee.name:
                            mo.hr_employee_printer = "発注者 " +  employee.name
                        else:
                            mo.hr_employee_printer = ""
                else:
                    mo.update(hr_defaults)
            else:
                mo.update(hr_defaults)
        
    def _compute_mrp_hr_employee(self):
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
            record.mrp_hr_employee = hr_employee_detail.rstrip('\n')
    
    def _compute_lang_code(self):
        for l in self:
            l.lang_code = self.env.user.lang or 'en_US'
            
    def _compute_mrp_note(self):
        note = ""
        for line in self:
            if line.remark:
                note += line.remark 
            # if line.production_memo:
            #     note += line.production_memo
            line.mrp_note = note

    def _compute_order_line(self):
        for line in self:
            sale_orders = self.env["sale.order"].search([("name", "=", line.origin)])
            line.order_line = self.env["sale.order.line"].search(
                [("order_id", "in", sale_orders.ids)]
            )

    def _compute_sale_order(self):
        for line in self:
            if line.origin.startswith("S"):# mo mother
                line.sale_order = self.env["sale.order"].search([("name", "=", line.origin)])
            else: # mo child
                mrp =  self.env["mrp.production"].search([("name", "=", line.origin)])
                if mrp:
                    line.sale_order = self.env["sale.order"].search([("name", "=", mrp.origin)])                    
class StockMoveContainerReport(models.Model):
    _inherit = "stock.move.container"

    pallet_count = fields.Char("", compute="_compute_pallet_count")
    note_eng = fields.Char('', compute="_compute_note_eng")

    def _compute_pallet_count(self):
        stock_move_pallet_count = len(
            self.env['stock.move.pallet'].search([('container_id', '=', self.id)]))
        self.pallet_count = str(stock_move_pallet_count) + ' PALLETS'

    def _compute_note_eng(self):
        stock_move_container = self.env['stock.move.container'].with_context(lang='en_US').search([('id','=',self.id)])
        self.note_eng = stock_move_container.note
class StockMovePalletReport(models.Model):
    _inherit = "stock.move.pallet"
    _name = "stock.move.pallet"

    pallet_name_and_product = fields.Char(
        "", compute="_compute_pallet_name_and_product"
    )
    stock_pallet_index = fields.Char("", compute="_compute_stock_pallet_index")
    blank_cell1 = fields.Char("", compute="_compute_blank_cell")
    blank_cell2 = fields.Char("", default="", compute="_compute_blank_cell")
    blank_cell3 = fields.Char("", default="", compute="_compute_blank_cell")
    blank_cell4 = fields.Char("", default="", compute="_compute_blank_cell")
    blank_cell5 = fields.Char("", default="", compute="_compute_blank_cell")
    blank_cell6 = fields.Char("", default="", compute="_compute_blank_cell")

    def _compute_blank_cell(self):
        self.blank_cell1 = ""
        self.blank_cell2 = ""
        self.blank_cell3 = ""
        self.blank_cell4 = ""
        self.blank_cell5 = ""
        self.blank_cell6 = ""

    def _compute_stock_pallet_index(self):
        index = 0
        for line in self:
            index = index + 1
            line.stock_pallet_index = str(index)

    def _compute_pallet_name_and_product(self):
        for record in self:
            pallet_name_and_product = record.name
            stock_move_lines = self.env["stock.move.line"].with_context(lang='en_US').search(
                [("pallet_id", "=", record.id)]
            )
            for line in stock_move_lines:
                product_detail = ""
                product_template_attribute_values = (
                    line.product_id.product_template_attribute_value_ids
                )
                for attr in product_template_attribute_values:
                    product_detail += "\t" + attr.display_name + "\n"
                pallet_name_and_product += (
                    "\n"
                    + "\t"
                    + line.product_id.name
                    + "\n"
                    + product_detail
                    + "\t"
                    + "W"
                    + str(line.product_id.width)
                    + " x"
                    + " D"
                    + str(line.product_id.depth)
                    + " x"
                    + " H"
                    + str(line.product_id.height)
                    + " mm"
                    + "\n"
                )
            record.pallet_name_and_product = pallet_name_and_product
class PurchaseOrderExcelReport(models.Model):
    _inherit = "purchase.order"

    purchase_order_line = fields.One2many(
        "purchase.order.line",
        "order_id",
        string="Sale order line",
        compute="_compute_purchase_order_line",
    )

    purchase_order_company = fields.Char(
        "Mrp product index",
        compute="_compute_purchase_order_company",
    )

    purchase_order_address_zip_city = fields.Char(
        "Mrp product index",
        compute="_compute_purchase_order_address_zip_city",
    )

    purchase_order_current_date = fields.Char(
        compute="_compute_purchase_order_current_date",
        string="Current Date",
    )

    purchase_order_printing_staff = fields.Char(
        compute="_compute_purchase_order_printing_staff",
        string="Printing Staff",
    )

    purchase_order_detail_address_partner = fields.Char(
        compute="_compute_purchase_order_detail_address_partner",
        string="Detail Address Partner",
    )
    
    purchase_order_origin = fields.Char(
        compute="_compute_purchase_order_origin",
        string="purchase order origin",
    )

    purchase_line_date_planned = fields.Char(
        "Date planned",
        compute="_compute_report_date",
    )

    purchase_line_date_order = fields.Char(
        "Date planned",
        compute="_compute_report_date",
    )
    
    purchase_print_staff= fields.Char(
        "purchase print staff",
        compute="_compute_print_staff",
    )  

    lang_code = fields.Char(string="Language Code", compute="_compute_lang_code")
    yearUnit = fields.Char(string="Year", compute="_compute_year_unit")
    monthUnit = fields.Char(string="Month", compute="_compute_month_unit")
    dayUnit = fields.Char(string="Day", compute="_compute_day_unit")
            
    def _compute_purchase_order_origin(self):
        for order in self:
            if order.origin:
                detail = []  
                if ',' in order.origin:
                    origin = order.origin.split(',')
                else:
                    origin = [order.origin]
                        
                for o in origin:
                    if 'MO' in o:
                        mp = self.env['mrp.production'].search([('name', '=', o.strip())])
                        if mp:
                            for l in mp:
                                if l.sale_reference:
                                    detail.append(l.sale_reference)  
                                elif l.origin:
                                    detail.append(l.origin) 
                                else:
                                    detail.append(l.name) 
                    else:
                        detail.append(o.strip())  
                    
                detail_unique = []
                for item in detail:
                    if item not in detail_unique:
                        detail_unique.append(item)
                        
                order.purchase_order_origin = ', '.join(detail_unique)
                
            else :
                order.purchase_order_origin =  ''
    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.user.lang or 'en_US'
            
    def _compute_print_staff(self):
        for line in self:
            printing_staff = ''
            if line.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',line.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
            line.purchase_print_staff = printing_staff  
            
    def _compute_year_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.yearUnit = "-"
            else:
                record.yearUnit = "年"

    def _compute_month_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.monthUnit = "-"
            else:
                record.monthUnit = "月"

    def _compute_day_unit(self):
        for record in self:
            if record.lang_code =="en_US":
                record.dayUnit = ""
            else:
                record.dayUnit = "日"

    def _compute_lang_code(self):
        for l in self:
            l.lang_code = self.env.user.lang or 'en_US'

    def _compute_report_date(self):
        for line in self:
            date_planned=line.date_planned
            date_order=line.date_order
            if date_planned:
                line.purchase_line_date_planned = (
                    str(date_planned.year)
                    + line.yearUnit
                    + str(date_planned.month)
                    + line.monthUnit
                    + str(date_planned.day)
                    + line.dayUnit
                )
            else:
                line.purchase_line_date_planned = ""

            if date_order:
                line.purchase_line_date_order = (
                    str(date_order.year)
                    + line.yearUnit
                    + str(date_order.month)
                    + line.monthUnit
                    + str(date_order.day)
                    + line.dayUnit
                )
            else:
                line.purchase_line_date_order = ""
    
    def _compute_purchase_order_detail_address_partner(self):
        details = ""
        for line in self:
            if line.partner_id.zip:
                details += "〒" + line.partner_id.zip + " "
            if line.partner_id.street:
                details += line.partner_id.street + " "
            if line.partner_id.street2:
                details += line.partner_id.street2 + " "
            if line.partner_id.city:
                details += line.partner_id.city + " "
            if line.partner_id.state_id.name:
                details += line.partner_id.state_id.name + " "
            if line.partner_id.country_id.name:
                details += line.partner_id.country_id.name + " "
            line.purchase_order_detail_address_partner =  details

    def _compute_purchase_order_printing_staff(self):
        for line in self:
            printing_staff = ''
            if line.user_id:
                res_partner= self.env['res.partner'].with_context({'lang':self.env.user.lang}).search([('id','=',line.user_id.id)])
                if res_partner :
                    for res in res_partner:
                        printing_staff = res.name if res.name else ''
            if printing_staff:  
                if line.lang_code == 'en_US':
                    line.purchase_order_printing_staff = "Orderer " + printing_staff
                else:
                    line.purchase_order_printing_staff = "発注者 " + printing_staff
            else:
                line.purchase_order_printing_staff = ""

    def _compute_purchase_order_current_date(self):
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        for record in self:
            if self.env.user.lang == 'ja_JP':
                record.purchase_order_current_date = year + " 年 " + month + " 月 " + day + " 日 "
            else:
                record.purchase_order_current_date = year + " - " + month + " - " + day 

    def _compute_purchase_order_company(self):
        for record in self:
            company = ""
            if record.partner_id:
                if record.lang_code == 'ja_JP':
                    if record.partner_id.commercial_company_name:
                        company = record.partner_id.commercial_company_name + " 御中"
                    elif record.partner_id.name:
                        company = record.partner_id.name + " 御中"
                else:
                    if record.partner_id.commercial_company_name:
                        company = "Dear " + record.partner_id.commercial_company_name
                    elif record.partner_id.name:
                        company = "Dear " + record.partner_id.name
                    
            record.purchase_order_company = company
            
    def _compute_purchase_order_address_zip_city(self):
        for record in self:
            address = ""
            if record.picking_type_id.warehouse_id.partner_id.city:
                address += record.picking_type_id.warehouse_id.partner_id.city +" "
            if record.picking_type_id.warehouse_id.partner_id.state_id.name:
                address += record.picking_type_id.warehouse_id.partner_id.state_id.name +" "
            if record.picking_type_id.warehouse_id.partner_id.zip:
                address += "〒" + record.picking_type_id.warehouse_id.partner_id.zip +" "
            record.purchase_order_address_zip_city =address

    def _compute_purchase_order_line(self):
        for line in self:
            purchase_order = self.env["purchase.order"].search([("id", "=", line.id)])
            line.purchase_order_line = self.env["purchase.order.line"].search(
                [("order_id", "in", purchase_order.ids)]
            )
class PurChaseOrderLineExcelReport(models.Model):
    _inherit = "purchase.order.line"
        
    purchase_order_index = fields.Integer(
        compute="_compute_purchase_order_index",
        string="index",
    )

    purchase_order_product_detail = fields.Char(
        compute="_compute_purchase_order_product_detail",
        string="仕様・詳細",
    )

    purchase_order_text_piece_leg = fields.Char(
        compute="_compute_purchase_order_text_piece_leg",
        string="Text piece leg",
    )

    purchase_order_sell_unit_price = fields.Float(
        compute="_compute_purchase_order_sell_unit_price",
        string="販売単価",
    )

    purchase_order_config_session = fields.Char(
        compute="_compute_purchase_order_config_session",
        string="Config Session",
    )

    purchase_order_prod_detail = fields.Char(
        compute="_compute_purchase_order_prod_detail",
        string="Config Session",
    )
    
    purchase_order_line_product_uom_qty = fields.Char(string="sale order product uom qty" , compute="_compute_purchase_order_line_product_uom_qty")
        
    purchase_order_prod_name = fields.Char(compute = '_compute_purchase_order_prod_name')
    purchase_order_line_size = fields.Char(compute = '_compute_purchase_order_prod_name')

    def _compute_purchase_order_prod_name(self):
        for line in self:
            categ_name = ""
            size = ""
            prod = line.product_id
            if prod:
                prod_tmpl = prod.product_tmpl_id
                if prod_tmpl:
                    if prod_tmpl.config_ok:  
                        if prod_tmpl.categ_id and prod_tmpl.categ_id.name:
                            categ_name = prod_tmpl.categ_id.name
                        elif prod_tmpl.product_no:
                            categ_name = prod_tmpl.product_no
                        elif prod_tmpl.name: 
                            categ_name = prod_tmpl.name   
                    elif line.name:
                        categ_name = line.name
                        
                    if prod_tmpl.width:
                        size += 'W' + str(prod_tmpl.width) + ' '
                    if prod_tmpl.depth:
                        size += '*D' + str(prod_tmpl.depth) + ' '
                    if prod_tmpl.diameter:
                        size += 'Φ' + str(prod_tmpl.diameter) + ' '
                    if prod_tmpl.height:
                        size += '*H' + str(prod_tmpl.height) + ' '
                    if prod_tmpl.sh:
                        size += 'SH' + str(prod_tmpl.sh) + ' '
                    if prod_tmpl.ah:
                        size += 'AH' + str(prod_tmpl.ah)
                    
            line.purchase_order_prod_name = categ_name
            line.purchase_order_line_size = size.strip()
            
    def _compute_purchase_order_line_product_uom_qty(self):
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.purchase_order_line_product_uom_qty = ''
            else:
                float_product_uom_qty = float(line.product_uom_qty)
                integer_part = int(line.product_uom_qty)
                decimal_part = round(float_product_uom_qty - integer_part,2)
                decimal_part_after_dot = int(str(decimal_part).split('.')[1])
                if str(decimal_part).split('.')[1] == "00" or str(decimal_part).split('.')[1] == "0" :
                    line.purchase_order_line_product_uom_qty = integer_part
                else:
                    while decimal_part_after_dot % 10 == 0:
                        decimal_part_after_dot = decimal_part_after_dot / 10
                    line.purchase_order_line_product_uom_qty =  integer_part + float('0.' + str(decimal_part_after_dot))
    
    def _compute_purchase_order_prod_detail(self):
        for line in self:
            product_number_and_size = ""
            categ = ""
            size = ""
            if line.product_id:
                product_tmpl = line.product_id.product_tmpl_id
                if product_tmpl:
                    if product_tmpl.categ_id and product_tmpl.categ_id.name:
                        categ += str(line.product_id.product_tmpl_id.categ_id.name)
                    
                    if product_tmpl.width:
                        size += 'W' + str(product_tmpl.width) + ' '
                    if product_tmpl.depth:
                        size += '*D' + str(product_tmpl.depth) + ' '
                    if product_tmpl.diameter:
                        size += 'Φ' + str(product_tmpl.diameter) + ' '
                    if product_tmpl.height:
                        size += '*H' + str(product_tmpl.height) + ' '
                    if product_tmpl.sh:
                        size += 'SH' + str(product_tmpl.sh) + ' '
                    if product_tmpl.ah:
                        size += 'AH' + str(product_tmpl.ah)
                        
            if categ and size:
                product_number_and_size = categ + "\n" + size
            elif categ:
                product_number_and_size = categ
            elif size:
                product_number_and_size = size
                
            line.purchase_order_prod_detail = product_number_and_size
            
    def _compute_purchase_order_index(self):
        index = 0
        for line in self:
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.purchase_order_index = ''
            else:
                index += 1
                line.purchase_order_index = str(index)
    
    def _compute_purchase_order_product_detail(self):
        for record in self:
            attr = ""
            attributes = record.product_id.product_template_attribute_value_ids
            if attributes:
                for attribute in attributes:
                    attribute_name = self.env['product.attribute'].with_context({'lang':self.env.user.lang}).search([('id','=',attribute.attribute_id.id)]).name
                    attribute_value = self.env['product.attribute.value'].with_context({'lang':self.env.user.lang}).search([('id','=',attribute.product_attribute_value_id.id)]).name
                    attr += (
                        '●' + ' '+
                        attribute_name
                        + ":"
                        + attribute_value
                        + "\n"
                    )
            record.purchase_order_product_detail = attr
            
    def _compute_purchase_order_text_piece_leg(self):
        for line in self:
            if line.display_type == "line_section" or line.display_type == "line_note":
                line.purchase_order_text_piece_leg = ""
            else:
                line.purchase_order_text_piece_leg = "脚"
            
    def _compute_purchase_order_sell_unit_price(self):
        for line in self:
            # if line.discount > 0:
            #     line.purchase_order_sell_unit_price = (
            #         line.price_unit - line.price_unit * line.discount / 100
            #     )
            if line.display_type == "line_section" or line.display_type == "line_note":
                line.purchase_order_sell_unit_price = ""
            else:
                line.purchase_order_sell_unit_price = line.price_unit

    def _compute_purchase_order_config_session(self):
        for line in self:
            config=""
            if line.p_type:
                if line.p_type =="special":
                    config += "別注" +"\n"
                if line.p_type =="custom":
                    config += "特注" +"\n"
            configCus=line.config_session_id.custom_value_ids
            if configCus:
                for cfg in configCus:
                    config += cfg.display_name + ":" + cfg.value + "\n"
            config.rstrip("\n")
            line.purchase_order_config_session=config
            