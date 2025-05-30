from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO

class StockPickingDelivery(models.AbstractModel):
    _name = 'report.rtw_excel_report.stock_picking_delivery_xls'
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
        img_ritzwell = img_ritzwell.resize((234, 40))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'bottom','font_size':18,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'right','font_name': font_name,'font_size':14, 'text_wrap':True})
        format_tel_fax = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_12 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':12})
        format_text_13 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13})
        format_text_14 = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14})
        format_note = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10})

        format_address = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':11})
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#808080', 'font_name': font_name,'font_size':14,'color':'white','bold':True})
        
        format_lines_14_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':14,'bottom':1})
        format_lines_14 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':14,'bottom':1})

        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet= workbook.add_worksheet(sheet_name)
            sheet_data= workbook.add_worksheet("data")
            sheet_data.hide()
            
            sheet.set_paper(9)  #A4
            sheet.set_landscape()
            sheet.set_print_scale(72)
            
            margin_header = 0.3
            margin_footer = 0.3
            left_margin = 0.4
            right_margin = 0.4
            top_margin = 0.6
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
            sheet.set_column("C:C", width=20,cell_format=font_family)  
            sheet.set_column("D:D", width=2,cell_format=font_family)  
            sheet.set_column("E:E", width=15,cell_format=font_family)  
            sheet.set_column("F:F", width=15,cell_format=font_family)
            sheet.set_column("G:G", width=12,cell_format=font_family)  
            sheet.set_column("H:H", width=0,cell_format=font_family)  
            sheet.set_column("I:I", width=8,cell_format=font_family)  
            sheet.set_column("J:J", width=8,cell_format=font_family)  
            sheet.set_column("K:K", width=8,cell_format=font_family) 
            sheet.set_column("L:L", width=8,cell_format=font_family) 
            sheet.set_column("M:M", width=8,cell_format=font_family) 
            sheet.set_column("N:N", width=8, cell_format=font_family) 
            sheet.set_column("O:O", width=24, cell_format=font_family) 
            sheet.set_column("P:Z", None, cell_format=font_family) 
            
            sheet.set_row(1, 35)
            sheet.set_row(2, 17)
            sheet.set_row(3, 17)
            sheet.set_row(5, 15)
            sheet.set_row(6, 15)
            sheet.set_row(7, 15)
            sheet.set_row(8, 14)
            sheet.set_row(9, 12)
            sheet.set_row(14, 7)
            sheet.set_row(15, 0)
            sheet.set_row(16, 0)
            sheet.set_row(17, 0)
            sheet.set_row(18, 0)
            sheet.set_row(19, 0)
            sheet.set_row(20,32)
            
            sheet.insert_image(0, 0, "logo", {'image_data': img_io_R})
            sheet.insert_image(1, 13, "logo2", {'image_data': img_io_ritzwell, 'y_offset': 2})
            
            # y,x
            sheet.write(1, 1, _("配送依頼書"), format_sheet_title) 
            
            sheet.merge_range(1, 2, 1, 3, so.sale_orders.dear_to_delivery if so.sale_orders.dear_to_delivery else '', format_name_company)
            sheet.write(1, 4, "  " + so.sale_orders.send_to_tel_fax if so.sale_orders.send_to_tel_fax else '', format_tel_fax)

            sheet.write(2, 0,  _("発注番号"), format_text) 
            sheet.write(2, 1, so.sale_id.name if so.sale_id.name else "", format_text_13) 
            sheet.write(3, 0, _("入荷日"), format_text) 
            sheet.write(3, 1, str(so.sale_id.sale_order_warehouse_arrive_date) if so.sale_id.sale_order_warehouse_arrive_date else "", format_text_13) 
            
            sheet.write(5, 0, _("搬入設置日"), format_text_12) 
            sheet.write(5, 1, str(so.sale_id.sale_order_preferred_delivery_date) if so.sale_id.sale_order_preferred_delivery_date else "", format_text_12) 
            sheet.write(6, 0, _("時間"), format_text_12) 
            sheet.write(6, 1, so.sale_id.time_text if so.sale_id.time_text else "", format_text_12) 
            
            sheet.write(8, 0, _("お届け先（物件名）"), format_text_12) 
            sheet.write(8, 1, so.sale_id.title if so.sale_id.title else "", format_text) 
            sheet.write(9, 1,  so.sale_orders.sale_order_partner_info if so.sale_orders.sale_order_partner_info else "", format_text) 
            
            sheet.write(11, 0, _("郵便番号："), format_text_14) 
            sheet.write(11, 1, ("〒 " + so.forwarding_address_zip )if so.forwarding_address_zip else "", format_text_14) 
            
            sheet.write(11, 4, _("備考："), format_text) 
            sheet.merge_range(11, 5,13, 8,so.sale_id.sale_order_shipping_notes[:120] if so.sale_id.sale_order_shipping_notes else "", format_note)

            sheet.write(12, 0, _("住    所："), format_text_14) 
            sheet.write(12, 1, ("〒 " + so.forwarding_address )if so.forwarding_address else "", format_text_14) 
            
            sheet.write(12, 12, "搬入費用：", format_text_12) 
            
            sheet.write(13, 0, _("立 会 人："), format_text_14) 
            sheet.write(13, 1, so.stock_picking_witness_name_phone if so.stock_picking_witness_name_phone else "", format_text_14) 
            
            sheet.merge_range(2, 13, 8, 14, so.sale_id.sale_order_hr_employee if so.sale_id.sale_order_hr_employee else '' , format_address) 
            
            #table title
            sheet.write(20, 0, _("№"), format_table)
            sheet.merge_range(20, 1, 20, 3,  _("品名"), format_table)
            sheet.merge_range(20, 4, 20, 8, _("品番・サイズ"), format_table)
            sheet.write(20, 9, _("数量"), format_table)
            sheet.write(20, 10, _("個口数"), format_table)
            sheet.write(20, 11, _("才数"), format_table)
            # sheet.write(20, 11, _("取説"), format_table)
            sheet.write(20, 12, _("開梱 "), format_table)
            sheet.write(20, 13, _("組立"), format_table)
            sheet.write(20, 14, _("備考"), format_table)

            if so.stock_move:
                row = 21

                for ind,line in enumerate(so.stock_move):
                    merge_line = 5
                    sheet.merge_range(row, 0, row + merge_line, 0, line.stock_index if line.stock_index else '' , format_lines_14) 
                    sheet.merge_range(row, 1, row + merge_line, 3, line.stock_move_line_name_excel if line.stock_move_line_name_excel else '', format_lines_14_left) 
                    sheet.merge_range(row, 4, row + merge_line, 8, line.product_number_and_size if line.product_number_and_size else '', format_lines_14_left) 
                    sheet.merge_range(row, 9, row + merge_line, 9, line.stock_product_uom_qty if line.stock_product_uom_qty else '', format_lines_14) 
                    sheet.merge_range(row, 10, row + merge_line, 10, line.prod_package_qty if line.prod_package_qty else '', format_lines_14) 
                    sheet.merge_range(row, 11, row + merge_line, 11, '{0:,.0f}'.format(line.product_id.sai) if line.product_id.sai else '', format_lines_14) 
                    # sheet.merge_range(row, 11, row + merge_line, 11, _('有') if line.combined_shipment else '', format_lines_14) 
                    sheet.merge_range(row, 12, row + merge_line, 12, _('有'), format_lines_14) 
                    sheet.merge_range(row, 13, row + merge_line, 13, _('無'), format_lines_14) 
                    sheet.merge_range(row, 14, row + merge_line, 14, '', format_lines_14) 
                    
                    row += merge_line + 1
                