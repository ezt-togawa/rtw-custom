from odoo import models, _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    """
        【請求書】Excelレポート出力ロジック
        レポートID: rtw_excel_report.invoice_sale_order_xls
        用途: 販売オーダーより請求書のExcelを作成する
    """
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
        alpha_signature = alpha_signature.point(lambda p: int(p * 0.3))
        stamp_signature_rgba.putalpha(alpha_signature)
        img_io_stamp_signature = BytesIO()
        stamp_signature_rgba.save(img_io_stamp_signature, 'PNG')
        img_io_stamp_signature.seek(0)

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
        format_text = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':11})
        format_text_2 = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':15})
        format_text_right_2 = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':11.25})
        format_text_12_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':12})
        format_text_12_right.set_num_format(num_format_with_symbol)
        format_text_13_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':13})
        format_text_13_right.set_num_format(num_format_with_symbol)
        format_note = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10})
        format_text_14_border = workbook.add_format({'align': 'left','font_name': font_name, 'font_size':14, 'shrink':1, 'bottom':1})
        format_money_bgRed = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':14, 'text_wrap':True, 'color':'white', 'bg_color':'#C00000'})
        format_money_bgRed_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'font_name': font_name, 'font_size':14, 'text_wrap':True, 'color':'white', 'bg_color':'#C00000'})
        format_money_bgRed_right.set_num_format(num_format_with_symbol)
        format_date = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'num_format': 'yyyy-mm-dd', 'font_name': font_name, 'font_size':10})
        format_address = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10.5})
        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11, 'color':'white', 'bold':True})
        format_table_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11, 'color':'white', 'bold':True})
        format_table_right = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'bg_color': '#999999', 'font_name': font_name, 'font_size':11, 'color':'white', 'bold':True})
        format_lines_note = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11, 'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        format_lines_9_left= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':11.25, 'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_10_left = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10, 'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_13.set_num_format(num_format_no_symbol)
        format_lines_14 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
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
            sheet = workbook.add_worksheet(sheet_name)
            sheet_data = workbook.add_worksheet("data")
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
            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin, bottom=bottom_margin)
            sheet.set_header(f'{"&"}R No．{so.name if so.name else ""}', margin=margin_header)
            sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)

            sheet.fit_to_pages(1, 0)
            sheet.center_horizontally()

            sheet.set_column("A:A", width=14, cell_format=font_family)
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
            sheet.set_row(4, 17)
            sheet.set_row(5, 17)
            sheet.set_row(6, 17)
            sheet.set_row(7, 17)
            sheet.set_row(8, 17)
            sheet.set_row(9, 17)
            sheet.set_row(10, 22)
            sheet.set_row(11, 22)
            sheet.set_row(12, 26)
            sheet.set_row(14, 32)

            name_title_end_col = 2  # 宛名・件名の縮小/下線を揃える幅(全角19文字くらい相当)

            sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
            sheet.insert_image(1, 11, "logo2", {'image_data': img_io_ritzwell})
            sheet.insert_image(2, 10, "stamp", {'image_data': img_io_stamp_signature, 'x_offset': 160, 'y_offset': 0})

            # y,x
            sheet.write(1, 1, _("御請求書"), format_sheet_title)
            if so.send_to_company_invoice_sale and so.send_to_people_invoice_sale:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_company_invoice_sale, format_name_company_no_border)
                sheet.merge_range(3, 0, 3, name_title_end_col, so.send_to_people_invoice_sale, format_name_people)
            elif so.send_to_company_invoice_sale:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_company_invoice_sale, format_name_company)
            elif so.send_to_people_invoice_sale:
                sheet.merge_range(2, 0, 2, name_title_end_col, so.send_to_people_invoice_sale, format_name_people)

            sheet.write(5, 0, _("平素より格別のお引き立てを賜り厚く御礼申し上げます。"), format_text)
            sheet.write(6, 0, _("下記の通り、ご請求申し上げます。"), format_text)
            sheet.merge_range(8, 0, 8, name_title_end_col, (_("件名 : ") + so.title) if so.title else '', format_text_14_border)
            sheet.write(10, 0, _("税抜合計"), format_text)
            sheet.write(11, 0, _("消費税(10%)"), format_text)
            sheet.write(12, 0, _("税込合計"), format_money_bgRed)
            sheet.write(10, 1, so.amount_untaxed, format_text_13_right)
            sheet.write(11, 1, so.amount_tax, format_text_12_right)
            sheet.write(12, 1, so.amount_total, format_money_bgRed_right)

            sheet.write(2, 5, _("お支払期限"), format_text_right_2)
            sheet.write(3, 5, _("お支払内容"), format_text_right_2)
            sheet.write(4, 5, _("お振込先"), format_text_right_2)
            sheet.write(4, 6, so.sale_order_bank_name if so.sale_order_bank_name else '', format_text)
            sheet.write(5, 6, so.sale_order_bank_branch if so.sale_order_bank_branch else '', format_text)
            sheet.write(6, 6, so.sale_order_number_account if so.sale_order_number_account else '', format_text)

            sheet.write(7, 5, _("納品日"), format_text_right_2)
            sheet.write(8, 5, _("納品場所"), format_text_right_2)
            sheet.write(9, 5, _("備考"), format_text_right_2)
            sheet.write(2, 6, so.sale_payment_deadline if so.sale_payment_deadline else '', format_text)
            sheet.write(3, 6, (so.payment_details or '') if so.payment_details else '', format_text)

            sheet.write(7, 6, so.sale_order_preferred_delivery_date if so.sale_order_preferred_delivery_date else '', format_text)
            sheet.write(8, 6, so.forwarding_address if so.forwarding_address else '', format_text)
            sheet.merge_range(9, 6, 12, 8, so.sale_order_billing_notes if so.sale_order_billing_notes else '', format_note)

            sheet.merge_range(0, 11, 0, 12, so.sale_order_current_date if so.sale_order_current_date else '', format_date)
            sheet.merge_range(2, 11, 9, 12, so.sale_order_hr_employee_invoice if so.sale_order_hr_employee_invoice else '', format_address)

            #table title
            sheet.write(14, 0, _("№"), format_table)
            sheet.merge_range(14, 1, 14, 3, _("品名"), format_table_left)
            sheet.merge_range(14, 4, 14, 7, _("品番・サイズ"), format_table_left)
            sheet.write(14, 8, _("数量"), format_table_right)
            sheet.write(14, 9, _("定価　"), format_table_right)
            sheet.write(14, 10, _("掛率"), format_table_right)
            sheet.write(14, 11, _("販売単価"), format_table_right)
            sheet.write(14, 12, _("販売金額"), format_table_right)

            sheet.print_area('A1:M15')

            if so.order_line:
                row = 15
                merge_line = 1

                # 改ページ位置(0-indexed行)は report_quotation.py の実測値(ページ2: 40行目, ページ3: 84行目)を
                # 明細表開始行の差分(このファイルは0-idx15開始、report_quotation.pyは0-idx16開始 → -1行)だけ
                # ずらして踏襲する。ページ2→3の行数間隔(44行)はそのまま。
                FIRST_PAGE_BREAK_ROW = 39
                SECOND_PAGE_BREAK_ROW = 83
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
                        sheet.merge_range(row, 0, row , 12, "=data!A" + str(ind * 1 + 1), fmt_note)
                        sheet_data.write(ind, 0, line.name if line.name else '', fmt_note)
                    elif line.display_type == 'line_section':
                        fmt_section = format_lines_section_top if is_first_of_new_page else format_lines_section
                        sheet.set_row(row, 18)
                        sheet.merge_range(row, 0, row , 12, "=data!B" + str(ind * 1 + 1) , fmt_section)
                        sheet_data.write(ind, 1, line.name if line.name else '', fmt_section)
                    else:
                        fmt_10 = format_lines_10_top if is_first_of_new_page else format_lines_10
                        fmt_9_left = format_lines_9_left_top if is_first_of_new_page else format_lines_9_left
                        fmt_11_left = format_lines_11_left_top if is_first_of_new_page else format_lines_11_left
                        fmt_13 = format_lines_13_top if is_first_of_new_page else format_lines_13
                        fmt_14 = format_lines_14_top if is_first_of_new_page else format_lines_14
                        sheet.set_row(row, 18)
                        sheet.set_row(row + merge_line, 18)
                        sheet.merge_range(row, 0, row + merge_line, 0, line.sale_order_index if line.sale_order_index else '' , fmt_10)
                        sheet.merge_range(row, 1, row + merge_line, 3, line.sale_order_line_name_excel if line.sale_order_line_name_excel else '' , fmt_9_left)
                        sheet.merge_range(row, 4, row + merge_line, 7, line.sale_order_number_and_size if line.sale_order_number_and_size else '' , fmt_11_left)

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

                if row > 15:
                    last_content_row = row - 1
                    sheet.print_area(f'A1:M{last_content_row + 1}')
                    if pagebreak_positions:
                        sheet.set_h_pagebreaks(pagebreak_positions)
