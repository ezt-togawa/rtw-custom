from odoo import models, fields
from datetime import datetime 

import math

from PIL import Image
import io
import base64

from io import BytesIO
from PIL import Image as PILImage

import xlsxwriter


# class rtw_excel_report(models.Model):
#     _name = 'rtw_excel_report.rtw_excel_report'
#     _description = 'rtw_excel_report.rtw_excel_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

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
    sale_order_company_name = fields.Char(
        compute="_compute_sale_order_company_name",
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
        compute="_compute_sale_order_preferred_delivery_date",
        string="Preferred Delivery Date",
    )
    sale_order_send_to_company = fields.Char(
        compute="_compute_sale_order_send_to_company",
        string="Send to company",
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
        compute='_compute_sale_order_date_planned',
        string='Order Date Planned',
    )

    sale_order_shiratani_entry_date = fields.Char(
        compute='_compute_sale_order_format_date',
        string='Shiratani Entry Date',
    )

    def _compute_sale_order_date_planned(self):
        for line in self:
            order_lines = self.env["sale.order.line"].search(
                [("order_id", "=", line.id)]
            )
            if order_lines:
                max_date_planned = max(order_lines.mapped('date_planned'))
                if max_date_planned:
                    date_planned=(
                            str(max_date_planned.year)
                            + "年"
                            + str(max_date_planned.month)
                            + "月"
                            + str(max_date_planned.day)
                            + "日"
                        )
                    line.sale_order_date_planned =date_planned
                else:
                    line.sale_order_date_planned =""

            
                
    def _compute_sale_order_detail_customer_info(self):
        info = ""
        for line in self:
            if line.company_id.partner_id.name:
                info += line.company_id.partner_id.name + "-"
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
                line.sale_order_printing_staff = line.user_id.name + "  印"

    def _compute_sale_order_detail_address_partner(self):
        details = ""
        for line in self:
            if line.partner_id.zip:
                details += line.partner_id.zip + " "
            if line.partner_id.street:
                details += line.partner_id.street + " "
            if line.partner_id.street2:
                details += line.partner_id.street2 + " "
            if line.partner_id.city:
                details += line.partner_id.city + " "
            if line.partner_id.state_id.name:
                details += line.partner_id.state_id.name
            line.sale_order_detail_address_partner = "〒" + details

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
            record.sale_order_current_date = year + " 年 " + month + " 月 " + day + " 日 "

    def _compute_sale_order_format_date(self):
        for record in self:
            shipping_date = record.estimated_shipping_date
            date_order = record.date_order
            validity_date = record.validity_date
            shiratani_entry_date = record.shiratani_entry_date
            if shipping_date:
                record.sale_order_estimated_shipping_date = (
                    str(shipping_date.year)
                    + "年"
                    + str(shipping_date.month)
                    + "月"
                    + str(shipping_date.day)
                    + "日"
                )
            else:
                record.sale_order_estimated_shipping_date = ""
            if date_order:
                record.sale_order_date_order = (
                    str(date_order.year)
                    + "年"
                    + str(date_order.month)
                    + "月"
                    + str(date_order.day)
                    + "日"
                )
            else:
                record.sale_order_date_order = ""
            if validity_date:
                record.sale_order_validity_date = (
                    str(validity_date.year)
                    + "年"
                    + str(validity_date.month)
                    + "月"
                    + str(validity_date.day)
                    + "日"
                )
            else:
                record.sale_order_validity_date = ""
            if shiratani_entry_date:
                record.sale_order_shiratani_entry_date = (
                    str(shiratani_entry_date.year)
                    + "年"
                    + str(shiratani_entry_date.month)
                    + "月"
                    + str(shiratani_entry_date.day)
                    + "日"
                )
            else:
                record.sale_order_shiratani_entry_date= ""

    def _compute_sale_order_company_name(self):
        for record in self:
            if record.partner_id.name:
                record.sale_order_company_name = record.partner_id.name + " 様"
            else:
                record.sale_order_company_name = ""

    def _compute_sale_order_list_price(self):
        for record in self:
            total_list_price = 0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_list_price += line.price_unit * line.product_uom_qty
            record.sale_order_total_list_price = total_list_price

        # total_subprice + total_discount

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

    def _compute_sale_order_preferred_delivery_date(self):
        for record in self:
            preferred_delivery_date = record.preferred_delivery_date
            if preferred_delivery_date:
                record.sale_order_preferred_delivery_date = (
                    str(preferred_delivery_date.year)
                    + "年"
                    + str(preferred_delivery_date.month)
                    + "月"
                    + str(preferred_delivery_date.day)
                    + "日"
                )
            else:
                record.sale_order_preferred_delivery_date = ""

    def _compute_sale_order_send_to_company(self):
        for record in self:
            if record.partner_id:
                record.sale_order_send_to_company = (
                    "株式会社 " + record.partner_id.name + " 御中"
                )

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

    sale_order_img_product = fields.Char(
        compute="_compute_sale_order_img_product",
        string="Img product",
    )
    
    sale_order_date_order = fields.Char(
        compute="_compute_sale_order_date_order",
        string="Order date",
    )

    sale_order_voucher_class = fields.Char(
        compute="_compute_sale_order_voucher_class",
        string="Voucher Class",
    )

    def _compute_sale_order_voucher_class(self):
        for line in self:
            line.sale_order_voucher_class = "受注引当"

    def _compute_sale_order_date_order(self):
        for line in self:
            if line.order_id.date_order:
                datetime_str = str(line.order_id.date_order)
                if "." in datetime_str:  # 2023-06-12 10:14:34.315388
                    line.sale_order_date_order = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
                else:  # 2023-06-12 10:14:34
                    line.sale_order_date_order =  datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            else:
                line.sale_order_date_order = ""

    def get_image_url(self, image_path,id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        image_url = f"{base_url}/web/image?model={self._name}&field=image_256&id={id}&filename={image_path}"
        return image_url
    
    def _compute_sale_order_img_product(self):
        for line in self:
            if line.product_id:
                self.generate_xlsx_report(
                    "C:\\Users\\ADMIN\\Desktop\\odoo\\rtw-custom\\rtw_excel_report\\report_product_specifications\\product_specifications.xlsm",
                    "test",
                    line
                )
            # # Create a workbook and a worksheet
            #     workbook = xlsxwriter.Workbook("C:\\Users\\ADMIN\\Desktop\\odoo\\rtw-custom\\rtw_excel_report\\report_product_specifications\\product_specifications.xlsm")
            #     sheet_main = workbook.add_worksheet("test")

            #     # image_path = 'C:\\Users\\ADMIN\\Desktop\\Rar--odoo\\6.png'
            #     # img = PILImage.open(image_path)

            #     # # Convert the image to RGB mode
            #     # img = img.convert('RGB')

            #     # img = img.resize((100, 100))
            #     img_io = BytesIO()  # Create a BytesIO object

            #     image_path = f'C:\\Users\\ADMIN\\Desktop\\Rar--odoo\\{line.product_id}.png'
            #     image_data = base64.b64decode(line.product_id.image_256)
            #     image = Image.open(io.BytesIO(image_data))
            #     image = image.convert('RGB')
            #     image = image.resize((100, 100))
            #     image.save(img_io, 'JPEG')  # Save image data to BytesIO

            #     img_io.seek(0)  # Reset the seek position to the beginning

            #     # Insert the image into the worksheet and get the image URL
            #     image_url = sheet_main.insert_image(
            #         'C7',
            #         line.product_id.name,
            #         {'image_data': img_io.getvalue()}  # Use getvalue() to get data from BytesIO
            #     )

            #     # Update the sale_order_img_product field with the image URL
            #     line.sale_order_img_product = image_url

            #     # Close and save the workbook
            #     workbook.close()
        
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
            if line.product_id.product_no:
                product_number_and_size += str(line.product_id.product_no) + "\n"
            if line.product_id.width:
                product_number_and_size += "W" + str(line.product_id.width) + " "
            if line.product_id.depth:
                product_number_and_size += "D" + str(line.product_id.depth) + " "
            if line.product_id.height:
                product_number_and_size += "H" + str(line.product_id.height) + " "
            if line.product_id.ah:
                product_number_and_size += "AH" + str(line.product_id.ah) + " "
            line.sale_order_number_and_size = product_number_and_size

    def _compute_sale_order_product_detail(self):
        for line in self:
            product_detail = ""
            product_config_sessions = line.config_session_id.custom_value_ids
            product_template_attribute_values = (
                line.product_id.product_template_attribute_value_ids
            )
            for attr in product_config_sessions:
                product_detail += attr.display_name + ":" + attr.value + "\n"
            for attr in product_template_attribute_values:
                product_detail += attr.display_name + "\n"
            if line.product_id.width > 0:
                product_detail += line.product_id.width + "\n"
            if line.product_id.depth > 0:
                product_detail += line.product_id.depth + "\n"
            if line.product_id.height > 0:
                product_detail += line.product_id.height + "\n"
            if line.product_id.sh > 0:
                product_detail += line.product_id.sh + "\n"
            if line.product_id.ah > 0:
                product_detail += line.product_id.ah + "\n"
            line.sale_order_product_detail = product_detail

    def _compute_sale_order_product_summary(self):
        for line in self:
            product_detail = ""
            product_config_sessions = line.config_session_id.custom_value_ids
            product_template_attribute_values = (
                line.product_id.product_template_attribute_value_ids
            )
            # for attr in product_config_sessions:
            #     product_detail += attr.display_name + '\n'
            for attr in product_template_attribute_values:
                product_detail += attr.attribute_id.name + "\n"
            line.sale_order_product_summary = product_detail

    def _compute_sale_order_sell_unit_price(self):
        for line in self:
            if line.discount > 0:
                line.sale_order_sell_unit_price=line.price_unit - line.price_unit * line.discount/100   
            else:
                line.sale_order_sell_unit_price=line.price_unit
                
    def _compute_sale_order_index(self):
        index = 0
        for line in self:
            index = index + 1
            line.sale_order_index = index

    def _compute_sale_order_name(self):
        for line in self:
            p_type = ""
            if line.p_type:
                if line.p_type == "special":
                    p_type = "別注"
                elif line.p_type == "custom":
                    p_type = "特注"
            line.sale_order_name = line.name + "\n" + p_type

    sale_order_img_product = fields.Char(
        compute="_compute_sale_order_img_product",
        string="Text piece leg",
    )
    
    def _compute_sale_order_img_product(self):
        for line in self:
            if line.product_id:
                self.generate_xlsx_report(
                    "C:\\Users\\ADMIN\\Desktop\\odoo\\rtw-custom\\rtw_excel_report\\report_product_specifications\\product_specifications.xlsm",
                    "test",
                    line
                )    

    def generate_xlsx_report(self,file_path,name_sheet,line):
        # text_file_path = get_module_resource('rtw_stock_report_xlsx', 'static', 'seal_template.xlsx')
        # print(text_file_path)
        workbook = xlsxwriter.Workbook(file_path)
        sheet_main = workbook.add_worksheet(name_sheet)
        sheet = workbook.add_worksheet("data")
        bold = workbook.add_format({'bold': True})
        merge_format = workbook.add_format({'align': 'center'})
        page_count = 1
        r = 0
        c = 0
        r = math.ceil(len(line)+12/2)
        print(r)
        for count in range(r):
                sheet_main.merge_range(count * 7 + 0, 0, count * 7 + 2, 5, "=data!A" + str(count * 2 + 1), merge_format)
                sheet_main.merge_range(count * 7 + 0, 7, count * 7 + 2, 12, "=data!A" + str(count * 2 + 2), merge_format)
                # ... thêm các dòng lệnh merge_range khác ...

                # Ghi dữ liệu vào các ô tương ứng
                x = ",".join(str(v.name) for v in line.product_id)
                sheet.write(count, 0, line.product_id.name, bold)
                sheet.write(count, 1, x, bold)
                sheet.write(count, 2, line.product_id.name, bold)
                sheet.write(count, 3, line.product_id.name, bold)

                if (count + 1) % 2 == 0:
                    pos = 7
                else:
                    pos = 0

                # Tạo đường dẫn và xử lý ảnh ở đây
                image_path = f'C:\\Users\\ADMIN\\Desktop\\Rar--odoo\\{line.product_id}.png'
                image_data = base64.b64decode(line.product_id.image_256)
                image = Image.open(io.BytesIO(image_data))
                image = image.convert('RGB')
                image = image.resize((200, 200))
                img_io = BytesIO()
                image.save(img_io, 'JPEG')
                img_io.seek(0)

                # Insert the image into the worksheet and get the image URL
                sheet_main.insert_image(
                    count, 0,
                    line.product_id.name,
                    {'image_data': img_io}
                )

        workbook.close()

class ProductTemplateExcelReport(models.Model):
    _inherit = "product.template"

    purchase_order_lines = fields.One2many(
        "purchase.order.line",
        "product_id",
        string="Purchase order line",
        copy=True,
        auto_join=True,
        compute="_compute_purchase_order_lines",
    )

    sale_order_line = fields.One2many(
        "sale.order.line",
        "product_id",
        string="Sale order line",
        copy=True,
        auto_join=True,
        compute="_compute_sale_order_line",
    )

    current_date = fields.Date(
        "current date",
        compute="_compute_current_date",
    )

    product_name = fields.Char(
        "Product name",
        compute="_compute_product_name",
    )

    stock_quant_on_hand = fields.Char(
        "Quantity on hand",
        compute="_compute_stock_quant_on_hand",
    )

    def _compute_stock_quant_on_hand(self):
        for record in self:
            prod=self.env["product.product"].search(
                    [("product_tmpl_id", "=", record.id)]
                )
            if prod:
                prod_qty=self.env["stock.quant"].search(
                    [("product_id", "=", prod.id)]
                )
                if prod_qty:
                    for p in prod_qty:
                        if p.quantity > 0:
                            record.stock_quant_on_hand=p.quantity

        
    def _compute_product_name(self):
        for record in self:
            record.product_name=record.name
            
    def _compute_current_date(self):
        for record in self:
            record.current_date=fields.Date.today()

    def _compute_purchase_order_lines(self):
        for record in self:
            record.purchase_order_lines = self.env["purchase.order.line"].search(
                [("product_id.product_tmpl_id", "=", record.id)]
            )

    def _compute_sale_order_line(self):
        for record in self:
            record.sale_order_line = self.env["sale.order.line"].search(
                    [("product_id.product_tmpl_id", "=", record.id)]
                )
            
            # if order_lines :
            #     for ol in order_lines:
            #         stock_move = self.env["stock.move"].search(
            #                 [("product_id", "=", ol.product_id.id)]
            #             )
            #         print('stock_move11111',stock_move)
            
class PurChaseOrderLineExcelReport(models.Model):      
    _inherit = "purchase.order.line"

    purchase_line_date_planned= fields.Char(
        "Date planned",
        compute="_compute_report_stock_status_list",
    )

    def _compute_report_stock_status_list(self):
        for line in self:
            if line.date_planned:
                datetime_str = str(line.date_planned)
                if "." in datetime_str:  # 2023-06-12 10:14:34.315388
                    line.purchase_line_date_planned = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
                else:  # 2023-06-12 10:14:34
                    line.purchase_line_date_planned =  datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            else:
                line.purchase_line_date_planned = ""

class StockPickingExcelReport(models.Model):
    _inherit="stock.picking"

    stock_move = fields.One2many(
        "stock.move",
        "picking_id",
        string="Stock move line",
        copy=True,
        auto_join=True,
        compute="_compute_stock_move",
    )

    stock_move_line = fields.One2many(
        "stock.move.line",
        "picking_id",
        string="Stock move line",
        copy=True,
        auto_join=True,
        compute="_compute_stock_move_line",
    )

    stock_picking_company_name= fields.Char(
        "Company name",
        compute="_compute_to_sale_order",
    )

    stock_picking_shiratani_entry_date= fields.Char(
        "Shiratani entry date",
        compute="_compute_to_sale_order",
    )

    stock_picking_scheduled_date= fields.Char(
        "Scheduled date",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_info= fields.Char(
        "Partner info",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_address= fields.Char(
        "Partner address",
        compute="_compute_to_sale_order",
    )

    stock_picking_partner_tel_phone= fields.Char(
        "Partner tel phone",
        compute="_compute_to_sale_order",
    )

    stock_picking_witness_name_phone= fields.Char(
        "Staff phone",
        compute="_compute_to_sale_order",
    )

    stock_picking_printing_staff= fields.Char(
        "Printing staff",
        compute="_compute_to_sale_order",
    )

    stock_picking_current_date= fields.Char(
        "Current date",
        compute="_compute_to_sale_order",
    )

    stock_estimated_shipping_date= fields.Char(
        "Estimated shipping date",
        compute="_compute_to_sale_order",
    )

    stock_scheduled_date= fields.Char(
        "Scheduled date",
        compute="_compute_to_sale_order",
    )

    stock_partner_address= fields.Char(
        "Partner address",
        compute="_compute_to_sale_order",
    )

    stock_printing_staff= fields.Char(
        "Printing staff",
        compute="_compute_to_sale_order",
    )

    stock_shiratani_date= fields.Char(
        "Shiratani date",
        compute="_compute_to_sale_order",
    )

    stock_picking_p_qty= fields.Char(
        "Picking product qty",
        compute="_compute_stock_move",
    )

    stock_picking_p_summary= fields.Char(
        "Picking product summary",
        compute="_compute_p_summary",
    )

    def _compute_p_summary(self):
        prod_summary=""
        for line in self:
            prod = self.env["product.product"].search(
                        [("id", "=", line.product_id.id)]
                    )
            attribute = prod.product_template_attribute_value_ids
            if attribute:
                for attr in attribute:
                    prod_summary += attr.attribute_id.name + ":" + attr.product_attribute_value_id.name + "\n"
            line.stock_picking_p_summary=prod_summary
            
    def _compute_stock_move(self):
        for line in self:
            prod=self.env["stock.move"].search(
                [("picking_id", "=", line.id)]
            )
            if prod :
                line.stock_picking_p_qty =prod[0].product_qty
                line.stock_move=prod

    def _compute_stock_move_line(self):
        for line in self:
            line.stock_move_line=self.env["stock.move.line"].search(
                [("picking_id", "=", line.id)]
            )

    def _compute_to_sale_order(self):
        for record in self:
            if record.sale_id.partner_id.commercial_company_name :
                record.stock_picking_company_name = "株式会社 " + record.sale_id.partner_id.commercial_company_name+ " 様"
            else:
                record.stock_picking_company_name = ""

            if record.sale_id.shiratani_entry_date:
                record.stock_picking_shiratani_entry_date =  (
                    str(record.sale_id.shiratani_entry_date.year)
                    + "年"
                    + str(record.sale_id.shiratani_entry_date.month)
                    + "月"
                    + str(record.sale_id.shiratani_entry_date.day)
                    + "日"
                )
            else:
                record.stock_picking_shiratani_entry_date= ""

            if record.scheduled_date:
                record.stock_picking_scheduled_date =  (
                    str(record.scheduled_date.year)
                    + "年"
                    + str(record.scheduled_date.month)
                    + "月"
                    + str(record.scheduled_date.day)
                    + "日"
                )
            else:
                record.stock_picking_scheduled_date= ""

            partner_info = ""
            if record.sale_id.partner_id.display_name:
                if "," in record.sale_id.partner_id.display_name:
                    partner_info += record.sale_id.partner_id.display_name.split(',')[0]+ "-" + record.sale_id.partner_id.display_name.split(',')[1] + " 様　ご依頼分-"
                else:
                    partner_info += record.sale_id.partner_id.display_name + " 様　ご依頼分-"
            # if record.sale_id.partner_id.department:
            #     partner_info += record.sale_id.partner_id.department + "-"
            # if record.sale_id.partner_id.site:
            #     partner_info += record.sale_id.partner_id.site + "-"
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
                partner_address += record.sale_id.partner_id.state_id.name
            record.stock_picking_partner_address = "〒" + partner_address

            partner_tel_phone = ""
            if record.sale_id.partner_id.phone and record.sale_id.partner_id.mobile:
                partner_tel_phone = record.sale_id.partner_id.phone + "/" + record.sale_id.partner_id.mobile
            elif record.sale_id.partner_id.phone and not record.sale_id.partner_id.mobile:
                partner_tel_phone = record.sale_id.partner_id.phone
            elif not record.sale_id.partner_id.phone and record.sale_id.partner_id.mobile:
                partner_tel_phone = record.sale_id.partner_id.mobile
            record.stock_picking_partner_tel_phone = partner_tel_phone

            witness_name_phone = ""
            if record.sale_id.witness:
                witness_name_phone += record.sale_id.witness
            if record.sale_id.witness_phone:
                witness_name_phone += " " + record.sale_id.witness_phone
            record.stock_picking_witness_name_phone = witness_name_phone

            printing_staff = ""
            if record.sale_id.user_id.name:
                printing_staff += record.sale_id.user_id.name+ "  印"
            record.stock_picking_printing_staff = printing_staff

            day = str(datetime.now().day)
            month = str(datetime.now().month)
            year = str(datetime.now().year)
            record.stock_picking_current_date = year + " 年 " + month + " 月 " + day + " 日 "
            
            estimated_shipping_date=record.sale_id.estimated_shipping_date
            if estimated_shipping_date:
                record.stock_estimated_shipping_date = (
                    str(estimated_shipping_date.year)
                    + "年"
                    + str(estimated_shipping_date.month)
                    + "月"
                    + str(estimated_shipping_date.day)
                    + "日"
                )
            else:
                record.stock_estimated_shipping_date = ""

            scheduled_date=record.scheduled_date
            if scheduled_date:
                record.stock_scheduled_date = (
                    str(scheduled_date.year)
                    + "年"
                    + str(scheduled_date.month)
                    + "月"
                    + str(scheduled_date.day)
                    + "日"
                )
            else:
                record.stock_scheduled_date = ""

            partner_address= ""
            if record.sale_id.partner_id.zip:
                partner_address += record.sale_id.partner_id.zip + " "
            if record.sale_id.partner_id.street:
                partner_address += record.sale_id.partner_id.street + " "
            if record.sale_id.partner_id.street2:
                partner_address += record.sale_id.partner_id.street2 + " "
            if record.sale_id.partner_id.city:
                partner_address += record.sale_id.partner_id.city + " "
            if record.sale_id.partner_id.state_id.name:
                partner_address += record.sale_id.partner_id.state_id.name
            record.stock_partner_address = "〒" + partner_address
            
            if record.sale_id.user_id.name:
                record.stock_printing_staff = record.sale_id.user_id.name + "  印"

class StockMoveExcelReport(models.Model):
    _inherit = "stock.move"

    stock_index= fields.Char(
        "Stock index",
        compute="_compute_stock_move",
    )
    product_name= fields.Char(
        "Product name",
        compute="_compute_stock_move",
    )

    product_number_and_size= fields.Char(
        "Product number and size",
        compute="_compute_stock_move",
    )

    product_attribute= fields.Char(
        "Product attribute",
        compute="_compute_stock_move",
    )

    packages_number= fields.Char(
        "Number packages",
        compute="_compute_stock_move",
    )

    action_packages= fields.Char(
        "Action packages",
        compute="_compute_stock_move",
    )

    action_assemble= fields.Char(
        "Action assemble",
        compute="_compute_stock_move",
    )

    stock_sai= fields.Char(
        "Stock sai",
        compute="_compute_stock_move",
    )
    
    stock_warehouse= fields.Char(
        "Stock warehouse",
        compute="_compute_stock_move",
    )

    stock_shiratani_date= fields.Char(
        "Shiratani date",
        compute="_compute_stock_move",
    )

    def _compute_stock_move(self):
        index=0
        for line in self:
            line.product_attribute=""
            index=index+1
            line.stock_index=index

            p_type = ""
            if line.p_type:
                if line.p_type == "special":
                    p_type = "別注"
                elif line.p_type == "custom":
                    p_type = "特注"
            line.product_name = line.product_id.name + "\n" + p_type

            size_detail = ""
            if line.product_id.product_no:
                size_detail += str(line.product_id.product_no) + "\n"
            if line.product_id.width:
                size_detail += "W" + str(line.product_id.width) + " "
            if line.product_id.depth:
                size_detail += "D" + str(line.product_id.depth) + " "
            if line.product_id.height:
                size_detail += "H" + str(line.product_id.height) + " "
            if line.product_id.ah:
                size_detail += "AH" + str(line.product_id.ah) + " "
            line.product_number_and_size = size_detail

            for attribute_value in line.product_id.product_template_attribute_value_ids:
                attribute_name = attribute_value.attribute_id.name
                attribute_value_name = attribute_value.product_attribute_value_id.name
                
                if attribute_name and attribute_value_name:
                    line.product_attribute += f"{attribute_name}:{attribute_value_name}\n"

            if line.product_id.two_legs_scale:
                line.packages_number = math.ceil(
                    line.product_uom_qty / line.product_id.two_legs_scale
                )
            else:
                line.packages_number = line.product_uom_qty

            line.action_packages="有"
            line.action_assemble="無"
            line.stock_sai=line.product_id.product_tmpl_id.sai
            line.stock_warehouse=line.warehouse_id.name
            line.stock_shiratani_date=line.sale_line_id.shiratani_date

class AccountMoveExcelReport(models.Model):   
    _inherit = "account.move"

    sale_order_line = fields.One2many(
        "sale.order.line",
        string="Sale order line",
        copy=True,
        auto_join=True,
        compute="_compute_sale_order_line",
    ) 

    sale_order = fields.One2many(
        "sale.order",
        string="Sale order",
        copy=True,
        auto_join=True,
        compute="_compute_sale_order",
    ) 

    def _compute_sale_order(self):
        for line in self: 
            line.sale_order=self.env["sale.order"].search(
                    [("name", "=", line.invoice_origin)]
                )
    
    def _compute_sale_order_line(self):
        for line in self: 
            line.sale_order_line=self.env["sale.order.line"].search(
                    [("order_id.name", "=", line.invoice_origin)]
                )
