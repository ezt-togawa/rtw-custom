from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    """
        【御見積書】Excelレポート出力ロジック
        レポートID: rtw_excel_report.report_quotation_xls
        用途: 販売オーダーより御見積書のExcelを作成する
    """
    _name = 'report.rtw_excel_report.report_quotation_xls'
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
        format_text_11_right = workbook.add_format({'align': 'right', 'valign': 'bottom', 'font_name': font_name, 'font_size':11})
        format_text_12_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':12})
        format_text_12_right.set_num_format(num_format_with_symbol)
        format_text_13_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':13})
        format_text_13_right.set_num_format(num_format_with_symbol)
        format_note = workbook.add_format({'align': 'left', 'valign': 'top', 'font_name': font_name, 'font_size':10, 'text_wrap':True})
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
            # sheet.set_print_scale(66)
            
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

            sheet.write(2,5, _("納品希望⽇："), format_text_right)
            sheet.write(3,5, _("製作⽇数："), format_text_right) 
            sheet.write(4,5, _("発注期限："), format_text_right) 
            sheet.write(5,5, _("納品場所："), format_text_right) 
            sheet.write(6,5, _("支払方法："), format_text_right) 
            sheet.write(8,5, _("⾒積有効期限："), format_text_right) 
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

            sheet.write(13, 12, f"No．{so.name if so.name else ''}", format_text_11_right)
            sheet.write(14, 12, _("消費税は含まれておりません"), format_text_12_right)
            #table title
            
            sheet.write(15, 0, _("№"), format_table)
            sheet.merge_range(15, 1, 15, 3, _("品名"), format_table_left)
            sheet.merge_range(15, 4, 15, 7, _("品番・サイズ"), format_table_left)
            sheet.write(15, 8, _("数量"), format_table_right)
            sheet.write(15, 9, _("定価　"), format_table_right)
            sheet.write(15, 10, _("掛率"), format_table_right)
            sheet.write(15, 11, _("販売単価"), format_table_right)
            sheet.write(15, 12, _("販売⾦額"), format_table_right)

            sheet.print_area('A1:M16')

            if so.order_line:
                row = 16
                merge_line = 1

                # 改ページ位置(0-indexed行)は実際の印刷結果から特定した固定値。
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

