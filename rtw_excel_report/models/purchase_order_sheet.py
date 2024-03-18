from odoo import models
from datetime import datetime 
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.purchase_order_sheet_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, mrp_data):
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        logo_R = PILImage.open(image_logo_R)
        logo_R = logo_R.convert('RGB')
        logo_R = logo_R.resize((55, 55))
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        image_logo_ritzwell = get_module_resource('rtw_excel_report', 'img', 'ritzwell.png')
        img_ritzwell = PILImage.open(image_logo_ritzwell)
        img_ritzwell = img_ritzwell.convert('RGB')
        img_ritzwell = img_ritzwell.resize((125, 25))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':18,'font_name': font_name,})
        format_name_company = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13})
        
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_13 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13})
        format_text_13_bold_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':13,'bold':True})
        format_text_9 = workbook.add_format({'align': 'right','font_name': font_name,'font_size':9})
        format_text_14 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_text_12 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':12})
        
        format_remark_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})
        
        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':9})
        
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#595959', 'font_name': font_name,'font_size':9,'color':'white','bold':True})
        
        format_lines_13 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':13})
        format_lines_12 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':12})
        format_lines_12_left = workbook.add_format({'align': 'left','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':12})
        format_lines_11 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':11})
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':10})
        format_lines_10_left= workbook.add_format({'align': 'left','valign': 'vcenter','bg_color': '#dddddd', 'text_wrap':True,'font_name': font_name,'font_size':10})

        #create sheet
        for index,mrp in enumerate(mrp_data):
            sheet_name = f"{mrp.name}" 
            sheet = workbook.add_worksheet(sheet_name)
            
            sheet.set_column("A:A", width=11,cell_format=font_family)  
            sheet.set_column("B:B", width=28,cell_format=font_family)  
            sheet.set_column("C:C", width=30,cell_format=font_family)  
            sheet.set_column("D:D", width=15,cell_format=font_family)  
            sheet.set_column("E:E", width=10,cell_format=font_family)  
            sheet.set_column("F:F", width=5,cell_format=font_family)
            sheet.set_column("G:G", width=19,cell_format=font_family)  
            sheet.set_column("H:H", width=25,cell_format=font_family)  
            sheet.set_column("I:I", width=23,cell_format=font_family)  
            sheet.set_column("J:J", width=27,cell_format=font_family)  
            sheet.set_column("K:Z", None,cell_format=font_family) 
            
            sheet.set_row(0, 18)
            sheet.set_row(5, 18)
            sheet.set_row(6, 18)
            sheet.set_row(8, 18)
            sheet.set_row(11, 18)
            sheet.set_row(12, 18)
            sheet.set_row(13, 18)
            sheet.set_row(17, 25)
            
            sheet.insert_image(0, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 9, "logo2", {'image_data': img_io_ritzwell})
            
            # y,x
            sheet.write(1, 1, "発注書", format_sheet_title) 
            sheet.write(3, 0, "発注書", format_text) 
            sheet.write(5, 0, "送り先着日", format_text) 
            sheet.write(6, 0, "出荷希望日", format_text) 
            sheet.write(8, 0, "物件名", format_text) 
            sheet.write(11, 0, "送り先", format_text) 
            sheet.write(10, 8, "送り先注記", format_text) 
            sheet.write(15, 8, "販売価格合計", format_text_13) 
            sheet.write(12, 0, "住所", format_text) 
            sheet.write(13, 0, "TEL", format_text) 
            
            sheet.write(1, 2, mrp.sale_order.sale_order_send_to_company if mrp.sale_order.sale_order_send_to_company else '', format_name_company) 
            sheet.write(1, 8, mrp.sale_order.check_oversea if mrp.sale_order.check_oversea else '', format_text_13) 
            sheet.write(0,9, mrp.sale_order.sale_order_current_date if mrp.sale_order.sale_order_current_date else '', format_date)
            sheet.write(3, 1, mrp.sale_order.sale_order_name if mrp.sale_order.sale_order_name else '', format_text) 
            sheet.write(15, 9, mrp.sale_order.amount_untaxed if mrp.sale_order.amount_untaxed else '', format_text_13_bold_right) 
            sheet.write(16, 9, mrp.sale_order.sale_order_name if mrp.sale_order.sale_order_name else '', format_text_9) 
            sheet.write(5, 1, mrp.sale_order.sale_order_estimated_shipping_date if mrp.sale_order.sale_order_estimated_shipping_date else '', format_text_14) 
            sheet.write(6, 1, mrp.sale_order.sale_order_preferred_delivery_date if mrp.sale_order.sale_order_preferred_delivery_date else '', format_text_12) 
            sheet.write(8, 1, mrp.sale_order.title if mrp.sale_order.title else '', format_text_14) 
            sheet.write(9, 1, mrp.sale_order.sale_order_info_cus if mrp.sale_order.sale_order_info_cus else '', format_text_12) 
            sheet.write(11, 1, mrp.sale_order.sale_order_company_name if mrp.sale_order.sale_order_company_name else '', format_text_12) 
            sheet.write(12, 1, mrp.sale_order.sale_order_detail_address_partner if mrp.sale_order.sale_order_detail_address_partner else '', format_text_12) 
            sheet.write(13, 1, mrp.sale_order.partner_id.phone if mrp.sale_order.partner_id.phone else '', format_text_12) 
            
            # y,x,y,x
            sheet.merge_range(11, 8,14,9, mrp.mrp_note if mrp.mrp_note else '', format_remark_note)
            sheet.merge_range(3,9,9,9, mrp.sale_order.sale_order_hr_employee if mrp.sale_order.sale_order_hr_employee else '', format_remark_note)

            #table title
            sheet.write(17, 0, "№", format_table)
            sheet.write(17, 1, "品名", format_table)
            sheet.write(17, 2, "仕様・詳細", format_table)
            sheet.write(17, 3, "摘要", format_table)
            sheet.write(17, 4, "数量", format_table)
            sheet.write(17, 5, "", format_table)
            sheet.write(17, 6, "単価", format_table)
            sheet.write(17, 7, "発注金額 ", format_table)
            sheet.write(17, 8, "Custom", format_table)
            sheet.write(17, 9, "メモ", format_table)

            row=18
            sheet.write(row, 0, 1, format_lines_10)
            sheet.write(row, 1, mrp.mrp_product_name_excel, format_lines_11)
            
            sheet.write(row, 2, mrp.mrp_product_attribute, format_lines_12_left)
            sheet.write(row, 3, mrp.mrp_product_attribute_summary, format_lines_10_left)
            
            sheet.write(row, 4, mrp.mrp_product_product_qty, format_lines_13)
            if mrp.product_id.product_tmpl_id.uom_id.name:
                sheet.write(row, 5, mrp.product_id.product_tmpl_id.uom_id.name, format_lines_12)
            else:
                sheet.write(row, 5, "", format_lines_12)
            sheet.write(row, 6, "", format_lines_13)
            sheet.write(row, 7, "", format_lines_13)
            sheet.write(row, 8, mrp.mrp_product_config_cus_excel, format_lines_13)
            sheet.write(row, 9, mrp.production_memo, format_lines_13)
            