from odoo import models
from datetime import datetime 
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.report_quotation_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, so_data):
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        logo_R = PILImage.open(image_logo_R)
        logo_R = logo_R.convert('RGB')
        logo_R = logo_R.resize((86, 62))
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        image_logo_ritzwell = get_module_resource('rtw_excel_report', 'img', 'ritzwell.png')
        img_ritzwell = PILImage.open(image_logo_ritzwell)
        img_ritzwell = img_ritzwell.convert('RGB')
        img_ritzwell = img_ritzwell.resize((220, 45))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13, 'text_wrap':True,'bottom':1})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_text_Wrap = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11, 'text_wrap':True})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})
        format_text_13 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13})
        format_text_13_border = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13,'bottom':1})
        format_text_14 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_money_bgRed = workbook.add_format({'align': 'left','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})
        format_money_bgRed_right = workbook.add_format({'align': 'right','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})

        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':10})
        format_sale_no = workbook.add_format({'align': 'right','valign': 'bottom','text_wrap':True, 'font_name': font_name,'font_size':10})
        format_address = workbook.add_format({'align': 'right','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':10})
    
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':9,'color':'white','bold':True})
        format_lines_13 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':13})
        format_lines_12 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':12})
        format_lines_12_left = workbook.add_format({'align': 'left','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':12})
        format_lines_11 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':11})
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':10})
        format_lines_10_left= workbook.add_format({'align': 'left','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':10})

        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet = workbook.add_worksheet(sheet_name)
            
            sheet.set_column("A:A", width=12,cell_format=font_family)  
            sheet.set_column("B:B", width=20,cell_format=font_family)  
            sheet.set_column("C:C", width=18,cell_format=font_family)  

            sheet.set_column("D:D", width=16,cell_format=font_family)  

            sheet.set_column("E:E", width=10,cell_format=font_family)  
            sheet.set_column("F:F", width=10,cell_format=font_family)

            sheet.set_column("G:G", width=10,cell_format=font_family)  
            sheet.set_column("H:H", width=26,cell_format=font_family)  

            sheet.set_column("I:I", width=6.5,cell_format=font_family)  
            sheet.set_column("J:J", width=6.5,cell_format=font_family)  
            sheet.set_column("K:K", width=6.5,cell_format=font_family) 

            sheet.set_column("L:L", width=14.5,cell_format=font_family) 
            sheet.set_column("M:M", width=14.5,cell_format=font_family) 
            sheet.set_column("N:Z", None,cell_format=font_family) 
            
            sheet.set_row(1, 46)
            sheet.set_row(14, 24)
            sheet.set_row(16, 26)
            
            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})
            
            # y,x
            sheet.write(1, 1, "御見積書", format_sheet_title) 

            sheet.merge_range(2, 0,3,1,  so.send_to_company if so.send_to_company else '', format_name_company)

            sheet.write(5,0, "平素より格別のお引き⽴てを賜り暑く御礼申し上げます。", format_text) 
            sheet.write(6,0, "御依頼の件、書きの通りお⾒積り致しました。", format_text) 
            sheet.write(7,0, "ご査収の程宜しくお願い致します。", format_text) 
            sheet.write(10, 0, "件名", format_text_13_border) 
            sheet.write(12, 0, "税抜合計", format_text) 
            sheet.write(13, 0, "消費税", format_text) 
            sheet.write(14, 0, "⽀払条件：", format_money_bgRed) 
            sheet.write(10, 1, so.title if so.title else '', format_text_13_border) 
            sheet.write(12, 1, so.sale_order_amount_untaxed if so.sale_order_amount_untaxed else '', format_text_right) 
            sheet.write(13, 1, so.sale_order_amount_tax if so.sale_order_amount_tax else '', format_text_right) 
            sheet.write(14, 1, so.sale_order_amount_total if so.sale_order_amount_total else '', format_money_bgRed_right) 


            sheet.write(2,5, "納品希望⽇：", format_text_right) 
            sheet.write(3,5, "製作⽇数：", format_text_right) 
            sheet.write(4,5, "発注期限：", format_text_right) 
            sheet.write(5,5, "納品場所：", format_text_right) 
            sheet.write(6,5, "納品希望⽇：", format_text_right) 
            sheet.write(8,5, "⾒積有効期限：", format_text_right) 
            sheet.write(9,5, "備考：", format_text_right) 
            
            sheet.write(2,6, so.preferred_delivery_period if so.preferred_delivery_period else '', format_text) 
            sheet.write(3,6, so.workdays if so.workdays else '', format_text) 
            sheet.write(4,6, so.sale_order_date_deadline if so.sale_order_date_deadline else '', format_text) 
            sheet.write(5,6, so.forwarding_address if so.forwarding_address else '', format_text) 
            sheet.write(6,6,so.sale_order_transactions_term if so.sale_order_transactions_term else '', format_text) 
            sheet.write(8,6, so.sale_order_validity_date if so.sale_order_validity_date else '', format_text) 
            sheet.merge_range(9,6,11,9,so.sale_order_special_note if so.sale_order_special_note else '', format_note) 

            sheet.write(0,12, so.sale_order_current_date if so.sale_order_current_date else '' , format_date) 
            sheet.merge_range(1,11,1,12, so.name if so.name else '' , format_sale_no) 
            sheet.merge_range(2,11,8,12, so.sale_order_hr_employee if so.sale_order_hr_employee else '' , format_address) 

            sheet.write(13, 9,so.sale_order_total_list_price if so.sale_order_total_list_price else '', format_text_right) 
            sheet.write(13, 12, so.sale_order_amount_untaxed if so.sale_order_amount_untaxed else '' , format_text_right) 
            sheet.write(14, 12,so.name if so.name else '' , format_text_right) 
            # sheet.write(12, 0, "住所", format_text) 
            # sheet.write(13, 0, "TEL", format_text) 
            
        #     sheet.write(1, 2, mrp.sale_order.sale_order_send_to_company if mrp.sale_order.sale_order_send_to_company else '', format_name_company) 
        #     sheet.write(1, 8, mrp.sale_order.check_oversea if mrp.sale_order.check_oversea else '', format_text_13) 
        #     sheet.write(0,9, mrp.sale_order.sale_order_current_date if mrp.sale_order.sale_order_current_date else '', format_date)
        #     sheet.write(3, 1, mrp.sale_order.sale_order_name if mrp.sale_order.sale_order_name else '', format_text) 
        #     sheet.write(15, 9, mrp.sale_order.amount_untaxed if mrp.sale_order.amount_untaxed else '', format_text_13_bold_right) 
        #     sheet.write(16, 9, mrp.sale_order.sale_order_name if mrp.sale_order.sale_order_name else '', format_text_9) 
        #     sheet.write(5, 1, mrp.sale_order.sale_order_estimated_shipping_date if mrp.sale_order.sale_order_estimated_shipping_date else '', format_text_14) 
        #     sheet.write(6, 1, mrp.sale_order.sale_order_preferred_delivery_date if mrp.sale_order.sale_order_preferred_delivery_date else '', format_text_12) 
        #     sheet.write(8, 1, mrp.sale_order.title if mrp.sale_order.title else '', format_text_14) 
        #     sheet.write(9, 1, mrp.sale_order.sale_order_info_cus if mrp.sale_order.sale_order_info_cus else '', format_text_12) 
        #     sheet.write(11, 1, mrp.sale_order.sale_order_company_name if mrp.sale_order.sale_order_company_name else '', format_text_12) 
        #     sheet.write(12, 1, mrp.sale_order.sale_order_detail_address_partner if mrp.sale_order.sale_order_detail_address_partner else '', format_text_12) 
        #     sheet.write(13, 1, mrp.sale_order.partner_id.phone if mrp.sale_order.partner_id.phone else '', format_text_12) 
            
            # y,x,y,x
        #     sheet.merge_range(11,8,14,9, mrp.mrp_note if mrp.mrp_note else '', format_remark_note)   
        #     sheet.merge_range(3,9,9,9, mrp.sale_order.sale_order_hr_employee if mrp.sale_order.sale_order_hr_employee else '', format_remark_note)

            #table title
            sheet.write(16, 0, "№", format_table)
            sheet.write(16, 1, "品名", format_table)
            sheet.merge_range(16, 2,16,3, "品番・サイズ", format_table)
            sheet.merge_range(16, 4,16,6, "仕様・詳細", format_table)
            sheet.write(16, 7, "仕様・詳細", format_table)
            sheet.write(16,8, "数量", format_table)
            sheet.write(16, 9, "定価", format_table)
            sheet.write(16, 10, "掛率 ", format_table)
            sheet.write(16, 11, "販売単価", format_table)
            sheet.write(16, 12, "販売⾦額", format_table)

            # row=18
            # sheet.write(row, 0, 1, format_lines_10)
            # sheet.write(row, 1, mrp.mrp_product_name_excel, format_lines_11)
            
            # sheet.write(row, 2, mrp.mrp_product_attribute, format_lines_12_left)
            # sheet.write(row, 3, mrp.mrp_product_attribute_summary, format_lines_10_left)
            
            # sheet.write(row, 4, mrp.mrp_product_product_qty, format_lines_13)
            # if mrp.product_id.product_tmpl_id.uom_id.name:
            #     sheet.write(row, 5, mrp.product_id.product_tmpl_id.uom_id.name, format_lines_12)
            # else:
            #     sheet.write(row, 5, "", format_lines_12)
            # sheet.write(row, 6, "", format_lines_13)
            # sheet.write(row, 7, "", format_lines_13)
            # sheet.write(row, 8, mrp.mrp_product_config_cus_excel, format_lines_13)
            # sheet.write(row, 9, mrp.production_memo, format_lines_13)
            