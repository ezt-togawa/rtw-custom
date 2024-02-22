from odoo import models, fields ,api
from datetime import datetime
import math
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
    sale_order_company_owner = fields.Char(
        compute="_compute_sale_order_company_owner",
        string="Company Name",
    )
    sale_order_total_list_price = fields.Float(
        compute="_compute_sale_order_list_price",
        string="Total List Price",
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
    
    sale_order_hr_employee = fields.Char(
        compute="_compute_sale_order_hr_employee",
        string="Sale order hr employee",
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

    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.context.get('lang') or ''

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
                
    def _compute_sale_order_hr_employee(self):
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
            
            record.sale_order_hr_employee= hr_employee_detail
                
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
            sale_order_company_name = ""
            if line.partner_id.commercial_company_name:
                sale_order_company_name = line.partner_id.commercial_company_name
            else:
                sale_order_company_name = line.partner_id.name
            if line.partner_id.department:
                sale_order_company_name += " " + line.partner_id.department
            if line.partner_id.user_id.name:
                sale_order_company_name += " " + line.partner_id.user_id.name + " ご依頼分"
            line.sale_order_company_name = sale_order_company_name

    def _compute_sale_order_info_cus(self):
        for line in self:
            info_cus = ""
            if line.partner_id.name:
                info_cus = line.partner_id.name
            if line.partner_id.site:
                info_cus = line.partner_id.site
            if line.partner_id.department:
                info_cus += " " + line.partner_id.department
            if line.partner_id.user_id.name:
                info_cus += " " + line.partner_id.user_id.name + " "
            if line.name:
                info_cus += "ご依頼分" + line.name
            line.sale_order_info_cus = info_cus

    def _compute_sale_order_ritzwell_staff(self):
        for line in self:
            if line.user_id.name:
                line.sale_order_ritzwell_staff = line.user_id.name + "  様"
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
            if line.user_id.name:
                line.sale_order_printing_staff = line.user_id.name + (" Seal" if line.lang_code == "en_US" else "  印")
            else:
                line.sale_order_printing_staff=""
                
    def _compute_sale_order_detail_address_partner(self):
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
                record.amount_total if record.amount_total else 0
            )
            record.sale_order_amount_untaxed = record.currency_id.symbol + str(
                record.amount_untaxed if record.amount_untaxed else 0
            )
            record.sale_order_amount_tax = record.currency_id.symbol + str(
                record.amount_tax if record.amount_tax else 0
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
            shipping_date = record.estimated_shipping_date
            date_order = record.date_order
            validity_date = record.validity_date
            shiratani_entry_date = record.shiratani_entry_date
            preferred_delivery_date = record.preferred_delivery_date
            date_deadline = record.date_deadline

            if shipping_date:
                record.sale_order_estimated_shipping_date = (
                    str(shipping_date.year)
                    + record.yearUnit
                    + str(shipping_date.month)
                    + record.monthUnit
                    + str(shipping_date.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_estimated_shipping_date = ""
            if date_order:

                record.sale_order_date_order = (
                    str(date_order.year)
                    + record.yearUnit
                    + str(date_order.month)
                    + record.monthUnit
                    + str(date_order.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_date_order = ""
            if validity_date:
                record.sale_order_validity_date = (
                    str(validity_date.year)
                    + record.yearUnit
                    + str(validity_date.month)
                    + record.monthUnit
                    + str(validity_date.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_validity_date = ""
            if shiratani_entry_date:
                record.sale_order_shiratani_entry_date = (
                    str(shiratani_entry_date.year)
                    + record.yearUnit
                    + str(shiratani_entry_date.month)
                    + record.monthUnit
                    + str(shiratani_entry_date.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_shiratani_entry_date = ""
            if preferred_delivery_date:
                record.sale_order_preferred_delivery_date = (
                    str(preferred_delivery_date.year)
                    + record.yearUnit
                    + str(preferred_delivery_date.month)
                    + record.monthUnit
                    + str(preferred_delivery_date.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_preferred_delivery_date = ""
            if date_deadline:
                record.sale_order_date_deadline = (
                    str(date_deadline.year)
                    + record.yearUnit
                    + str(date_deadline.month)
                    + record.monthUnit
                    + str(date_deadline.day)
                    + record.dayUnit
                )
            else:
                record.sale_order_date_deadline = ""

    def _compute_sale_order_company_owner(self):
        for record in self:
            if record.partner_id.name:
                record.sale_order_company_owner = record.partner_id.name + " 様"
            else:
                record.sale_order_company_owner = ""

    def _compute_sale_order_list_price(self):
        for record in self:
            total_list_price = 0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_list_price += line.price_unit * line.product_uom_qty
            record.sale_order_total_list_price = total_list_price

    def _compute_sale_order_total_discount(self):
        for record in self:
            total_discount = 0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_discount += (
                    line.price_unit - line.price_reduce
                ) * line.product_uom_qty
            record.sale_order_total_discount = "- " + str(total_discount)

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

    sale_order_sell_unit_price = fields.Float(
        compute="_compute_sale_order_sell_unit_price",
        string="販売単価",
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
            product_number_and_size = ""
            if line.product_id.product_tmpl_id.product_no:
                product_number_and_size += (
                    str(line.product_id.product_tmpl_id.product_no) + "\n"
                )

            if line.product_id.product_tmpl_id.width:
                product_number_and_size += (
                    "W" + str(line.product_id.product_tmpl_id.width) + "*"
                )

            if line.product_id.product_tmpl_id.depth:
                product_number_and_size += (
                    "D" + str(line.product_id.product_tmpl_id.depth) + "*"
                )

            if line.product_id.product_tmpl_id.height:
                product_number_and_size += (
                    "H" + str(line.product_id.product_tmpl_id.height) + "*"
                )

            if line.product_id.product_tmpl_id.sh:
                product_number_and_size += (
                    "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
                )

            if line.product_id.product_tmpl_id.ah:
                product_number_and_size += (
                    "AH" + str(line.product_id.product_tmpl_id.ah) + "*"
                )
            line.sale_order_number_and_size = product_number_and_size

    def _compute_sale_order_product_detail(self):
        for line in self:
            attr = ""
            attributes = line.product_id.product_template_attribute_value_ids
            if attributes:
                for attribute in attributes:
                    attr += (
                        attribute.attribute_id.name
                        + ":"
                        + attribute.product_attribute_value_id.name
                        + "\n"
                    )
            line.sale_order_product_detail = attr

    def _compute_sale_order_product_summary(self):
        for line in self:
            attr = ""
            attributes = line.product_id.product_template_attribute_value_ids
            if attributes:
                for attribute in attributes:
                    attr += attribute.attribute_id.name + "\n"
            line.sale_order_product_summary = attr
                    
    @api.onchange('product_uom_qty', 'discount', 'price_unit')
    def _compute_sale_order_sell_unit_price(self):
        for line in self:
            line.sale_order_sell_unit_price = line.price_unit - line.price_unit * line.discount / 100 
            
    def _compute_sale_order_index(self):
        index = 0
        for line in self:
            index = index + 1
            line.sale_order_index = index

    def _compute_sale_order_name(self):
        for line in self:
            if line.display_type == "line_note" or line.display_type == "line_section":
                line.sale_order_name = line.name
            else:
                categ_name=""
                if line.product_id.product_tmpl_id.config_ok :  
                    if line.product_id.product_tmpl_id.categ_id.name:
                        categ_name = line.product_id.product_tmpl_id.categ_id.name
                    elif line.product_id.product_tmpl_id.product_no :
                        categ_name = line.product_id.product_tmpl_id.product_no
                    else: 
                        categ_name = line.product_id.product_tmpl_id.name   
                else:
                    # case product is standard Prod + download payment
                    if line.product_id.product_tmpl_id.seller_ids and line.order_id.partner_id.id:
                        matching_sup = None  
                        for sup in line.product_id.product_tmpl_id.seller_ids:
                            if sup.name.id == line.order_id.partner_id.id:
                                matching_sup = sup 
                                break
                        if matching_sup:
                            categ_name = "[" + matching_sup.product_code + "]" + matching_sup.product_name
                        else:
                            categ_name =  line.product_id.product_tmpl_id.name
                    else:
                        if line.product_id.product_tmpl_id.default_code:
                            categ_name = "[" +line.product_id.product_tmpl_id.default_code +"]" + line.product_id.product_tmpl_id.name
                        else:
                            categ_name =  line.product_id.product_tmpl_id.name
                
                                    
                p_type = ""
                if line.p_type:
                    if line.p_type == "special":
                        p_type = "別注"
                    elif line.p_type == "custom":
                        p_type = "特注"

                size_detail = ""
                if line.product_id.product_tmpl_id.width:
                    size_detail += "W" + str(line.product_id.product_tmpl_id.width) + "*"
                if line.product_id.product_tmpl_id.depth:
                    size_detail += "D" + str(line.product_id.product_tmpl_id.depth) + "*"
                if line.product_id.product_tmpl_id.height:
                    size_detail += "H" + str(line.product_id.product_tmpl_id.height) + "*"
                if line.product_id.product_tmpl_id.sh:
                    size_detail += "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
                if line.product_id.product_tmpl_id.ah:
                    size_detail += "AH" + str(line.product_id.product_tmpl_id.ah)

                prod=""
                if categ_name != "" :
                    if p_type !="":
                        prod+= categ_name+ "\n" +p_type
                        if size_detail != "" :
                            prod+=  "\n" + size_detail
                    else:
                        prod+= categ_name
                        if size_detail != "" :
                            prod+= "\n" +size_detail
                else:
                    if p_type !="":
                        prod+= p_type
                        if size_detail != "" :
                            prod+=  "\n" + size_detail
                    else:
                        if size_detail != "" :
                            prod+= "\n" +size_detail
                            
                line.sale_order_name = prod
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
            order.lang_code = self.env.context.get('lang') or ''

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
            sp.lang_code = self.env.context.get('lang') or ''
    
    def _compute_stock_move(self):
        for line in self:
            prod=self.env["stock.move"].search(
                [("picking_id", "=", line.id)]
            )
            if prod :
                line.stock_move=prod

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

            if record.scheduled_date:
                record.stock_picking_scheduled_date = (
                    str(record.scheduled_date.year)
                    + record.yearUnit
                    + str(record.scheduled_date.month)
                    + record.monthUnit
                    + str(record.scheduled_date.day)
                    + record.dayUnit
                )
            else:
                record.stock_picking_scheduled_date = ""

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
            if record.sale_id.partner_id.street:
                partner_address += record.sale_id.partner_id.street + " "
            if record.sale_id.partner_id.street2:
                partner_address += record.sale_id.partner_id.street2 + " "
            if record.sale_id.partner_id.city:
                partner_address += record.sale_id.partner_id.city + " "
            if record.sale_id.partner_id.state_id.name:
                partner_address += record.sale_id.partner_id.state_id.name + " "
            if record.sale_id.partner_id.country_id.name:
                partner_address += record.sale_id.partner_id.country_id.name
            record.stock_picking_partner_address = "〒" + partner_address

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
                if record.sale_id.sipping_to == "inst":
                    sipping_to = "搬入設置まで"
                if record.sale_id.sipping_to == "inst_depo":
                    sipping_to = "搬入設置（デポ入）"
                if record.sale_id.sipping_to == "direct":
                    sipping_to = "直送"
                if record.sale_id.sipping_to == 'container':
                    record.sipping_to = 'オランダコンテナ出荷'
                if record.sale_id.sipping_to == 'pick_up':
                    record.sipping_to = '引取'
                if record.sale_id.sipping_to == 'bring_in':
                    record.sipping_to = '持込'
            record.stock_picking_sipping_to = sipping_to
            

            witness_name_phone = ""
            if record.sale_id.witness:
                witness_name_phone += record.sale_id.witness
            if record.sale_id.witness_phone:
                witness_name_phone += "-" + record.sale_id.witness_phone
            record.stock_picking_witness_name_phone = witness_name_phone

            printing_staff = ""
            if record.sale_id.user_id.name:
                printing_staff += record.sale_id.user_id.name + (" Seal" if record.lang_code == "en_US" else "  印")
            record.stock_picking_printing_staff = printing_staff

            day = str(datetime.now().day)
            month = str(datetime.now().month)
            year = str(datetime.now().year)
            record.stock_picking_current_date = (
                year + " " + record.yearUnit + " " + month + " " + record.monthUnit +" " + day + " "+ record.dayUnit
            )

            estimated_shipping_date = record.sale_id.estimated_shipping_date
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

            if record.sale_id.user_id.name:
                record.stock_printing_staff = record.sale_id.user_id.name +  (" Seal" if record.lang_code == "en_US" else "  印")
class StockMoveExcelReport(models.Model):
    _inherit = "stock.move"
    calculate_packages = fields.Integer('Packages' , compute="_compute_calculate_packages")

    calculate_product_pack = fields.Char(
        string="Calculate product pack",
        compute="_compute_calculate_product_pack",
        default=""
    )

    def _compute_calculate_product_pack(self):
        for line in self:
            if line.sale_line_id.pack_parent_line_id:
                line.calculate_product_pack = ' / ' + line.sale_line_id.pack_parent_line_id.product_id.name
            else:
                line.calculate_product_pack = ''

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

    packages_number = fields.Char(
        "Number packages",
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
            line.product_attribute = ""
            index = index + 1
            line.stock_index = index

            categ_name=""
            p_type = ""
            
            if line.product_id.product_tmpl_id.config_ok :  
                if line.product_id.product_tmpl_id.categ_id.name:
                    categ_name = line.product_id.product_tmpl_id.categ_id.name
                elif line.product_id.product_tmpl_id.product_no :
                    categ_name = line.product_id.product_tmpl_id.product_no
                else: 
                    categ_name = line.product_id.product_tmpl_id.name
            else:
                if line.product_id.product_tmpl_id.seller_ids and  line.picking_id.partner_id.id:
                    matching_sup = None  

                    for sup in line.product_id.product_tmpl_id.seller_ids:
                        if sup.name.id == line.picking_id.partner_id.id:
                            matching_sup = sup 
                            break
                    if matching_sup:
                        categ_name = "[" + matching_sup.product_code + "]" + matching_sup.product_name
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
                        
            if line.p_type:
                if line.p_type == "special":
                    p_type = "別注"
                elif line.p_type == "custom":
                    p_type = "特注"
            
            if categ_name != "":
                if p_type != "":
                    line.product_name = categ_name + "\n" + p_type
                else:
                    line.product_name = categ_name
            else:
                if p_type != "":
                    line.product_name = p_type
                else:
                    line.product_name = ""

            size_detail = ""
            product_pack_ids = line.product_id.product_tmpl_id.mapped('pack_line_ids')
            if line.product_id.product_tmpl_id.product_no:
                size_detail += str(line.product_id.product_tmpl_id.product_no)
                if product_pack_ids:
                    size_detail += ' / '
                    product_pack_names = []
                    for pack in product_pack_ids:
                        product_pack_names.append(pack.product_id.name)
                    size_detail += ', '.join(product_pack_names)
            else:
                if product_pack_ids:
                    product_pack_names = []
                    for pack in product_pack_ids:
                        product_pack_names.append(pack.product_id.name)
                    size_detail += ', '.join(product_pack_names)
            size_detail + '\n'

            other_size=""
            if line.product_id.product_tmpl_id.width:
                other_size += "W" + str(line.product_id.product_tmpl_id.width) + "*"
            if line.product_id.product_tmpl_id.depth:
                other_size += "D" + str(line.product_id.product_tmpl_id.depth) + "*"
            if line.product_id.product_tmpl_id.height:
                other_size += "H" + str(line.product_id.product_tmpl_id.height) + "*"
            if line.product_id.product_tmpl_id.sh:
                other_size += "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
            if line.product_id.product_tmpl_id.ah:
                other_size += "AH" + str(line.product_id.product_tmpl_id.ah)
            
            if other_size != "":
                line.product_number_and_size = size_detail + '\n' + other_size
            else:
                line.product_number_and_size = size_detail


            for attribute_value in line.product_id.product_template_attribute_value_ids:
                attribute_name = attribute_value.attribute_id.name
                attribute_value_name = attribute_value.product_attribute_value_id.name

                if attribute_name and attribute_value_name:
                    line.product_attribute += (
                        f"{attribute_name}:{attribute_value_name}\n"
                    )

            if line.product_id.two_legs_scale:
                line.packages_number = math.ceil(
                    line.product_uom_qty / line.product_id.two_legs_scale
                )
            else:
                line.packages_number = line.product_uom_qty

            line.action_packages = "有"
            line.action_assemble = "無"
            line.stock_sai = line.product_id.product_tmpl_id.sai
            line.stock_warehouse = line.warehouse_id.name
            line.stock_shiratani_date = line.sale_line_id.shiratani_date
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
    
    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.context.get('lang') or ''

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
            l.lang_code = self.env.context.get('lang') or ''
            
    def _compute_acc_move_print_staff(self):
        for l in self:
            if l.user_id.name:
                l.acc_move_print_staff = l.user_id.name +  (" Seal" if l.lang_code == "en_US" else "  印")
            else:
                l.acc_move_print_staff = ""
                
    def _compute_acc_move_invoice_name(self):
        for line in self:
            if line.state == "draft":
                if line.name =='/':
                    line.acc_move_invoice_name= "Draft Invoice"
                else:
                    line.acc_move_invoice_name= "Draft Invoice " + line.name
            if line.state == "posted":
                line.acc_move_invoice_name= "Invoice " + line.name
    
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

    acc_line_discount = fields.Char(
        compute="_compute_acc_line_discount",
        string="discount",
    )

    acc_line_sell_unit_price = fields.Float(
        compute="_compute_acc_line_sell_unit_price",
        string="sell unit price",
    )
    
    acc_line_name = fields.Char(
        compute="_compute_acc_line_name",
        string="acc line name",
    )

    def _compute_acc_line_name(self):
        for line in self:
            name = ""
            if line.display_type =='line_note' or line.display_type =='line_section':
                line.acc_line_name = line.name
                return
            if line.product_id: 
                # case product is download payment 
                # if line.product_id.product_tmpl_id.type == 'service':  
                #     name = line.product_id.product_tmpl_id.name
                # else:
                # case product is configurable Products
                if line.product_id.product_tmpl_id.config_ok :  
                    if line.product_id.product_tmpl_id.categ_id.name:
                        name = line.product_id.product_tmpl_id.categ_id.name
                    elif line.product_id.product_tmpl_id.product_no :
                        name = line.product_id.product_tmpl_id.product_no
                    else: 
                        name = line.product_id.product_tmpl_id.name   
                else:
                    # case product is standard Prod + download payment
                    if line.product_id.product_tmpl_id.seller_ids and line.move_id.partner_id.id:
                        matching_sup = None  
                        for sup in line.product_id.product_tmpl_id.seller_ids:
                            if sup.name.id == line.move_id.partner_id.id:
                                matching_sup = sup 
                                break
                        if matching_sup:
                            name = "[" + matching_sup.product_code + "]" + matching_sup.product_name
                        else:
                            name =  line.name
                    else:
                        name =  line.name
                
            line.acc_line_name = name
            
    def _compute_acc_line_index(self):
        index = 0
        for line in self:
            index = index + 1
            line.acc_line_index = index

    def _compute_acc_line_number_and_size(self):
        for line in self:
            product_number_and_size = ""
            if line.product_id.product_tmpl_id.product_no:
                product_number_and_size += (
                    str(line.product_id.product_tmpl_id.product_no) + "\n"
                )

            if line.product_id.product_tmpl_id.width:
                product_number_and_size += (
                    "W" + str(line.product_id.product_tmpl_id.width) + "*"
                )

            if line.product_id.product_tmpl_id.depth:
                product_number_and_size += (
                    "D" + str(line.product_id.product_tmpl_id.depth) + "*"
                )

            if line.product_id.product_tmpl_id.height:
                product_number_and_size += (
                    "H" + str(line.product_id.product_tmpl_id.height) + "*"
                )

            if line.product_id.product_tmpl_id.sh:
                product_number_and_size += (
                    "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
                )

            if line.product_id.product_tmpl_id.ah:
                product_number_and_size += (
                    "AH" + str(line.product_id.product_tmpl_id.ah) + "*"
                )
            line.acc_line_number_and_size = product_number_and_size

    def _compute_acc_line_product_detail(self):
        for line in self:
            product_detail = ""
            product_template_attribute_values = (
                line.product_id.product_template_attribute_value_ids
            )

            for attr in product_template_attribute_values:
                product_detail += attr.display_name + "\n"
            line.acc_line_product_detail = product_detail
    
    def _compute_acc_line_discount(self):
        for line in self:
            if  line.discount != 0.00 or line.discount != 0.0 or line.discount != 0 :
                line.acc_line_discount = '{0:,.1f}'.format(100-line.discount)
            else:
                line.acc_line_discount = ""

    def _compute_acc_line_sell_unit_price(self):
        for line in self:
            if line.discount > 0:
                line.acc_line_sell_unit_price = (
                    line.price_unit - line.price_unit * line.discount / 100
                )
            else:
                line.acc_line_sell_unit_price = line.price_unit
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

    def _compute_lang_code(self):
        for l in self:
            l.lang_code = self.env.context.get('lang') or ''
            


    def _compute_mrp_note(self):
        note = ""
        for line in self:
            if line.remark:
                note += line.remark + "\n"
            if line.production_memo:
                note += line.production_memo
            line.mrp_note = note

    def _compute_order_line(self):
        for line in self:
            sale_orders = self.env["sale.order"].search([("name", "=", line.origin)])
            line.order_line = self.env["sale.order.line"].search(
                [("order_id", "in", sale_orders.ids)]
            )

    def _compute_sale_order(self):
        for line in self:
            line.sale_order = self.env["sale.order"].search(
                [("name", "=", line.sale_reference)]
            )
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
    
    def _compute_lang_code(self):
        for order in self:
            order.lang_code = self.env.context.get('lang') or ''
            
    def _compute_print_staff(self):
        for l in self:
            if l.user_id.name :
                l.purchase_print_staff = l.user_id.name +  (" Seal" if l.lang_code == "en_US" else "  印")
            else:
                l.purchase_print_staff =""
                
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
            l.lang_code = self.env.context.get('lang') or ''

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
            if line.user_id.name:
                line.purchase_order_printing_staff = line.user_id.name +  (" Seal" if line.lang_code == "en_US" else "  ")
            else:
                line.purchase_order_printing_staff = ""

    def _compute_purchase_order_current_date(self):
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        for record in self:
            record.purchase_order_current_date = year + " 年 " + month + " 月 " + day + " 日 "

    def _compute_purchase_order_company(self):
        for record in self:
            if record.partner_id.commercial_company_name:
                record.purchase_order_company = (
                    "株式会社 " + record.partner_id.commercial_company_name + " 御中"
                )
            else:
                record.purchase_order_company = (
                    "株式会社 " + record.partner_id.name + " 御中"
                )

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
                
    def _compute_purchase_order_line_product_uom_qty(self):
        for line in self:
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
            categ=""
            if line.product_id.product_tmpl_id.categ_id.name:
                categ += (
                    str(line.product_id.product_tmpl_id.categ_id.name) 
                )
        
            detail=""
            if line.product_id.product_tmpl_id.width:
                detail += (
                    "W" + str(line.product_id.product_tmpl_id.width) + "*"
                )

            if line.product_id.product_tmpl_id.depth:
                detail += (
                    "D" + str(line.product_id.product_tmpl_id.depth) + "*"
                )

            if line.product_id.product_tmpl_id.height:
                detail += (
                    "H" + str(line.product_id.product_tmpl_id.height) + "*"
                )

            if line.product_id.product_tmpl_id.sh:
                detail += (
                    "SH" + str(line.product_id.product_tmpl_id.sh) + "*"
                )

            if line.product_id.product_tmpl_id.ah:
                detail += (
                    "AH" + str(line.product_id.product_tmpl_id.ah) + "*"
                )

            if detail != "":
                product_number_and_size = categ + "\n" + detail
            else:
                product_number_and_size = categ
            
            line.purchase_order_prod_detail = product_number_and_size
            
            
    def _compute_purchase_order_index(self):
        index = 0
        for line in self:
            index = index + 1
            line.purchase_order_index = index
    
    def _compute_purchase_order_product_detail(self):
        for line in self:
            attr = ""
            attributes = line.product_id.product_template_attribute_value_ids
            if attributes:
                for attribute in attributes:
                    attr += (
                        attribute.attribute_id.name
                        + ":"
                        + attribute.product_attribute_value_id.name
                        + "\n"
                    )
            line.purchase_order_product_detail = attr

    def _compute_purchase_order_text_piece_leg(self):
        for line in self:
            line.purchase_order_text_piece_leg = "脚"

    def _compute_purchase_order_sell_unit_price(self):
        for line in self:
            # if line.discount > 0:
            #     line.purchase_order_sell_unit_price = (
            #         line.price_unit - line.price_unit * line.discount / 100
            #     )
            # else:
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
            