from odoo import models , fields
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.report_purchase_order_for_part_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, list_purchase):
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
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11})
        format_text_wrap = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11,'text_wrap':True})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})

        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':10})
        format_address = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':10})
    
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':11,'color':'white','bold':True})
    
        format_lines_note = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':13,'bottom':1})
        
        sheet_name = "発注書(部材用)" 
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
        
        sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
        sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})
        
        langJP = False
        if self.env.user.lang == 'ja_JP':
            langJP = True
        
        for po in list_purchase[0]:
        #     # y,x
            sheet.write(1, 1, "発注書(部材用)" if langJP else 'Purchase Order(Components)', format_sheet_title)
            sheet.write(1, 3, po.purchase_order_company , format_sheet_partner)
            
        #     sheet.merge_range(2, 0,3,2,  po.dear_to if po.dear_to else '', format_name_company)
            sheet.write(3,0, "発注番号" if langJP else 'Order No', format_text) 
            

            sheet.write(6,0, "送り先着日" if langJP else 'Shipment Arrival Date' , format_text) 
            sheet.write(6,1, po.purchase_line_date_planned, format_text) 
            
            sheet.write(9,0, "送り先:" if langJP else 'Shipping Destination:', format_text) 
            sheet.merge_range(9,1,9,4, po.picking_type_id.warehouse_id.name, format_text_wrap) 
            sheet.write(10,0, "住所:" if langJP else 'Address:', format_text) 
            sheet.merge_range(10,1,10,4, po.purchase_order_address, format_text_wrap) 
            sheet.write(11,0, "TEL:", format_text) 
            sheet.merge_range(11,1,11,4, po.picking_type_id.warehouse_id.partner_id.phone if po.picking_type_id.warehouse_id.partner_id.phone else '', format_text_wrap) 

            sheet.write(9,5, "送り先注記:" if langJP else 'Shipping Notes:', format_address) 
            sheet.merge_range(9,6,11,8,po.destination_note if po.destination_note else '', format_note)
            
            sheet.write(11,11, "販売価格合計:" if langJP else 'Total sale amount:', format_text_right) 

            sheet.merge_range(0,11,0,12, po.purchase_order_current_date if po.purchase_order_current_date else '' , format_date )
            sheet.merge_range(3,11,8,12, po.purchase_order_hr_employee if po.purchase_order_hr_employee else '' , format_address) 

        #     #table title
            sheet.write(13, 0, "№" if langJP else 'No', format_table)
            sheet.merge_range(13,1,13,2, "品名" if langJP else 'Product Name', format_table)
            sheet.merge_range(13,3,13,6, "仕様・詳細" if langJP else 'Specifications/ Details', format_table)
            sheet.write(13,7, "数量" if langJP else 'Quantity', format_table)
            sheet.write(13,8, "", format_table)
            sheet.write(13,9, "単価 " if langJP else 'Unit Price', format_table)
            sheet.write(13,10, "発注金額" if langJP else 'Order Amount', format_table)
            sheet.merge_range(13,11,13,12, "Custom", format_table)
        
        allow_print = False
        if len(list_purchase) == 1:
            allow_print = True
        else: 
            list_partner_id =[]
            for list in list_purchase:
                list_partner_id.append(list.partner_id.id or '')

            if list_partner_id:
                for id in list_partner_id[1:]:
                    if id == list_partner_id[0]:
                        allow_print = True
                    else:
                        allow_print = False
                        break
        po_name = ""
        po_origin = ""
        po_amount_untaxed = 0
        row = 14
        if allow_print :
            for po in list_purchase:
                po_name += po.name + ', '
                po_origin += po.purchase_order_origin + ', '
                po_amount_untaxed += int(po.amount_untaxed)
                
                if po.order_line:
                    # merge_line = 3 
                    for ind,line in enumerate(po.order_line):
                        merge_line = 2 + len(line.product_id.product_template_attribute_value_ids) if len(line.product_id.product_template_attribute_value_ids) > 1 else 2
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
                            sheet.merge_range(row,7,row + merge_line,7, line.purchase_order_line_product_uom_qty if line.purchase_order_line_product_uom_qty else 0 , format_lines_13) 
                            sheet.merge_range(row,8,row + merge_line,8, '個' , format_lines_10) 
                            sheet.merge_range(row,9,row + merge_line,9, "{:,.0f}".format(line.purchase_order_sell_unit_price) if line.purchase_order_sell_unit_price else 0 , format_lines_13) 
                            sheet.merge_range(row,10,row + merge_line,10, "{:,.0f}".format(line.price_subtotal) if line.price_subtotal else 0 , format_lines_13) 
                            sheet.merge_range(row,11,row + merge_line,12, '' , format_lines_13) 

                            row += merge_line + 1
                            
            if "," in po_name:
                po_name = po_name.rstrip(', ')
            if "," in po_origin:   
                po_origin = po_origin.rstrip(', ')
                
        else:
            for po in list_purchase[0]:
                po_name += po.name if po.name else ""
                po_origin += po.origin if po.origin else ""
                po_amount_untaxed += int(po.amount_untaxed)

                if po.order_line:
                    # merge_line = 3 
                    for ind,line in enumerate(po.order_line):
                        merge_line = 2 + len(line.product_id.product_template_attribute_value_ids) if len(line.product_id.product_template_attribute_value_ids) > 1 else 2
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
                            sheet.merge_range(row,7,row + merge_line,7, line.purchase_order_line_product_uom_qty if line.purchase_order_line_product_uom_qty else 0 , format_lines_13) 
                            sheet.merge_range(row,8,row + merge_line,8, '個' , format_lines_10) 
                            sheet.merge_range(row,9,row + merge_line,9, "{:,.0f}".format(line.purchase_order_sell_unit_price) if line.purchase_order_sell_unit_price else 0 , format_lines_13) 
                            sheet.merge_range(row,10,row + merge_line,10, "{:,.0f}".format(line.price_subtotal) if line.price_subtotal else 0 , format_lines_13) 
                            sheet.merge_range(row,11,row + merge_line,12, '' , format_lines_13) 

                            row += merge_line + 1
                            
        sheet.set_header( f'{"&"}R {po_name if po_name else ""}', margin=margin_header)
        sheet.write(3,1, po_name if po_name else "", format_text)
        sheet.write(4,1, po_origin if po_name else "", format_text)
        sheet.write(11,12,"{:,.0f}".format(po_amount_untaxed), format_text_right)
        
