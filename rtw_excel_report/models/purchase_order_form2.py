from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO

class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.report_purchase_order2_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, so_data):
        self = self.with_context(lang=self.env.user.lang)             
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
        
        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_text_12_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':12})
        format_text_14 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_text_14_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':14})
        format_text_13_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':13})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})
        format_text_14_border = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14,'bottom':1})
        format_money_bgRed = workbook.add_format({'align': 'left','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})
        format_money_bgRed_right = workbook.add_format({'align': 'right','valign': 'vcenter','font_name': font_name,'font_size':14, 'text_wrap':True,'color':'white','bg_color':'#C00000'})

        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':10})
    
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
            # sheet.set_print_scale(63)
            
            margin_header = 0.3
            margin_footer = 0.3
            left_margin = 0.7
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
            sheet.set_column("H:H", width=7,cell_format=font_family)  

            sheet.set_column("I:I", width=9,cell_format=font_family)  
            sheet.set_column("J:J", width=14,cell_format=font_family)  
            sheet.set_column("K:K", width=6.5,cell_format=font_family) 

            sheet.set_column("L:L", width=14,cell_format=font_family) 
            sheet.set_column("M:M", width=0,cell_format=font_family) 
            sheet.set_column("N:N", width=13,cell_format=font_family) 
            sheet.set_column("O:O", width=1.6,cell_format=font_family) 
            sheet.set_column("P:Z", None,cell_format=font_family) 
            
            sheet.set_row(1, 46)
            sheet.set_row(2, 17)
            sheet.set_row(3, 17)
            sheet.set_row(5, 15)
            sheet.set_row(6, 15)
            sheet.set_row(7, 15)
            sheet.set_row(8, 15)
            sheet.set_row(9, 12)
            sheet.set_row(10, 15)
            sheet.set_row(11, 19)
            sheet.set_row(12, 24)
            sheet.set_row(13, 22)
            sheet.set_row(14, 26)
            sheet.set_row(15, 24)
            sheet.set_row(16,32)
            
            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            
            # y,x
            sheet.write(1, 1, _("定価注文書"), format_sheet_title) 
            
            sheet.write(2, 0, _("株式 会社リッツウェル"), format_text_14)
            sheet.write(3, 0, so.sale_order_ritzwell_staff if so.sale_order_ritzwell_staff else '', format_text_14)
            sheet.write(1, 10, _("海外")if so.overseas  else "", format_text_14_right) 

            sheet.write(5,0, _("下記の通り注文いたします。"), format_text) 
            
            sheet.write(7, 0, _("件名"), format_text_14_border) 
            sheet.write(10, 0, _("税抜合計"), format_text) 
            sheet.write(11, 0, _("消費税"), format_text) 
            sheet.write(12, 0, _("税込合計"), format_money_bgRed) 
            sheet.write(7, 1, so.title if so.title else '', format_text_14_border) 
            sheet.write(10, 1, so.sale_order_amount_untaxed if so.sale_order_amount_untaxed else '', format_text_13_right) 
            sheet.write(11, 1, so.sale_order_amount_tax if so.sale_order_amount_tax else '', format_text_12_right) 
            sheet.write(12, 1, so.sale_order_amount_total if so.sale_order_amount_total else '', format_money_bgRed_right) 

            sheet.write(5,4, _("納品希望日"), format_text_right) 
            sheet.write(6,4, _("納品場所"), format_text_right) 
            sheet.write(7,4, _("備考"), format_text_right) 
            
            sheet.write(5,6,so.sale_order_preferred_delivery_period if so.sale_order_preferred_delivery_period else '', format_text) 
            sheet.write(6,6, so.forwarding_address if so.forwarding_address else '', format_text) 
            sheet.merge_range(7,5,10,8,so.special_note[:115] if so.special_note else '', format_note) 

            sheet.write(0, 14, so.sale_order_current_date if so.sale_order_current_date else '' , format_date) 
            sheet.write(1, 13, _("西暦        年   月   日") , format_text_right) 
            if so.partner_id and so.partner_id.company_type == "company":
                sheet.write(3, 10, _("社名"), format_text) 
                sheet.write(5, 10, _("担当者名"), format_text) 
                sheet.write(6, 14, _("印"), format_text) 
            else:
                sheet.write(3, 10, _("氏名") , format_text) 
                
            sheet.write(4, 14, _("印"), format_text) 
            sheet.write(7, 10, _("納品先住所"), format_text) 
            sheet.write(9, 10, _("立会者"), format_text) 
            sheet.write(10, 10, _("立会者連絡先"), format_text) 
        
            sheet.write(12, 10, _("定価合計: ") + str( so.sale_order_total_list_price ) if so.sale_order_total_list_price else "", format_text_right) 
            sheet.write(12, 14, _("販売価格合計: ") + str(so.sale_order_amount_untaxed2) if so.sale_order_amount_untaxed2 else "" , format_text_right) 

            #table title
            sheet.write(14, 0, _("№"), format_table)
            sheet.write(14, 1, _("品名"), format_table)
            sheet.merge_range(14, 2,14,3, _("品番・サイズ"), format_table)
            sheet.merge_range(14, 4,14,6, _("仕様・詳細"), format_table)
            sheet.merge_range(14, 7,14, 9, _("仕様・詳細"), format_table)
            sheet.write(14,10, _("数量"), format_table)
            sheet.write(14, 11, _("定価"), format_table)
            sheet.merge_range(14, 12,14, 14, _("販売⾦額"), format_table)
            
            if so.order_line:       
                row = 15
                merge_line = 6 
                for ind,line in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                    
                    if line.display_type == 'line_note':
                        sheet.merge_range(row,0,row,14, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                        sheet_data.write(ind,0, line.name if line.name else '', format_lines_note) 
                        row += 1 
                    elif line.display_type == 'line_section':
                        sheet.merge_range(row,0,row,14, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                        sheet_data.write(ind,1,line.name if line.name else '' , format_lines_section) 
                        row += 1 
                    else:
                        sheet.merge_range(row,0,row + merge_line,0, line.sale_order_index if line.sale_order_index else '' , format_lines_10) 
                        sheet.merge_range(row,1,row + merge_line,1, line.sale_order_line_name_excel if line.sale_order_line_name_excel else '' , format_lines_9_left) 
                        
                        sheet.merge_range(row,2,row + merge_line,3, line.sale_order_number_and_size if line.sale_order_number_and_size else '' , format_lines_11_left) 
                        
                        sheet.merge_range(row,4,row + merge_line,6, line.sale_order_product_detail if line.sale_order_product_detail else '' , format_lines_10_left) 
                        sheet.merge_range(row,7,row + merge_line,9, line.sale_order_product_detail_2 if line.sale_order_product_detail_2 else '' , format_lines_10_left) 
                        
                        sheet.merge_range(row,10,row + merge_line,10, line.sale_order_line_product_uom_qty if line.sale_order_line_product_uom_qty else '' , format_lines_13) 
                        sheet.merge_range(row,11,row + merge_line,11, line.sale_order_price_unit if line.sale_order_price_unit else '' , format_lines_13) 
                        sheet.merge_range(row,12,row + merge_line,14, line.sale_order_amount_no_rate if line.sale_order_amount_no_rate else '' , format_lines_13) 
                        
                        row += merge_line + 1
                        