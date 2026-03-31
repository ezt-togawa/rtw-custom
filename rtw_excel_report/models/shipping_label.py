from datetime import date, datetime
from odoo import models, _


class productShippingLabel(models.AbstractModel):
    """
        【送り状シール】Excel出力ロジック
        レポートID: rtw_excel_report.shipping_label_xls
    """
    _name = 'report.rtw_excel_report.shipping_label_xls'
    _inherit = 'report.report_xlsx.abstract'

    def _format_jp_date_with_weekday(self, value):
        weekday_names = ['月', '火', '水', '木', '金', '土', '日']

        if not value or value == ' ':
            return ' '

        dt_value = None

        if isinstance(value, datetime):
            dt_value = value.date()
        elif isinstance(value, date):
            dt_value = value
        elif isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                return ' '

            normalized = normalized.split('（')[0].split('(')[0].strip()

            for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日'):
                try:
                    dt_value = datetime.strptime(normalized, fmt).date()
                    break
                except ValueError:
                    continue

        if not dt_value:
            return value

        weekday = weekday_names[dt_value.weekday()]
        return f"{dt_value.year}年{dt_value.month}月{dt_value.day}日（{weekday}）"

    def _get_objs_for_report(self, docids, data):
        return self.env['stock.picking'].browse(docids)

    def generate_xlsx_report(self, workbook, data, lines):
   
        self = self.with_context(lang=self.env.user.lang)
        font_name = 'HGP創英角ｺﾞｼｯｸUB'

        # 印字開始位置の取得
        rec = self.env["mrp.location_item_excel_prod_label"].get_singleton()
        location_item_row = rec.location_item_row or 1

        fmt_sale_order = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'top',
        })
    
        fmt_depo_date = workbook.add_format({
            'font_name': font_name, 'font_size': 12,
            'bold': True,
            'align': 'left', 'valign': 'top',
            'num_format': 'yyyy/mm/dd',
        })
        fmt_stock_move_date = workbook.add_format({
            'num_format': 'yyyy"年"mm"月"dd"日"（  ）',
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'top',
        })
        fmt_warehouse_arrive_date = workbook.add_format({
            'num_format': 'yyyy"年"mm"月"dd"日"（  ）',
            'font_name': font_name, 'font_size': 13,
            'align': 'left', 'valign': 'top',
        })
        fmt_description_picking = workbook.add_format({
            'font_name': font_name, 'font_size': 18,
            'align': 'left', 'shrink': True,
        })
        fmt_prod_attrs = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'vcenter',
            'text_wrap': True,
        })
        fmt_address = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'top', 'shrink': True,
        })
        fmt_sale_title = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'vcenter',
            'shrink': True,
        })
        fmt_recipient = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'top', 'shrink': True,
        })
        fmt_customer_name = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'vcenter',
            'shrink': True,
        })
        fmt_itoshima_shiratani_shipping_notes_first_line = workbook.add_format({
            'font_name': font_name, 'font_size': 11,
            'align': 'left', 'valign': 'vcenter',
            'shrink': True,
        })
        fmt_product_qty= workbook.add_format({
            'font_name': font_name, 'font_size': 14,
            'align': 'left', 'valign': 'left',
        })
        fmt_qty_center = workbook.add_format({
            'font_name': font_name, 'font_size': 14,
            'align': 'left', 'valign': 'center',
        })

        COL_WIDTHS = {
            0: 17.89,   # A
            1: 10.44,   # B
            2: 2.22,    # C
            3: 15.66,   # D
            4: 8.0,     # E  
            5: 20.11,   # F
            6: 4.0,     # G 
            7: 2.89,    # H  
            8: 5.78,    # I  
            9: 8.44,    # J  
            10: 4.44,   # K
            11: 1.78,   # L
            12: 5.78,   # M
            13: 0.89,   # N
            14: 4.22,   # O
        }
        HIDDEN_COLS = {6, 7, 8, 9}  # G, H, I, J

        ROW_LAYOUT = [
            (15.15, False),   # row 0  
            (20.25, False),   # row 1  
            (6.75,  False),   # row 2  
            (10.5,  False),   # row 3  
            (15.0,  False),   # row 4  
            (9.0,   True),    # row 5  
            (24.0,  False),   # row 6  
            (15.6,  False),   # row 7 
            (15.6,  False),   # row 8  
            (15.75, False),   # row 9
            (10.5,  False),   # row 10
            (16.5,  False),   # row 11 
            (16.5,  False),   # row 12 
            (14.25, False),   # row 13 
            (9.75,  False),   # row 14
            (15.0,  False),   # row 15 
            (13.5,  False),   # row 16 
            (6.0,   False),   # row 17
            (18.0,  False),   # row 18 
            (9.75,  False),   # row 19
            (9.75,  False),   # row 20
        ]
        
        ROW_LAYOUT_2 = [
            (33.75, False),  # row 0
            (20.25, False),  # row 1
            (6.75,  False),  # row 2
            (10.35, False),  # row 3
            (15.0,  False),  # row 4
            (9.0,   True),   # row 5 
            (24.0,  False),  # row 6
            (15.6,  False),  # row 7
            (15.6,  False),  # row 8
            (15.75, False),  # row 9
            (10.35, False),  # row 10
            (16.5,  False),  # row 11
            (16.5,  False),  # row 12
            (14.25, False),  # row 13
            (9.75,  False),  # row 14
            (14.85, False),  # row 15
            (13.5,  False),  # row 16
            (6.0,   False),  # row 17
            (18.0,  False),  # row 18
            (9.75,  False),  # row 19
            (9.75,  False),  # row 20
        ]
        ROW_LAYOUT_3 = [
            (33.75, False),  # row 0
            (20.25, False),  # row 1
            (6.75,  False),  # row 2
            (9.75,  False),  # row 3
            (15.0,  False),  # row 4
            (9.0,   True),   # row 5 
            (24.6,  False),  # row 6
            (15.6,  False),  # row 7
            (15.6,  False),  # row 8
            (15.75, False),  # row 9
            (10.35, False),  # row 10
            (16.5,  False),  # row 11
            (16.35, False),  # row 12
            (14.25, False),  # row 13
            (9.75,  False),  # row 14
            (14.85, False),  # row 15
            (13.5,  False),  # row 16
            (6.0,   False),  # row 17
            (18.0,  False),  # row 18
            (9.75,  False),  # row 19
            (10.2,  False),  # row 20
        ]
        
        PAGE_ROW_LAYOUTS = [ROW_LAYOUT, ROW_LAYOUT_2, ROW_LAYOUT_3]

        def write_label(sheet, row_start, layout, label_data):
  
            for rel, (h, hidden) in enumerate(layout):
                r = row_start + rel
                sheet.set_row(r, h)
                if hidden:
                    sheet.set_row(r, h, None, {'hidden': True})

            d = label_data

            sheet.merge_range(row_start + 1, 3, row_start + 1, 4, d.get('sale_order', ''), fmt_sale_order)
            sheet.merge_range(row_start + 1, 10, row_start + 1, 12, d.get('product_qty', ''), fmt_product_qty)

            sheet.merge_range(row_start + 2, 3, row_start + 3, 4,
                              d.get('stock_move_date', ''), fmt_stock_move_date)

            sheet.merge_range(row_start + 3, 10, row_start + 4, 10, d.get('seri_number', ''), fmt_qty_center)
            sheet.merge_range(row_start + 3, 12, row_start + 4, 12, d.get('product_package_quantity', ''), fmt_qty_center)

            sheet.merge_range(row_start + 4, 3, row_start + 4, 4,
                              d.get('warehouse_arrive_date', ''), fmt_warehouse_arrive_date)

            sheet.write(row_start + 4, 9, d.get('depo_date', ''), fmt_depo_date)

            sheet.merge_range(row_start + 6, 3, row_start + 6, 12,
                              d.get('description_picking', ''), fmt_description_picking)

            sheet.merge_range(row_start + 7, 3, row_start + 9, 12,
                              d.get('prod_attrs', ''), fmt_prod_attrs)

            sheet.merge_range(row_start + 11, 3, row_start + 11, 12,
                              d.get('partner_name', ''), fmt_recipient)

            sheet.merge_range(row_start + 12, 3, row_start + 12, 12,
                              d.get('zip_city_state', ''), fmt_address)

            sheet.merge_range(row_start + 13, 3, row_start + 13, 12,
                              d.get('phone', ''), fmt_address)

            sheet.merge_range(row_start + 15, 3, row_start + 15, 12,
                              d.get('sale_title', ''), fmt_sale_title)

            sheet.merge_range(row_start + 16, 3, row_start + 16, 12,
                              d.get('customer_name', ''), fmt_customer_name)

            sheet.merge_range(row_start + 17, 3, row_start + 18, 12,
                              d.get('itoshima_shiratani_shipping_notes_first_line', ''), fmt_itoshima_shiratani_shipping_notes_first_line)

        sheet_main = workbook.add_worksheet("印刷画面")
        sheet_main.set_paper(9)
        sheet_main.set_margins(left=0.15, right=0.15, top=0.15, bottom=0.15)
        sheet_main.set_footer('&C Page &P ')

        for col_idx, width in COL_WIDTHS.items():
            if col_idx in HIDDEN_COLS:
                sheet_main.set_column(col_idx, col_idx, width, None, {'hidden': True})
            else:
                sheet_main.set_column(col_idx, col_idx, width)

        global_label_index = 0

        model_name = lines._name if lines else ''
        if model_name == 'stock.picking':
            target_moves = self.env["stock.move"].search([("picking_id", "in", lines.ids)])
        elif model_name == 'stock.move':
            target_moves = lines
        else:
            target_moves = []

        current_label_pos = location_item_row  # 開始位置

        for line in target_moves:
            stock_picking = line.picking_id
            if stock_picking or not stock_picking:
                description_picking = line.description_picking or ''

                prod_attrs = " "
                attribute = line.product_id.product_template_attribute_value_ids
                if attribute:
                    attr_list = []
                    for attr in attribute:
                        attr_str = attr.attribute_id.name + ":" + attr.name
                        attr_list.append(attr_str)
                    prod_attrs += " / ".join(attr_list)

                partner = stock_picking.waypoint or line.sale_id.waypoint

                state = partner.state_id.name or ' ' if partner else ' '
                city = partner.city or ' ' if partner else ' '
                street = partner.street or ' ' if partner else ' '
                street_2 = partner.street2 or ' ' if partner else ' '
                phone = partner.phone or ' ' if partner else ' '
                partner_name = partner.name if partner else ' '
                sale_title = line.sale_id.title if line.sale_id.title else ' '
                customer_name = line.customer_id.name if line.customer_id.name else ' '
                sale_order = line.sale_id.name if line.sale_id.name else ' '

                stock_move_date = self._format_jp_date_with_weekday(line.date)

                warehouse_arrive_date = line.warehouse_arrive_date or ' '
                warehouse_arrive_date = self._format_jp_date_with_weekday(warehouse_arrive_date)
                itoshima_shiratani_shipping_notes_first_line = line.itoshima_shiratani_shipping_notes.split('\n')[0] if line.itoshima_shiratani_shipping_notes else ' '
                product_qty = line.product_qty or ' '
                product_package_quantity = line.product_package_quantity if line.product_package_quantity is not False else ' '

                zip_city_state = f"{state} {city} {street} {street_2}"

                try:
                    pkg_qty = int(product_package_quantity)
                except (ValueError, TypeError):
                    pkg_qty = 1

                if pkg_qty <= 0:
                    pkg_qty = 1

                for count in range(pkg_qty):
                    label_data = {
                        'sale_order': sale_order,
                        'stock_move_date': stock_move_date,
                        'warehouse_arrive_date': warehouse_arrive_date,
                        'description_picking': description_picking,
                        'prod_attrs': prod_attrs,
                        'partner_name': partner_name,
                        'zip_city_state': zip_city_state,
                        'phone': phone,
                        'sale_title': sale_title,
                        'customer_name': customer_name,
                        'itoshima_shiratani_shipping_notes_first_line': itoshima_shiratani_shipping_notes_first_line,
                        'product_qty': product_qty,
                        'seri_number': count + 1,
                        'product_package_quantity': product_package_quantity,
                    }

                    # 印字位置計算
                    page_inner_idx = (current_label_pos - 1) % 3
                    row_start = ((current_label_pos - 1) // 3) * 63 + (page_inner_idx * 21)

                    write_label(sheet_main, row_start, PAGE_ROW_LAYOUTS[page_inner_idx], label_data)
                    current_label_pos += 1

        total_pages = (current_label_pos + 2) // 3
        sheet_main.set_h_pagebreaks([63 * i for i in range(1, total_pages)])
        sheet_main.print_area(0, 0, (total_pages * 63) - 1, 12)
        sheet_main.fit_to_pages(1, total_pages)


class ProductShippingLabelMove(models.AbstractModel):
    _name = 'report.rtw_excel_report.shipping_label_move_xls'
    _inherit = 'report.report_xlsx.abstract'

    def _get_objs_for_report(self, docids, data):
        return self.env['stock.move'].browse(docids)

    def generate_xlsx_report(self, workbook, data, lines):
        return self.env['report.rtw_excel_report.shipping_label_xls'].generate_xlsx_report(workbook, data, lines)
