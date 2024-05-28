from odoo import models
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.delivery_sale_order_xls'
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
        img_ritzwell = img_ritzwell.resize((215, 40))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'bottom','font_size':18,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_text_12 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':12})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})
        format_text_14 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})

        format_address = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':10})
    
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':11,'color':'white','bold':True})
    
        format_lines_note = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        
        format_lines_9_left= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':9,'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':13,'bottom':1})

        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet= workbook.add_worksheet(sheet_name)
            sheet_data= workbook.add_worksheet("data")
            sheet_data.hide()
            
            sheet.set_paper(9)  #A4
            sheet.set_landscape()
            # sheet.set_print_scale(66)
            
            margin_header = 0.3
            margin_footer = 0.3
            left_margin = 0.8
            right_margin = 0.7
            top_margin = 0.5
            bottom_margin = 0.5

            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
            header_parts = []
            if so.name:
                header_parts.append(so.name)
            if so.sale_order_current_date:
                header_parts.append('\n '+ so.sale_order_current_date)
            header_text = " &R " + " ".join(header_parts)

            sheet.set_header(header_text, margin=margin_header)
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)   

            sheet.set_column("A:A", width=17,cell_format=font_family)  
            sheet.set_column("B:B", width=20,cell_format=font_family)  
            sheet.set_column("C:C", width=18,cell_format=font_family)  

            sheet.set_column("D:D", width=16,cell_format=font_family)  

            sheet.set_column("E:E", width=10,cell_format=font_family)  
            sheet.set_column("F:F", width=10,cell_format=font_family)

            sheet.set_column("G:G", width=10,cell_format=font_family)  
            sheet.set_column("H:H", width=26,cell_format=font_family)  

            sheet.set_column("I:I", width=8,cell_format=font_family)  
            sheet.set_column("J:J", width=8,cell_format=font_family)  
            sheet.set_column("K:K", width=8,cell_format=font_family) 

            sheet.set_column("L:L", width=8,cell_format=font_family) 
            sheet.set_column("M:M", width=8,cell_format=font_family) 
            sheet.set_column("N:N", width=24,cell_format=font_family) 
            sheet.set_column("O:Z", None,cell_format=font_family) 
            
            sheet.set_row(1, 35)
            sheet.set_row(2, 17)
            sheet.set_row(3, 17)
            sheet.set_row(5, 15)
            sheet.set_row(6, 15)
            sheet.set_row(7, 15)
            sheet.set_row(8, 12)
            sheet.set_row(9, 12)
            sheet.set_row(20,32)
            
            sheet.insert_image(0, 0, "logo", {'image_data': img_io_R})
            sheet.insert_image(1, 12, "logo2", {'image_data': img_io_ritzwell, 'y_offset': 2})
            
            # y,x
            sheet.write(1, 1, "配送依頼書", format_sheet_title) 
            
            send_to = ""
            company = ""
            if so.partner_id and so.partner_id.parent_id and so.partner_id.parent_id.name:
                company = so.partner_id.parent_id.name
            elif so.partner_id.name:
                company = so.partner_id.name
                    
            if so.lang_code == "en_US":
                if company:
                    send_to += "御中 " + company + " 株式会社" 
            else:
                if company:
                    send_to += "株式会社 " + company + " 御中"
                    
            sheet.write(1, 2, send_to, format_name_company)
            
            sheet.write(2, 0,  "発注番号", format_text) 
            sheet.write(2, 1, so.name if so.name else "", format_text_14) 
            
            sheet.write(4,0, "搬入日時", format_text) 
            sheet.write(5,0, "入荷日", format_text) 
            sheet.write(4,1, so.sale_order_warehouse_arrive_date if so.sale_order_warehouse_arrive_date else "", format_text_12) 
            sheet.write(5,1, "", format_text_12) 
            
            sheet.write(7, 0, "お届け先（物件名）", format_text_12) 
            sheet.write(7, 1, so.title if so.title else "", format_text) 
            sheet.write(8, 1, so.sale_order_partner_info if so.sale_order_partner_info else "", format_text) 
            
            sheet.write(10, 0, "住所", format_text) 
            sheet.write(11, 0, "TEL／携帯", format_text) 
            sheet.write(10, 1, so.sale_order_partner_address if so.sale_order_partner_address else "", format_text) 
            phone = ""
            if so.partner_id.phone and so.partner_id.mobile:
                phone += so.partner_id.phone + "/" + so.partner_id.mobile
            elif so.partner_id.phone:
                phone += so.partner_id.phone
            elif so.partner_id.mobile:
                phone += so.partner_id.mobile
            sheet.write(11, 1, phone, format_text) 
            
            sheet.write(13, 0, "配送", format_text) 
            sheet.write(14, 0, "デポ", format_text) 
            sheet.write(15, 0, "配送ラベル", format_text) 
            sheet.write(16, 0, "設置先〒", format_text) 
            sheet.write(13, 1, so.sale_order_sipping_to if so.sale_order_sipping_to else "", format_text) 
            sheet.write(14, 1, so.waypoint.name if so.waypoint and so.waypoint.name else "", format_text) 
            sheet.write(15, 1, so.shipping_to_text if so.shipping_to_text else "", format_text) 
            sheet.write(16, 1, so.forwarding_address_zip if so.forwarding_address_zip else "", format_text) 
            
            sheet.write(13, 3, "設置先", format_text_right) 
            sheet.merge_range(13, 4, 15, 6, so.forwarding_address[:120]  if so.forwarding_address else "", format_note) 
            
            sheet.write(18, 0, "搬入立会人", format_text) 
            sheet.write(18, 1, so.witness if so.witness else "", format_text) 
            
            sheet.write(10,7, "送り状注記", format_text_right) 
            sheet.merge_range(10,8,12,11,so.sale_order_special_note[:120] if so.sale_order_special_note else '', format_note) 
            
            sheet.merge_range(2,12,8,13, so.sale_order_hr_employee if so.sale_order_hr_employee else '' , format_address) 

            #table title
            sheet.write(20, 0, "№", format_table)
            sheet.write(20, 1, "品名", format_table)
            sheet.merge_range(20, 2,20,3, "品番・サイズ", format_table)
            sheet.merge_range(20, 4,20,6, "仕様・詳細", format_table)
            sheet.write(20, 7, "仕様・詳細", format_table)
            sheet.write(20,8, "数量", format_table)
            sheet.write(20, 9, "個口数", format_table)
            sheet.write(20, 10, "取説", format_table)
            sheet.write(20, 11, "開梱 ", format_table)
            sheet.write(20, 12, "組立", format_table)
            sheet.write(20, 13, "販売⾦額", format_table)

            if so.order_line:
                row = 21
                merge_line = 6 
                for ind,line in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                    
                    if line.display_type == 'line_note':
                        sheet.merge_range(row, 0, row, 12, "=data!A" + str(ind * 1 + 1), format_lines_note) 
                        sheet_data.write(ind, 0, line.name if line.name else '', format_lines_note) 
                        row += 1
                    elif line.display_type == 'line_section':
                        sheet.merge_range(row, 0, row ,12, "=data!B" + str(ind * 1 + 1), format_lines_section) 
                        sheet_data.write(ind, 1, line.name if line.name else '' , format_lines_section) 
                        row += 1
                    else:
                        sheet.merge_range(row, 0, row + merge_line, 0, line.sale_order_index if line.sale_order_index else '' , format_lines_10) 
                        sheet.merge_range(row, 1, row + merge_line, 1, line.sale_order_line_name_excel if line.sale_order_line_name_excel else '', format_lines_9_left) 
                        
                        sheet.merge_range(row, 2, row + merge_line, 3, line.sale_order_number_and_size if line.sale_order_number_and_size else '', format_lines_11_left) 
                        
                        sheet.merge_range(row, 4, row + merge_line, 6, line.sale_order_product_detail if line.sale_order_product_detail else '', format_lines_10_left) 
                        sheet.merge_range(row, 7, row + merge_line, 7, line.sale_order_product_detail_2 if line.sale_order_product_detail_2 else '', format_lines_10_left) 
                        
                        sheet.merge_range(row, 8, row + merge_line, 8, line.sale_order_line_product_uom_qty if line.sale_order_line_product_uom_qty else '', format_lines_13) 
                        sheet.merge_range(row, 9, row + merge_line, 9, '{0:,.0f}'.format(line.sale_line_calculate_packages)if line.sale_line_calculate_packages else 0, format_lines_13) 
                       
                        sheet.merge_range(row, 10, row + merge_line, 10, '有' if line.instruction_status else '', format_lines_13) 
                        sheet.merge_range(row, 11, row + merge_line, 11, '有', format_lines_13) 
                        sheet.merge_range(row, 12, row + merge_line, 12, '無', format_lines_13) 
                        sheet.merge_range(row, 13, row + merge_line, 13, '', format_lines_13) 
                        
                        row += merge_line + 1
