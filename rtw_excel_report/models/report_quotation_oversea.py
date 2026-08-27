from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO

class ReportMrpExcel(models.AbstractModel):
    """
        【御見積書（海外）】Excelレポート出力ロジック
        レポートID: rtw_excel_report.report_quotation_oversea_xls
        用途: 販売オーダーより注文書のExcelを作成する
    """
    _name = 'report.rtw_excel_report.report_quotation_oversea_xls'
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

        # 通貨処理
        currency = so_data[0].currency_id
        symbol = currency.symbol or ''
        decimal_places = currency.decimal_places
        num_format_with_symbol = f'"{symbol}"#,##0'
        if decimal_places > 0:
            num_format_with_symbol += '.' + ('0' * decimal_places)
        num_format_no_symbol = '#,##0'
        if decimal_places > 0:
            num_format_no_symbol += '.' + ('0' * decimal_places)
        num_format_trailing_0 = 'General'  # [#,##0.###]指定だと整数の場合ドットが残ってしまうので、カンマ編集を捨ててドットを消す

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'shrink':1, 'bottom':1})
        format_name_company_no_border = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'shrink':1})
        format_name_people = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'shrink':1, 'bottom':1})
        format_text = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':11})
        format_text_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':11.25})
        format_text_right_2 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':11})
        format_text_12_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':12})
        format_text_12_right.set_num_format(num_format_with_symbol)
        format_text_13_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':13})
        format_text_13_right.set_num_format(num_format_with_symbol)
        format_note = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10})
        format_text_14_border = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'shrink':1, 'bottom':1})
        format_money_bgRed = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':16, 'text_wrap':True, 'color':'white','bg_color':'#C00000', 'bold':True})
        format_money_bgRed_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':16, 'text_wrap':True, 'color':'white','bg_color':'#C00000', 'bold':True})
        format_money_bgRed_right.set_num_format(num_format_with_symbol)

        format_date = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'num_format': 'yyyy-mm-dd', 'font_name': font_name, 'font_size':10})
        format_address = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True,  'font_name': font_name, 'font_size':10.5})
    
        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11,'color':'white','bold':True})
        format_table_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11,'color':'white','bold':True})
        format_table_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11,'color':'white','bold':True})

        format_lines_note = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11,'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11,'bg_color':'#e9ecef','bottom':1})

        format_lines_9_left= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11.25,'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':10,'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1})
        format_lines_13.set_num_format(num_format_no_symbol)
        format_lines_14 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1})
        format_lines_14.set_num_format(num_format_trailing_0)

        # 改ページ直後の明細1行目は、直前(前ページ側)の明細の下線を頼りに区切り線を出せないため上罫線を追加
        format_lines_note_top = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11,'bottom':1,'top':1})
        format_lines_section_top = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11,'bg_color':'#e9ecef','bottom':1,'top':1})
        format_lines_9_left_top = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11.25,'bottom':1,'top':1})
        format_lines_10_top = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1,'top':1})
        format_lines_11_left_top = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1,'top':1})
        format_lines_13_top = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1,'top':1})
        format_lines_13_top.set_num_format(num_format_no_symbol)
        format_lines_14_top = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12,'bottom':1,'top':1})
        format_lines_14_top.set_num_format(num_format_trailing_0)

        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet= workbook.add_worksheet(sheet_name)
            sheet_data= workbook.add_worksheet("data")
            sheet_data.hide()
            
            sheet.set_paper(9)  #A4
            sheet.set_landscape()
            sheet.hide_gridlines(2)
            # sheet.set_print_scale(63)

            margin_header = 0.08
            margin_footer = 0.12
            left_margin = 0.2
            right_margin = 0.2
            top_margin = 0.2
            bottom_margin = 0.2
            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
            sheet.set_header(f'{"&"}R No．{so.name if so.name else ""}', margin=margin_header)
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)
            note = '※商品の詳細は仕様書を参照ください'
            footer_text = f'&L&P/&N&R&"MS UI Gothic,Regular"&12 {note}'
            sheet.set_footer(footer_text, margin=margin_footer)

            sheet.fit_to_pages(1, 0)
            sheet.center_horizontally()

            sheet.set_column("A:A", width=14,cell_format=font_family)
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
            sheet.set_row(4, 17)
            sheet.set_row(5, 17)
            sheet.set_row(6, 17)
            sheet.set_row(7, 17)
            sheet.set_row(8, 17)
            sheet.set_row(9, 17)
            sheet.set_row(10, 22)
            sheet.set_row(11, 22)
            sheet.set_row(12, 26)
            sheet.set_row(13, 22)
            sheet.set_row(15, 32)

            name_title_end_col = 2  # 宛名・件名の縮小/下線を揃える幅(全角19文字くらい相当)

            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})

            # y,x
            sheet.write(1, 1, _("御見積書"), format_sheet_title)
            if so.send_to_company and so.send_to_people:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_company, format_name_company_no_border)
                sheet.merge_range(3, 0, 3, name_title_end_col, so.send_to_people, format_name_people)
            elif so.send_to_company:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_company, format_name_company)
            elif so.send_to_people:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_people, format_name_people)

            sheet.write(5,0, _("平素より格別のお引き立てを賜り厚く御礼申し上げます。"), format_text)
            sheet.write(6,0, _("御依頼の件、下記の通りお見積り致しました。ご査収の程宜しくお願い致します。"), format_text)
            sheet.merge_range(8, 0, 8, name_title_end_col, (_("件名 : ") + so.title) if so.title else '', format_text_14_border)
            sheet.write(10, 0, _("税抜合計"), format_text)
            sheet.write(11, 0, _("消費税"), format_text)
            sheet.write(12, 0, _("税込合計"), format_money_bgRed)
            sheet.write(10, 1, so.amount_untaxed, format_text_13_right)
            sheet.write(11, 1, so.amount_tax, format_text_12_right)
            sheet.write(12, 1, so.amount_total, format_money_bgRed_right)

            sheet.write(2,5, _("納品希望日："), format_text_right)
            sheet.write(3,5, _("製作日数："), format_text_right)
            sheet.write(4,5, _("発注期限："), format_text_right)
            sheet.write(5,5, _("納品場所："), format_text_right)
            sheet.write(6,5, _("支払方法："), format_text_right)
            sheet.write(8,5, _("見積有効期限："), format_text_right)
            sheet.write(9,5, _("備考："), format_text_right)

            sheet.write(2,6, so.preferred_delivery_period if so.preferred_delivery_period else '', format_text)
            sheet.write(3,6, so.workday_id.name if so.workday_id else '', format_text)
            sheet.write(4,6, so.sale_order_date_deadline if so.sale_order_date_deadline else '', format_text)
            sheet.write(5,6, so.forwarding_address if so.forwarding_address else '', format_text)
            sheet.write(6,6,so.sale_order_transactions_term if so.sale_order_transactions_term else '', format_text)
            sheet.write(8,6, so.sale_order_validity_date if so.sale_order_validity_date else '', format_text)
            sheet.merge_range(9,6,12,8,so.sale_order_special_note if so.sale_order_special_note else '', format_note)

            sheet.merge_range(0,11,0,12, so.sale_order_current_date if so.sale_order_current_date else '' , format_date)
            sheet.merge_range(2,11,9,12, so.sale_order_hr_employee_split_street if so.sale_order_hr_employee_split_street else '' , format_address)

            sheet.write(13, 0, _("税抜定価合計 "), format_text)
            # if so.currency_id.symbol and so.sale_order_total_list_price:
            #     total_list_price = so.currency_id.symbol + str(so.sale_order_total_list_price)
            #     sheet.write(13, 1, total_list_price, format_text_12_right)
            sheet.write(13, 1, so.sale_order_total_list_price, format_text_12_right)

            sheet.write(13, 12, _("消費税は含まれておりません"), format_text_12_right)

            #table title
            sheet.write(15, 0, _("№"), format_table)
            sheet.merge_range(15, 1, 15, 3, _("品名"), format_table_left)
            sheet.merge_range(15, 4, 15, 7, _("品番・サイズ"), format_table_left)
            sheet.write(15, 8, _("数量"), format_table_right)
            sheet.write(15, 9, _("定価　"), format_table_right)
            sheet.write(15, 10, _("掛率"), format_table_right)
            sheet.write(15, 11, _("販売単価"), format_table_right)
            sheet.write(15, 12, _("販売金額"), format_table_right)

            sheet.print_area('A1:M16')

            if so.order_line:
                row = 16
                merge_line = 1

                # 改ページ位置(0-indexed行)は実際の印刷結果から特定した固定値(report_quotation.pyと同じ明細開始行のため同一値を使用)。
                # Excel41行目(0-idx 40)からページ2、85行目(0-idx 84)からページ3が始まる。
                # 3ページ目以降は明細行のみが続くため、ページ2→3の行数間隔(44行)をそのまま踏襲する。
                FIRST_PAGE_BREAK_ROW = 40
                SECOND_PAGE_BREAK_ROW = 84
                PAGE_BREAK_INTERVAL = SECOND_PAGE_BREAK_ROW - FIRST_PAGE_BREAK_ROW

                next_break_row = FIRST_PAGE_BREAK_ROW
                pagebreak_positions = []

                for ind,line in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                    line_span = 1 if line.display_type in ('line_note', 'line_section') else merge_line + 1

                    is_first_of_new_page = row >= next_break_row
                    if is_first_of_new_page:
                        pagebreak_positions.append(row)
                        next_break_row = (
                            SECOND_PAGE_BREAK_ROW if next_break_row == FIRST_PAGE_BREAK_ROW
                            else next_break_row + PAGE_BREAK_INTERVAL
                        )

                    if line.display_type == 'line_note':
                        fmt_note = format_lines_note_top if is_first_of_new_page else format_lines_note
                        sheet.set_row(row, 18)
                        sheet.merge_range(row,0,row ,12, "=data!A" + str(ind * 1 + 1) , fmt_note)
                        sheet_data.write(ind,0, line.name if line.name else '', fmt_note)
                    elif line.display_type == 'line_section':
                        fmt_section = format_lines_section_top if is_first_of_new_page else format_lines_section
                        sheet.set_row(row, 18)
                        sheet.merge_range(row,0,row ,12, "=data!B" + str(ind * 1 + 1) , fmt_section)
                        sheet_data.write(ind,1,line.name if line.name else '' , fmt_section)
                    else:
                        fmt_10 = format_lines_10_top if is_first_of_new_page else format_lines_10
                        fmt_9_left = format_lines_9_left_top if is_first_of_new_page else format_lines_9_left
                        fmt_11_left = format_lines_11_left_top if is_first_of_new_page else format_lines_11_left
                        fmt_13 = format_lines_13_top if is_first_of_new_page else format_lines_13
                        fmt_14 = format_lines_14_top if is_first_of_new_page else format_lines_14
                        sheet.set_row(row, 18)
                        sheet.set_row(row + merge_line, 18)
                        sheet.merge_range(row, 0, row + merge_line, 0, line.sale_order_index or '', fmt_10)
                        sheet.merge_range(row, 1, row + merge_line, 3, line.sale_order_line_name_excel or '', fmt_9_left)
                        sheet.merge_range(row, 4, row + merge_line, 7, line.sale_order_number_and_size or '', fmt_11_left)
                        if line.is_tax_excluded_product:
                            sheet.merge_range(row, 8, row + merge_line, 8, '', fmt_13)
                            sheet.merge_range(row, 9, row + merge_line, 9, '', fmt_13)
                            sheet.merge_range(row, 10, row + merge_line, 10, '', fmt_13)
                            sheet.merge_range(row, 11, row + merge_line, 11, '', fmt_13)
                        else:
                            sheet.merge_range(row, 8, row + merge_line, 8, line.product_uom_qty or 0, fmt_14)
                            sheet.merge_range(row, 9, row + merge_line, 9, line.price_unit or 0, fmt_13)
                            sheet.merge_range(row, 10, row + merge_line, 10, line.call_rate or 0, fmt_14)
                            sheet.merge_range(row, 11, row + merge_line, 11, line.price_reduce or 0, fmt_13)
                        sheet.merge_range(row, 12, row + merge_line, 12, line.price_subtotal or 0, fmt_13)

                    row += line_span

                if row > 16:
                    last_content_row = row - 1
                    sheet.print_area(f'A1:M{last_content_row + 1}')
                    if pagebreak_positions:
                        sheet.set_h_pagebreaks(pagebreak_positions)

            #  Prescription
            sheet_prescription= workbook.add_worksheet("Prescription")
            sheet_prescription.set_paper(9)  #A4
            sheet_prescription.set_portrait()
            sheet_prescription.hide_gridlines(2)
            sheet_prescription.set_margins(left=0.2, right=0.2, top=0.2, bottom=0.2)
            sheet_prescription.fit_to_pages(1, 0)
            sheet_prescription.center_horizontally()
            sheet_prescription.print_area('A1:L26')

            border_default = workbook.add_format({'top':1,'left':1,'right':1})
            border_left = workbook.add_format({'left':1,'bottom':1})
            border_right = workbook.add_format({'right':1,'bottom':1})
            address_web = workbook.add_format({'align': 'center','valign': 'vcenter', 'font_name': font_name,'font_size':14,'underline':1})
            address_office_title = workbook.add_format({'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':12,'bold':True})
            address_office_title2 = workbook.add_format({'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':12,'bold':True,'bottom':1})
            address_office = workbook.add_format({'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':9})
            
            prescrip_note =  workbook.add_format({'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':12,'bold':True})
            prescrip_note_detail = workbook.add_format({'text_wrap':True,'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':9})
            sale_condition = workbook.add_format({'text_wrap':True,'align': 'center','valign': 'vcenter', 'font_name': font_name,'font_size':9})
            sale_condition_detail = workbook.add_format({'text_wrap':True,'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':8})
            # 最終行(Governing Law)の下線用
            sale_condition_bottom = workbook.add_format({'text_wrap':True,'align': 'center','valign': 'vcenter', 'font_name': font_name,'font_size':9,'bottom':1})
            sale_condition_detail_bottom = workbook.add_format({'text_wrap':True,'align': 'left','valign': 'vcenter', 'font_name': font_name,'font_size':8,'bottom':1})
            border_bottom_only = workbook.add_format({'bottom':1})
            
            sheet_prescription.set_row(0, 3)
            sheet_prescription.set_column("A:A", width=0.5,cell_format=font_family)  
            sheet_prescription.set_column("B:B", width=3,cell_format=font_family)  
            sheet_prescription.set_column("C:C", width=5.5,cell_format=font_family)  
            sheet_prescription.set_column("D:K", width=13,cell_format=font_family)  
            sheet_prescription.set_column("L:L", width=3,cell_format=font_family) 
            
            sheet_prescription.write(6, 2, "MAIN OFFICE", address_office_title)
            sheet_prescription.write(7, 2, so.prescription_company_name if so.prescription_company_name else '', address_office)
            sheet_prescription.write(8, 2,so.prescription_address_info if so.prescription_address_info else '', address_office)
            sheet_prescription.write(9, 2, so.prescription_address_country if so.prescription_address_country else '', address_office)
            sheet_prescription.write(10, 2, so.prescription_tel_fax if so.prescription_tel_fax else '', address_office)
            sheet_prescription.write(11, 2, so.prescription_email if so.prescription_email else '', address_office)
            
            sheet_prescription.merge_range(14, 2,14,10, "SALES TERMS AND CONDITIONS", address_office_title2)
            sheet_prescription.write(15, 3, "Cancellation", sale_condition)
            sheet_prescription.write(16, 3, "Packing", sale_condition)
            sheet_prescription.write(17, 3, "Shipment", sale_condition)
            sheet_prescription.write(18, 3, "Inspection", sale_condition)
            sheet_prescription.write(19, 3, "Patents", sale_condition)
            sheet_prescription.write(20, 3, "Warranty", sale_condition)
            sheet_prescription.write(21, 3, "Claim", sale_condition)
            sheet_prescription.write(22, 3, "Force Majeure", sale_condition)
            sheet_prescription.write(23, 3, "Arbitration", sale_condition)
            sheet_prescription.write(24, 3, "Trade Terms", sale_condition)
            sheet_prescription.write(25, 2, "", border_bottom_only)
            sheet_prescription.write(25, 3, "Governing Law", sale_condition_bottom)
            
            sheet_prescription.merge_range(15, 4, 15,10,"Buyer’s cancellation or changes in specifications after confirmation of receipt of order will incur a fifty (50) percent cancellation fee." + "\n" + "  Orders for built-to-order and custom-tailored products cannot be cancelled.", sale_condition_detail)
            sheet_prescription.merge_range(16, 4, 16,10,"The make-up, packing, packaging and marking shall be at Seller’s option.", sale_condition_detail)
            sheet_prescription.merge_range(17, 4, 17,10,"The date of a bill of landing shall be accepted as the conclusive date of shipment. Any shipment made within fifteen (15) days after date specified for shipment shall be deemed as a contracted delivery. Partial shipment and / or transshipment shall be permitted and, in such case, each shipment shall be considered as a separate contract.", sale_condition_detail)
            sheet_prescription.merge_range(18, 4, 18,10,"Seller shall, before shipment, make inspection of the goods especially in respect of specification, quality and condition of the goods. Unless otherwise arranged, the inspection by Seller shall be final in all respects regarding the goods.", sale_condition_detail)
            sheet_prescription.merge_range(19, 4, 19,10,"Buyer shall hold Seller harmless from liability, loss or expense in connection with any alleged infringement with regard to any patent, trademark, copyright, design, pattern, etc., in any country.", sale_condition_detail)
            sheet_prescription.merge_range(20, 4, 20,10,"Seller warrants that the goods are free from any defects of design, material and workmanship and conform to its specifications. Once after having delivered the goods to Buyer, Buyer is responsible to give all dealers and customers necessary or adequate instructions for proper use of the goods and prevention of misuse thereof.", sale_condition_detail)
            sheet_prescription.merge_range(21, 4, 21,10,"Buyer’s claim of whatever nature arising under the contract shall be notified to Seller by email or fax within seven (7) days after arrival of the goods at the destination specified in the bills of lading. Full particulars of such claim, together with sworn surveyor’s report shall be made in writing and forwarded by registered airmail within fifteen (15) days after notification.", sale_condition_detail)
            sheet_prescription.merge_range(22, 4, 22,10,"Buyer’s cancellation or changes in specifications after confirmation of receipt of order will incur a fifty (50) percent cancellation fee.Orders for built-to-order and custom-tailored products cannot be cancelled.", sale_condition_detail)
            sheet_prescription.merge_range(23, 4, 23,10,"All disputes, controversies, or differences which may arise between the parties hereto, out of or in relation to or in connection with the contract, shall be finally settled by arbitration in Japan in accordance with the Commercial Arbitration Rules of The Japan Commercial Arbitration Association. The award rendered by the arbitrator shall be final and binding upon both parties.", sale_condition_detail)
            sheet_prescription.merge_range(24, 4, 24,10,"All trade terms provided in the contract shall be interpreted in accordance with the latest Incoterms of the International Chamber of Commerce.", sale_condition_detail)
            sheet_prescription.merge_range(25, 4, 25,10,"The contract shall be governed as to all matters, including validity, construction and performance by and under the laws of Japan.", sale_condition_detail_bottom)
            
            sheet_prescription.set_row(14, 26)
            sheet_prescription.set_row(15, 50)
            sheet_prescription.set_row(16, 50)
            sheet_prescription.set_row(17, 50)
            sheet_prescription.set_row(18, 50)
            sheet_prescription.set_row(19, 50)
            sheet_prescription.set_row(20, 50)
            sheet_prescription.set_row(21, 50)
            sheet_prescription.set_row(22, 50)
            sheet_prescription.set_row(23, 50)
            sheet_prescription.set_row(24, 50)
            sheet_prescription.set_row(25, 50)
            sheet_prescription.merge_range(1,1,1,11,'' , border_default)
            sheet_prescription.merge_range(2,1,25,1,'' , border_left)
            sheet_prescription.merge_range(2,11,25,11,'' , border_right)
            sheet_prescription.insert_image(2, 5, "logo", {'image_data': img_io_ritzwell, 'x_offset': 38, 'y_offset': 1})
            sheet_prescription.merge_range(4,3,4,9,'www.ritzwell.com' , address_web) 
            
            if so.is_show_prescription_note:
                sheet_prescription.write(6,6,so.prescription_note if so.prescription_note else '' , prescrip_note) 
                sheet_prescription.merge_range(7,6,13,10,so.prescription_note_detail if so.prescription_note_detail else '', prescrip_note_detail) 
