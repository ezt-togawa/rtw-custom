from odoo import models , fields
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO

class PurchaseOrderLineCustom(models.Model):
    _inherit = 'purchase.order.line'
    
    purchase_order_prod_name = fields.Char(compute = '_compute_purchase_order_prod_name')

    def _compute_purchase_order_prod_name(self):
        for record in self:
            if record.product_id.product_tmpl_id.config_ok:
                if record.product_id.product_tmpl_id.categ_id.name:
                    record.purchase_order_prod_name = record.product_id.product_tmpl_id.categ_id.name
                elif record.product_id.product_tmpl_id.product_no:
                    record.purchase_order_prod_name = record.product_id.product_tmpl_id.product_no
                else:
                    record.purchase_order_prod_name = record.name
            else:
                record.purchase_order_prod_name = record.name
            
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.report_purchase_order_for_part_xls'
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
        format_sheet_partner = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':16,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left','font_name': font_name,'font_size':14, 'text_wrap':True,'bottom':1})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_wrap = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11,'text_wrap':True})
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

        # #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet= workbook.add_worksheet(sheet_name)
            sheet_data= workbook.add_worksheet("data")
            sheet_data.hide()
            
            sheet.set_paper(9)  #A4
            sheet.set_landscape()
            sheet.set_print_scale(66)
            
            margin_header = 0.3
            margin_footer = 0.3
            left_margin = 0.8
            right_margin = 0.7
            top_margin = 0.5
            bottom_margin = 0.5
            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
            sheet.set_header( f'{"&"}R {so.name  if so.name else ""}', margin=margin_header) 
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)   

            sheet.set_column("A:A", width=17,cell_format=font_family)  
            sheet.set_column("B:B", width=20,cell_format=font_family)  
            sheet.set_column("C:C", width=18,cell_format=font_family)  

            sheet.set_column("D:D", width=16,cell_format=font_family)  

            sheet.set_column("E:E", width=10,cell_format=font_family)  
            sheet.set_column("F:F", width=14.5,cell_format=font_family)

            sheet.set_column("G:G", width=10,cell_format=font_family)  
            sheet.set_column("H:H", width=26,cell_format=font_family)  

            sheet.set_column("I:I", width=6.5,cell_format=font_family)  
            sheet.set_column("J:J", width=10,cell_format=font_family)  
            sheet.set_column("K:K", width=14.5,cell_format=font_family) 

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
            
        #     # y,x
            sheet.write(1, 1, "発注書(部材用)" if self.env.user.lang == 'ja_JP' else 'Purchase Order(Components)', format_sheet_title)
            sheet.write(1, 3, so.purchase_order_company , format_sheet_partner)
            
        #     sheet.merge_range(2, 0,3,2,  so.dear_to if so.dear_to else '', format_name_company)
            sheet.write(3,0, "発注番号" if self.env.user.lang == 'ja_JP' else 'Order No', format_text) 
            sheet.write(3,1, so.name, format_text) 
            sheet.write(4,1, so.purchase_order_origin, format_text) 

            sheet.write(6,0, "送り先着日" if self.env.user.lang == 'ja_JP' else 'Shipment Arrival Date' , format_text) 
            sheet.write(6,1, so.purchase_line_date_planned, format_text) 
            
            sheet.write(9,0, "送り先:" if self.env.user.lang == 'ja_JP' else 'Shipping Destination:', format_text) 
            sheet.merge_range(9,1,9,4, so.picking_type_id.warehouse_id.name, format_text_wrap) 
            sheet.write(10,0, "住所:" if self.env.user.lang == 'ja_JP' else 'Address:', format_text) 
            sheet.merge_range(10,1,10,4, so.purchase_order_address, format_text_wrap) 
            sheet.write(11,0, "TEL:", format_text) 
            sheet.merge_range(11,1,11,4, so.picking_type_id.warehouse_id.partner_id.phone if so.picking_type_id.warehouse_id.partner_id.phone else '', format_text_wrap) 

            sheet.write(10,5, "送り先注記:" if self.env.user.lang == 'ja_JP' else 'Shipping Notes:', format_address) 
            sheet.merge_range(9,6,11,8,so.destination_note if so.destination_note else '', format_note)
            
            sheet.write(11,11, "販売価格合計:" if self.env.user.lang == 'ja_JP' else 'Total sale amount:', format_text_right) 
            sheet.write(11,12,"{:,.0f}".format(so.amount_untaxed) if so.amount_untaxed else 0, format_text_right)

            sheet.merge_range(0,11,0,12, so.purchase_order_current_date if so.purchase_order_current_date else '' , format_date )
            sheet.merge_range(3,11,8,12, so.purchase_order_hr_employee if so.purchase_order_hr_employee else '' , format_address) 

        #     #table title
            sheet.write(13, 0, "№" if self.env.user.lang == 'ja_JP' else 'No', format_table)
            sheet.merge_range(13,1,13,2, "品名" if self.env.user.lang == 'ja_JP' else 'Product Name', format_table)
            sheet.merge_range(13,3,13,6, "仕様・詳細" if self.env.user.lang == 'ja_JP' else 'Specifications/ Details', format_table)
            sheet.write(13,7, "数量" if self.env.user.lang == 'ja_JP' else 'Quantity', format_table)
            sheet.write(13,8, "", format_table)
            sheet.write(13,9, "単価 " if self.env.user.lang == 'ja_JP' else 'Unit Price', format_table)
            sheet.write(13,10, "発注金額" if self.env.user.lang == 'ja_JP' else 'Order Amount', format_table)
            sheet.merge_range(13,11,13,12, "Custom", format_table)

            if so.order_line:
                row = 14
                merge_line = 6 
                for ind,line in enumerate(so.order_line):
                    
                    if line.display_type == 'line_note':
                        sheet.merge_range(row,0,row ,12, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                        sheet_data.write(ind,0, line.name if line.name else '', format_lines_note) 
                        row += 1
                    elif line.display_type == 'line_section':
                        sheet.merge_range(row,0,row ,12, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                        sheet_data.write(ind,1,line.name if line.name else '' , format_lines_section) 
                        row += 1
                    else:

                        sheet.merge_range(row,0,row + merge_line,0, line.purchase_order_index if line.purchase_order_index else '' , format_lines_10) 
                        sheet.merge_range(row,1,row + merge_line,2, line.purchase_order_prod_name if line.purchase_order_prod_name else '' , format_lines_11_left) 
                        sheet.merge_range(row,3,row + merge_line,6, line.purchase_order_product_detail if line.purchase_order_product_detail else '' , format_lines_10_left) 
                        sheet.merge_range(row,7,row + merge_line,7, line.purchase_order_line_product_uom_qty if line.purchase_order_line_product_uom_qty else 0 , format_lines_10) 
                        sheet.merge_range(row,8,row + merge_line,8, '個' , format_lines_10) 
                        sheet.merge_range(row,9,row + merge_line,9, "{:,.0f}".format(line.purchase_order_sell_unit_price) if line.purchase_order_sell_unit_price else 0 , format_lines_13) 
                        sheet.merge_range(row,10,row + merge_line,10, "{:,.0f}".format(line.price_subtotal) if line.price_subtotal else 0 , format_lines_13) 
                        sheet.merge_range(row,11,row + merge_line,12, '' , format_lines_13) 

                        row += merge_line + 1
