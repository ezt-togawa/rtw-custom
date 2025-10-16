from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.invoice_sale_order_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, so_data):
        self = self.with_context(lang=self.env.user.lang)             
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        def resize_keep_aspect(image_path, target_width):
            img = PILImage.open(image_path).convert('RGB')
            w, h = img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio)
            img = img.resize((target_width, target_height), PILImage.LANCZOS)
            return img

        def resize_with_fixed_height(img, height, new_width):
            w, h = img.size
            ratio = height / float(h)
            scaled_width = int(w * ratio)
            scaled_img = img.resize((scaled_width, height), PILImage.LANCZOS)
            final_img = scaled_img.resize((new_width, height), PILImage.LANCZOS)
            return final_img

        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'R_log.jpg')
        logo_R = resize_keep_aspect(image_logo_R, 86)
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        image_logo_ritzwell = get_module_resource('rtw_excel_report', 'img', 'Ritzwell_log.jpg')
        img_ritzwell = resize_keep_aspect(image_logo_ritzwell, 215)
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        image_signature_photo = get_module_resource('rtw_excel_report', 'img', 'signature_photo.png')
        img_signature = resize_keep_aspect(image_signature_photo, 215)
        img_io_signature = BytesIO()
        img_signature.save(img_io_signature, 'PNG')
        img_io_signature.seek(0)

        img_stamp_signature = PILImage.open(image_signature_photo)
        stamp_signature = resize_with_fixed_height(img_stamp_signature, 115, 105)
        stamp_signature_rgba = stamp_signature.convert('RGBA')
        alpha_signature = stamp_signature_rgba.split()[-1]
        alpha_signature = alpha_signature.point(lambda p: p * 0.3)
        stamp_signature_rgba.putalpha(alpha_signature)
        img_io_stamp_signature = BytesIO()
        stamp_signature_rgba.save(img_io_stamp_signature, 'PNG')
        img_io_stamp_signature.seek(0)
        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'text_wrap':True, 'bottom':1})
        format_text = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':11})
        format_text_2 = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':15})
        format_text_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':11})
        format_text_right_2 = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':11.25})
        format_text_12_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':12})
        format_text_13_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':13})
        format_note = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10})
        format_text_14_border = workbook.add_format({'align': 'left','font_name': font_name, 'font_size':14, 'bottom':1})
        format_money_bgRed = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':14, 'text_wrap':True, 'color':'white', 'bg_color':'#C00000'})
        format_money_bgRed_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':14, 'text_wrap':True, 'color':'white', 'bg_color':'#C00000'})
        format_date = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'num_format': 'yyyy-mm-dd', 'font_name': font_name, 'font_size':10})
        format_address = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10.5})
        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11, 'color':'white', 'bold':True})
        format_table_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11, 'color':'white', 'bold':True})
        format_lines_note = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11, 'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        format_lines_9_left= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11.25, 'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10, 'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})

        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet = workbook.add_worksheet(sheet_name)
            sheet_data = workbook.add_worksheet("data")
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
            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin, bottom=bottom_margin)
            sheet.set_header(f'{"&"}R No．{so.name if so.name else ""}', margin=margin_header) 
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)   

            sheet.set_column("A:A", width=13, cell_format=font_family)  
            sheet.set_column("B:B", width=20, cell_format=font_family)  
            sheet.set_column("C:C", width=18, cell_format=font_family)  

            sheet.set_column("D:D", width=16, cell_format=font_family)  

            sheet.set_column("E:E", width=10, cell_format=font_family)  
            sheet.set_column("F:F", width=10, cell_format=font_family)

            sheet.set_column("G:G", width=10, cell_format=font_family)  
            sheet.set_column("H:H", width=26, cell_format=font_family)  

            sheet.set_column("I:I", width=6.5, cell_format=font_family)  
            sheet.set_column("J:J", width=14.5, cell_format=font_family)  
            sheet.set_column("K:K", width=6.5, cell_format=font_family) 

            sheet.set_column("L:L", width=14.5, cell_format=font_family) 
            sheet.set_column("M:M", width=14.5, cell_format=font_family) 
            sheet.set_column("N:Z", None, cell_format=font_family) 
            
            sheet.set_row(1, 46)
            sheet.set_row(2, 17)
            sheet.set_row(3, 17)
            sheet.set_row(5, 15)
            sheet.set_row(6, 15)
            sheet.set_row(7, 15)
            sheet.set_row(8, 22)
            sheet.set_row(9, 16)
            sheet.set_row(10, 23)
            sheet.set_row(11, 21)
            sheet.set_row(12, 24)
            sheet.set_row(13, 16)
            sheet.set_row(14, 18)
            sheet.set_row(16, 32)
            
            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})
            sheet.insert_image(2, 10, "stamp", {'image_data': img_io_stamp_signature, 'x_offset': 160, 'y_offset': 0})
            
            # y,x
            sheet.write(1, 1, _("御請求書"), format_sheet_title) 
            sheet.merge_range(2, 0, 3, 2,  so.dear_to_invoice_sale if so.dear_to_invoice_sale else '', format_name_company)
            sheet.write(5, 0, _("平素より格別のお引き⽴てを賜り暑く御礼申し上げます。"), format_text) 
            sheet.write(6, 0, _("下記の通り、ご請求申し上げます。"), format_text) 
            sheet.write(8, 0, _("件名 : "), format_text_14_border) 
            sheet.write(10, 0, _("税抜合計"), format_text) 
            sheet.write(11, 0, _("消費税(10%)"), format_text)
            sheet.write(12, 0, _("税込合計"), format_money_bgRed) 
            sheet.write(8, 1, so.title if so.title else '', format_text_14_border) 
            sheet.write(10, 1, so.sale_order_amount_untaxed if so.sale_order_amount_untaxed else '', format_text_13_right) 
            sheet.write(11, 1, so.sale_order_amount_tax if so.sale_order_amount_tax else '', format_text_12_right) 
            sheet.write(12, 1, so.sale_order_amount_total if so.sale_order_amount_total else '', format_money_bgRed_right) 

            sheet.write(2, 5, _("お支払期限"), format_text_right_2) 
            sheet.write(3, 5, _("お支払内容"), format_text_right_2) 
            sheet.write(4, 5, _("お振込先"), format_text_right_2) 
            sheet.write(4, 6, so.sale_order_bank_name if so.sale_order_bank_name else '', format_text) 
            sheet.write(5, 6, so.sale_order_bank_branch if so.sale_order_bank_branch else '', format_text) 
            sheet.write(6, 6, so.sale_order_number_account if so.sale_order_number_account else '', format_text) 

            sheet.write(7, 5, _("納品日"), format_text_right_2) 
            sheet.write(8, 5, _("納品場所"), format_text_right_2) 
            sheet.write(9, 5, _("備考"), format_text_right_2) 

            sheet.write(2, 6, '', format_text) 
            sheet.write(3, 6, (so.payment_details or '') if so.payment_details else '', format_text) 

            sheet.write(7, 6, so.sale_order_preferred_delivery_date if so.sale_order_preferred_delivery_date else '', format_text) 
            sheet.write(8, 6, so.forwarding_address if so.forwarding_address else '', format_text) 
            sheet.merge_range(9, 6, 11, 8, so.sale_order_billing_notes[:120] if so.sale_order_billing_notes else '', format_note) 

            sheet.merge_range(0, 11, 0, 12, so.sale_order_current_date if so.sale_order_current_date else '', format_date) 
            sheet.merge_range(2, 11, 9, 12, so.sale_order_hr_employee_invoice if so.sale_order_hr_employee_invoice else '', format_address) 

            sheet.write(13, 9, _("定価合計: ") + str( so.sale_order_total_list_price ) if so.sale_order_total_list_price else "", format_text_right) 
            sheet.write(13, 12, _("販売価格合計: ") + str(so.sale_order_amount_untaxed2) if so.sale_order_amount_untaxed2 else '', format_text_right) 
            sheet.write(14, 12,so.sale_order_draff_invoice if so.sale_order_draff_invoice else '', format_text_13_right) 

            #table title
            sheet.write(16, 0, _("№"), format_table)
            sheet.merge_range(16, 1, 16, 3, _("品名"), format_table_left)
            sheet.merge_range(16, 4, 16, 7, _("品番・サイズ"), format_table_left)
            sheet.write(16, 8, _("数量"), format_table)
            sheet.write(16, 9, _("定価"), format_table)
            sheet.write(16, 10, _("掛率 "), format_table)
            sheet.write(16, 11, _("販売単価"), format_table)
            sheet.write(16, 12, _("販売⾦額"), format_table)

            if so.order_line:
                row = 17
                merge_line = 1
                for ind,line in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                    if line.display_type == 'line_note':
                        sheet.merge_range(row, 0, row , 12, "=data!A" + str(ind * 1 + 1), format_lines_note) 
                        sheet_data.write(ind, 0, line.name if line.name else '', format_lines_note) 
                        row += 1
                    elif line.display_type == 'line_section':
                        sheet.merge_range(row, 0, row , 12, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                        sheet_data.write(ind, 1, line.name if line.name else '', format_lines_section) 
                        row += 1
                    else:
                        sheet.merge_range(row, 0, row + merge_line, 0, line.sale_order_index if line.sale_order_index else '' , format_lines_10) 
                        sheet.merge_range(row, 1, row + merge_line, 3, line.sale_order_line_name_excel if line.sale_order_line_name_excel else '' , format_lines_9_left) 
                        sheet.merge_range(row, 4, row + merge_line, 7, line.sale_order_number_and_size if line.sale_order_number_and_size else '' , format_lines_11_left) 
                        sheet.merge_range(row, 8, row + merge_line, 8, line.sale_order_line_product_uom_qty if line.sale_order_line_product_uom_qty else '' , format_lines_13) 
                        sheet.merge_range(row, 9, row + merge_line, 9, line.sale_order_price_unit if line.sale_order_price_unit else '' , format_lines_13) 
                        sheet.merge_range(row, 10, row + merge_line, 10, line.sale_order_line_discount if line.sale_order_line_discount else '' , format_lines_13) 
                        sheet.merge_range(row, 11, row + merge_line, 11, '{:,.0f}'.format(line.sale_order_sell_unit_price) if line.sale_order_sell_unit_price else '' , format_lines_13) 
                        sheet.merge_range(row, 12, row + merge_line, 12, line.sale_order_price_subtotal if line.sale_order_price_subtotal else '' , format_lines_13) 
                        
                        row += merge_line + 1
