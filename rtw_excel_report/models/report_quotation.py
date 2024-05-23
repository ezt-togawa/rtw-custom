from odoo import models
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
        img_ritzwell = img_ritzwell.resize((215, 40))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14, 'text_wrap':True,'bottom':1})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_text_12_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':12})
        format_text_13_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':13})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})
        format_text_14_border = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14,'bottom':1})
        format_money_bgRed = workbook.add_format({'align': 'left','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})
        format_money_bgRed_right = workbook.add_format({'align': 'right','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})

        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':10})
        format_address = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':10})
    
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':11,'color':'white','bold':True})
    
        format_lines_note = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        
        format_lines_9_left= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':9,'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left','valign': 'top', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
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
            sheet.set_header( f'{"&"}R {so.name  if so.name else ""}', margin=margin_header) 
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)   

            sheet.set_column("A:A", width=13,cell_format=font_family)  
            sheet.set_column("B:B", width=20,cell_format=font_family)  
            sheet.set_column("C:C", width=18,cell_format=font_family)  

            sheet.set_column("D:D", width=16,cell_format=font_family)  

            sheet.set_column("E:E", width=10,cell_format=font_family)  
            sheet.set_column("F:F", width=10,cell_format=font_family)

            sheet.set_column("G:G", width=10,cell_format=font_family)  
            sheet.set_column("H:H", width=26,cell_format=font_family)  

            sheet.set_column("I:I", width=6.5,cell_format=font_family)  
            sheet.set_column("J:J", width=14.5,cell_format=font_family)  
            sheet.set_column("K:K", width=6.5,cell_format=font_family) 

            sheet.set_column("L:L", width=14.5,cell_format=font_family) 
            sheet.set_column("M:M", width=14.5,cell_format=font_family) 
            sheet.set_column("N:Z", None,cell_format=font_family) 
            
            sheet.set_row(1, 46)
            sheet.set_row(2, 17)
            sheet.set_row(3, 17)
            sheet.set_row(5, 15)
            sheet.set_row(6, 15)
            sheet.set_row(7, 15)
            sheet.set_row(8, 12)
            sheet.set_row(9, 12)
            sheet.set_row(11, 22)
            sheet.set_row(12, 24)
            sheet.set_row(13, 22)
            sheet.set_row(14, 26)
            sheet.set_row(15, 24)
            sheet.set_row(16,32)
            
            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})
            
            # y,x
            sheet.write(1, 1, "御見積書", format_sheet_title) 
            sheet.merge_range(2, 0,3,2,  so.dear_to if so.dear_to else '', format_name_company)
            sheet.write(5,0, "平素より格別のお引き⽴てを賜り暑く御礼申し上げます。", format_text) 
            sheet.write(6,0, "御依頼の件、下記の通りお⾒積り致しました。", format_text)
            sheet.write(7,0, "ご査収の程宜しくお願い致します。", format_text) 
            sheet.write(10, 0, "件名", format_text_14_border) 
            sheet.write(12, 0, "税抜合計", format_text) 
            sheet.write(13, 0, "消費税", format_text) 
            sheet.write(14, 0, "税込合計", format_money_bgRed) 
            sheet.write(10, 1, so.title if so.title else '', format_text_14_border) 
            sheet.write(12, 1, so.sale_order_amount_untaxed if so.sale_order_amount_untaxed else '', format_text_13_right) 
            sheet.write(13, 1, so.sale_order_amount_tax if so.sale_order_amount_tax else '', format_text_12_right) 
            sheet.write(14, 1, so.sale_order_amount_total if so.sale_order_amount_total else '', format_money_bgRed_right) 

            sheet.write(2,5, "納品希望⽇：", format_text_right) 
            sheet.write(3,5, "製作⽇数：", format_text_right) 
            sheet.write(4,5, "発注期限：", format_text_right) 
            sheet.write(5,5, "納品場所：", format_text_right) 
            sheet.write(6,5, "⽀払条件：", format_text_right) 
            sheet.write(8,5, "⾒積有効期限：", format_text_right) 
            sheet.write(9,5, "備考：", format_text_right) 
            sheet.write(2,6, so.preferred_delivery_period if so.preferred_delivery_period else '', format_text) 
            sheet.write(3,6, so.workday_id.name if so.workday_id else '', format_text) 
            sheet.write(4,6, so.sale_order_date_deadline if so.sale_order_date_deadline else '', format_text) 
            sheet.write(5,6, so.forwarding_address if so.forwarding_address else '', format_text) 
            sheet.write(6,6,so.sale_order_transactions_term if so.sale_order_transactions_term else '', format_text) 
            sheet.write(8,6, so.sale_order_validity_date if so.sale_order_validity_date else '', format_text) 
            sheet.merge_range(9,6,11,8,so.sale_order_special_note[:120] if so.sale_order_special_note else '', format_note) 

            sheet.merge_range(0,11,0,12, so.sale_order_current_date if so.sale_order_current_date else '' , format_date) 
            sheet.merge_range(2,11,8,12, so.sale_order_hr_employee if so.sale_order_hr_employee else '' , format_address) 

            sheet.write(13, 9,'定価合計: ' + str( so.sale_order_total_list_price ) if so.sale_order_total_list_price else '', format_text_right) 
            sheet.write(13, 12,'販売価格合計: ' + str(so.sale_order_amount_untaxed2) if so.sale_order_amount_untaxed2 else '' , format_text_right) 
            sheet.write(14, 12,so.name if so.name else '' , format_text_right) 

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

            if so.order_line:
                row = 17
                merge_line = 6 
                for ind,line in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                    
                    if line.display_type == 'line_note':
                        sheet.merge_range(row,0,row ,12, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                        sheet_data.write(ind,0, line.name if line.name else '', format_lines_note) 
                        row += 1
                    elif line.display_type == 'line_section':
                        sheet.merge_range(row,0,row ,12, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                        sheet_data.write(ind,1,line.name if line.name else '' , format_lines_section) 
                        row += 1
                    else:

                        sheet.merge_range(row,0,row + merge_line,0, line.sale_order_index if line.sale_order_index else '' , format_lines_10) 
                        sheet.merge_range(row,1,row + merge_line,1, line.sale_order_line_name_excel if line.sale_order_line_name_excel else '' , format_lines_9_left) 
                        
                        sheet.merge_range(row,2,row + merge_line,3, line.sale_order_number_and_size if line.sale_order_number_and_size else '' , format_lines_11_left) 
                        
                        sheet.merge_range(row,4,row + merge_line,6, line.sale_order_product_detail if line.sale_order_product_detail else '' , format_lines_10_left) 
                        sheet.merge_range(row,7,row + merge_line,7, line.sale_order_product_detail_2 if line.sale_order_product_detail_2 else '' , format_lines_10_left) 
                        
                        sheet.merge_range(row,8,row + merge_line,8, line.sale_order_line_product_uom_qty if line.sale_order_line_product_uom_qty else '' , format_lines_13) 
                        sheet.merge_range(row,9,row + merge_line,9, line.sale_order_price_unit if line.sale_order_price_unit else '' , format_lines_13) 
                        sheet.merge_range(row,10,row + merge_line,10, line.sale_order_line_discount if line.sale_order_line_discount else '' , format_lines_13) 
                        sheet.merge_range(row,11,row + merge_line,11, line.sale_order_sell_unit_price if line.sale_order_sell_unit_price else '' , format_lines_13) 
                        sheet.merge_range(row,12,row + merge_line,12, line.sale_order_price_subtotal if line.sale_order_price_subtotal else '' , format_lines_13) 
                        
                        row += merge_line + 1
