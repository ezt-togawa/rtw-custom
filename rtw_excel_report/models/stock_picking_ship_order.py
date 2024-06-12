from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO

class StockPickingShipOrder(models.AbstractModel):
    _name = 'report.rtw_excel_report.stock_picking_ship_order_xls'
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
        format_money = workbook.add_format({'align': 'left','valign': 'center', 'font_name': font_name,'font_size':13})
    
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
            if so.sale_id.name:
                header_parts.append(so.sale_id.name)
            if so.sale_id.sale_order_current_date:
                header_parts.append('\n '+ so.sale_id.sale_order_current_date)
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
            sheet.set_column("H:H", width=0,cell_format=font_family)  

            sheet.set_column("I:I", width=10,cell_format=font_family)  
            sheet.set_column("J:J", width=10,cell_format=font_family)  
            sheet.set_column("K:K", width=10,cell_format=font_family) 

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
            sheet.set_row(16, 0)
            sheet.set_row(17, 0)
            sheet.set_row(18, 0)
            sheet.set_row(19, 0)
            sheet.set_row(20,32)
            
            sheet.insert_image(0, 0, "logo", {'image_data': img_io_R})
            sheet.insert_image(1, 12, "logo2", {'image_data': img_io_ritzwell, 'y_offset': 2})
            
            # y,x
            sheet.write(1, 1, _("出荷依頼書"), format_sheet_title) 
            
            send_to = ""
            company = ""
            if so.sale_id and so.sale_id.partner_id and so.sale_id.partner_id.commercial_company_name:
                company = so.sale_id.partner_id.parent_id.name
            elif so.sale_id.partner_id.name:
                company = so.sale_id.partner_id.name
                    
            if so.lang_code == "en_US":
                if company:
                    send_to += _("御中 ") + company + _(" 株式会社" )
            else:
                if company:
                    send_to += _("株式会社 ") + company + _(" 御中")
                    
            sheet.write(1, 2, send_to, format_name_company)
            
            sheet.write(2, 0,  _("発注番号"), format_text) 
            sheet.write(2, 1, so.sale_id.name if so.sale_id.name else "", format_text_14) 
            
            sheet.write(4,0, _("出荷日"), format_text) 
            sheet.write(5,0, _("送り先着日"), format_text) 
            sheet.write(6,0, _("配送手段"), format_text) 
            sheet.write(4,1, so.stock_estimated_shipping_date if so.stock_estimated_shipping_date else "", format_text_12) 
            sheet.write(5,1, so.stock_scheduled_date if so.stock_scheduled_date else "", format_text_12) 
            sheet.write(6,1, _("定期便"), format_text_12) 
            
            sheet.write(8, 0, _("物件名"), format_text_12) 
            sheet.write(8, 1, so.sale_id.title if so.sale_id.title else "", format_text) 
            sheet.write(9, 1, so.stock_picking_partner_info if so.stock_picking_partner_info else "", format_text) 
            
            sheet.write(10, 0, _("送り先"), format_text) 
            sheet.write(10, 1, so.sale_id.partner_id.commercial_company_name if so.sale_id.partner_id.commercial_company_name else "", format_text) 
            
            sheet.write(11, 0, _("住所"), format_text) 
            sheet.write(12, 0, _("TEL／携帯"), format_text)
            sheet.write(11, 1, so.stock_picking_partner_address if so.stock_picking_partner_address else "", format_text) 
            phone = ""
            if so.sale_id.partner_id.phone and so.sale_id.partner_id.mobile:
                phone += so.sale_id.partner_id.phone + "/" + so.sale_id.partner_id.mobile
            elif so.sale_id.partner_id.phone:
                phone += so.sale_id.partner_id.phone
            elif so.sale_id.partner_id.mobile:
                phone += so.sale_id.partner_id.mobile
            sheet.write(12, 1, phone, format_text) 
        
            sheet.write(10,10, _("送り状注記"), format_text) 
            sheet.merge_range(11,10,13,13,so.note[:120] if so.note else '', format_note) 
            
            sheet.merge_range(2,12,8,13, so.sale_id.sale_order_hr_employee if so.sale_id.sale_order_hr_employee else '' , format_address) 
            
            sheet.write(14,13, so.sale_id.sale_order_amount_untaxed if so.sale_id.sale_order_amount_untaxed else '' , format_money) 
            sheet.write(14,11, _('販売価格合計') , format_money) 

            #table title
            sheet.write(20, 0, _("№"), format_table)
            sheet.write(20, 1, _("品名"), format_table)
            sheet.merge_range(20, 2,20,3, _("品番・サイズ"), format_table)
            sheet.merge_range(20, 4,20,6, _("仕様・詳細"), format_table)
            sheet.write(20,8, _("数量"), format_table)
            sheet.write(20, 9, _("個口数"), format_table)
            sheet.write(20, 10, _("才数"), format_table)
            sheet.merge_range(20, 11,20, 12, _("入荷元 "), format_table)
            sheet.write(20, 13, _("白谷着日"), format_table)

            if so.stock_move:
                row = 21
                for ind,line in enumerate(so.stock_move):
                    merge_line = 2 + len(line.product_id.product_template_attribute_value_ids) if len(line.product_id.product_template_attribute_value_ids) > 1 else 2

                    sheet.merge_range(row, 0, row + merge_line, 0, line.stock_index if line.stock_index else '' , format_lines_10) 
                    sheet.merge_range(row, 1, row + merge_line, 1, line.product_name if line.product_name else '', format_lines_9_left) 
                    
                    sheet.merge_range(row, 2, row + merge_line, 3, line.product_number_and_size if line.product_number_and_size else '', format_lines_11_left) 
                    
                    sheet.merge_range(row, 4, row + merge_line, 6, line.product_attribute if line.product_attribute else '', format_lines_10_left) 
                    
                    sheet.merge_range(row, 8, row + merge_line, 8, line.stock_product_uom_qty if line.stock_product_uom_qty else '', format_lines_13) 
                    sheet.merge_range(row, 9, row + merge_line, 9, '{0:,.0f}'.format(line.product_package_quantity)if line.product_package_quantity else 0, format_lines_13) 
                    
                    sheet.merge_range(row, 10, row + merge_line, 10, line.stock_sai if line.stock_sai else '', format_lines_13) 
                    sheet.merge_range(row, 11, row + merge_line, 12, line.stock_warehouse if line.stock_warehouse else '', format_lines_13) 
                    sheet.merge_range(row, 13, row + merge_line, 13, line.stock_shiratani_date if line.stock_shiratani_date else '', format_lines_13) 
                    
                    row += merge_line + 1
