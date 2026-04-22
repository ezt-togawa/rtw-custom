from odoo import models, _
import math

class productLabelSticker(models.AbstractModel):
    """
        【商品ラベルシール】Excel出力ロジック
        レポートID: rtw_excel_report.product_label_sticker_xls
    """
    _name = "report.rtw_excel_report.product_label_sticker_xls"
    _inherit = "report.report_xlsx.abstract"
    def _get_attr_by_priority(self, product):
        result = {
            '4': '',
            '5': '',
            '6': '',
            '7': '',
            '8': '',
            '9': '',
            '10': '',
            '11': '',
        }

        if not product or not product.product_template_attribute_value_ids:
            return result

        attr_map = {}
        attr_code_map = {}

        for line in product.product_template_attribute_value_ids:
            attr = line.attribute_id
            value = line.product_attribute_value_id

            attr_name = attr.name
            value_name = value.name

            attr_map[attr_name] = f"{attr_name}: {value_name}"

            attr_xml = attr.get_external_id().get(attr.id)
            attr_code = None
            if attr_xml and '.' in attr_xml:
                code_part = attr_xml.split('.')[-1]
                if code_part.isdigit():
                    attr_code = code_part

            if attr_code:
                attr_code_map[attr_code] = f"{attr_name}: {value_name}"

        # 属性のコード
        priority_code_map = {
            '4': ['001', '050'],
            '5': ['002', '051'],
            '6': ['006', '010'],
            '7': ['009', '011'],
            '8': ['110', '117', '111', '118'],
            '9': ['112'],
            '10': ['003', '004', '005', '008', '204', '326', '325'],
            '11': ['402', '012'],
        }

        for key in result.keys():
            for code in priority_code_map.get(key, []):
                if code in attr_code_map:
                    result[key] = attr_code_map[code]
                    break
        return result

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)

        model_name = lines._name if lines else ''

        def _to_label_count(qty):
            try:
                qty_float = float(qty or 0)
            except (TypeError, ValueError):
                return 0
            qty_int = int(qty_float)
            return qty_int if qty_int > 0 else 0

        def _get_label_count(record):
            if model_name == 'stock.move':
                return _to_label_count(record.product_package_quantity)
            if model_name == 'mrp.production':
                for move in record.move_finished_ids:
                    for dest_move in move.move_dest_ids:
                        if dest_move.picking_id:
                            return _to_label_count(dest_move.product_package_quantity)
                return 0
            return 1

        font_name = 'HGPｺﾞｼｯｸM'

        def _fmt(props):
            props['font_name'] = font_name
            return workbook.add_format(props)

        fmt_base = _fmt({})

        fmt_prod_name = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 17, 'text_wrap': True,
            'border': 2, 
        })

        fmt_chubun = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 18,
            'left': 2, 'right': 1, 'bottom': 1,
        })

        fmt_product_uom_qty = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 18,
            'left': 1, 'right': 2, 'bottom': 1, 
        })
        
        fmt8_prod_name = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 18, 'text_wrap': True,
            'border': 2,
        })

        fmt8_chubun = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 18,
            'top': 2, 'bottom': 2, 'left': 2, 'right': 1,
        })

        fmt8_product_uom_qty = _fmt({
            'align': 'center', 'valign': 'vcenter',
            'font_size': 18,
            'top': 2, 'bottom': 2, 'left': 1, 'right': 2,
        })

        fmt_attr_left_wide = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 16, 'text_wrap': True,
            'left': 2, 'top': 1, 'bottom': 1, 
        })

        fmt_attr_right_narrow = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 14, 'text_wrap': True,
            'right': 2, 'top': 1, 'bottom': 1, 
        })

        fmt_harijiL = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 14, 'text_wrap': True,
            'left': 2, 'top': 1, 'bottom': 1, 'right': 1,
        })

        fmt_harijiR = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 14, 'text_wrap': True,
            'left': 1, 'top': 1, 'bottom': 1, 'right': 2,
        })

        fmt_beltoL = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 14, 'text_wrap': True,
            'left': 2, 'top': 1, 'bottom': 2, 'right': 1,
        })
        fmt_beltoR = _fmt({
            'align': 'left', 'valign': 'vcenter',
            'font_size': 14, 'text_wrap': True,
            'left': 1, 'top': 1, 'bottom': 2, 'right': 2,
        })

        sheet = workbook.add_worksheet(_("商品ラベルシール-"))

  
        sheet.set_column(0,  0,  0.69,  fmt_base)
        sheet.set_column(1,  6,  7.89,  fmt_base)
        sheet.set_column(7,  8,  0.69,  fmt_base)
        sheet.set_column(9,  14, 7.89,  fmt_base)
        sheet.set_column(15, 15, 0.69,  fmt_base)

        ROW_HEIGHTS_6 = [7.35, 53.85, 46.75, 46.75, 46.75, 46.75, 46.75, 6.15]

        ROW_HEIGHTS_8 = [7.35, 105.0, 104.5, 7.15]

        L_START = 1   # B
        L_MID1  = 4   # E 
        L_MID2  = 5   # F  
        L_END   = 6   # G

        R_START = 9   # J
        R_MID1  = 12  # M 
        R_MID2  = 13  # N  
        R_END   = 14  # O

        # 印字開始位置の取得
        rec = self.env["mrp.location_item_excel_prod_label"].get_singleton()
        location_item_row = rec.location_item_row or 1

        sheet.set_margins(left=0, right=0, top=0.05, bottom=0)
        sheet.center_horizontally()
        sheet.set_paper(9)
        # ページ数は印刷しない（ラベル用紙にスペースなし想定）
        # if rec and rec.label_type == '6':
        #     sheet.set_footer('&C&8Page &P', {'margin': 0.1, 'scale_with_doc': False})
        # else:
        #     sheet.set_footer('&C&8Page &P', {'scale_with_doc': False})

        group_size = 8 if rec.label_type == '6' else 4
        row_start_begin = (location_item_row - 1) // 2 * group_size

        labels_per_page = 6 if rec.label_type == '6' else 8
        pairs_per_page = labels_per_page // 2
        rows_per_page = pairs_per_page * group_size

        total_labels = sum(_get_label_count(obj) for obj in lines)
        if total_labels <= 0:
            total_labels = 1
        
        max_group_index = (location_item_row + total_labels - 2) // 2
        full_pages = (max_group_index // pairs_per_page) + 1
        total_rows = full_pages * rows_per_page
        sheet.print_area(f'$A$1:$P${total_rows}')
        sheet.fit_to_pages(1, 0)

        page_breaks = []
        r = rows_per_page
        while r < total_rows:
            page_breaks.append(r)
            r += rows_per_page
        if page_breaks:
            sheet.set_h_pagebreaks(page_breaks)

        def _write_label_sheet6(slot, row_heights_set, r, data_row):
     
            if r not in row_heights_set:
                for offset, h in enumerate(ROW_HEIGHTS_6):
                    sheet.set_row(r + offset, h)
                row_heights_set.add(r)

            if slot % 2 != 0:
                c0, c_mid1, c_mid2, c_end = L_START, L_MID1, L_MID2, L_END
            else:
                c0, c_mid1, c_mid2, c_end = R_START, R_MID1, R_MID2, R_END

            sheet.merge_range(r+1, c0,     r+1, c_end,    data_row['prod_name'],   fmt_prod_name)
            sheet.merge_range(r+2, c0,     r+2, c_mid1-1, data_row['sale_name'],    fmt_chubun)
            sheet.merge_range(r+2, c_mid1, r+2, c_end,    data_row['product_uom_qty'], fmt_product_uom_qty)
            sheet.merge_range(r+3, c0,     r+3, c_mid2-1, data_row['attr_value_1'], fmt_attr_left_wide)
            sheet.merge_range(r+3, c_mid2, r+3, c_end,    data_row['attr_value_2'], fmt_attr_right_narrow)
            sheet.merge_range(r+4, c0,     r+4, c_mid2-1, data_row['attr_value_3'], fmt_attr_left_wide)
            sheet.merge_range(r+4, c_mid2, r+4, c_end,    data_row['attr_value_4'], fmt_attr_right_narrow)
            sheet.merge_range(r+5, c0,     r+5, c_mid1-1, data_row['attr_value_5'], fmt_harijiL)
            sheet.merge_range(r+5, c_mid1, r+5, c_end,    data_row['attr_value_6'], fmt_harijiR)
            sheet.merge_range(r+6, c0,     r+6, c_mid1-1, data_row['attr_value_7'], fmt_beltoL)
            sheet.merge_range(r+6, c_mid1, r+6, c_end,    data_row['attr_value_8'], fmt_beltoR)

        def _write_label_sheet8(slot, row_heights_set, r, data_row):
          
            if r not in row_heights_set:
                for offset, h in enumerate(ROW_HEIGHTS_8):
                    sheet.set_row(r + offset, h)
                row_heights_set.add(r)

            if slot % 2 != 0:
                c0, c_mid1, c_end = L_START, L_MID1, L_END
            else:
                c0, c_mid1, c_end = R_START, R_MID1, R_END

            sheet.merge_range(r+1, c0,     r+1, c_end,    data_row['prod_name'], fmt8_prod_name)
            sheet.merge_range(r+2, c0,     r+2, c_mid1-1, data_row['sale_name'], fmt8_chubun)
            sheet.merge_range(r+2, c_mid1, r+2, c_end,    data_row['product_uom_qty'], fmt8_product_uom_qty)

        # 入数算出
        def _calculate_package_contents(qty, num_packages):
            if num_packages <= 0:
                return []

            # 1箱あたりの基本の数（最低限入る数、切り捨て）
            base_qty = qty // num_packages
            # 余りの数
            remainder = qty % num_packages

            packages = []
            for i in range(num_packages):
                # 余りがあるうちは、基本の数に +1 してあげる
                current_package_qty = base_qty + (1 if i < remainder else 0)
                packages.append(current_package_qty)

            return packages

        row_heights_set = set()
        count = 0

        _heights = ROW_HEIGHTS_6 if rec.label_type == '6' else ROW_HEIGHTS_8
        for pair_idx in range(total_rows // group_size):
            r = pair_idx * group_size
            for offset, h in enumerate(_heights):
                sheet.set_row(r + offset, h)
            row_heights_set.add(r)

        for obj in lines:
            attributes = []

            prod_name = obj.product_id.name if obj.product_id else ""
            if prod_name and '→' in prod_name:
                prod_name = prod_name.replace('→', '\n→')

            attr_dict = self._get_attr_by_priority(obj.product_id)

            if not attr_dict['4']:
                attr_dict['5'] = ''
            if not attr_dict['6']:
                attr_dict['7'] = ''

            attributes = [
                attr_dict['4'],
                attr_dict['5'],
                attr_dict['6'],
                attr_dict['7'],
                attr_dict['8'],
                attr_dict['9'],
                attr_dict['10'],
                attr_dict['11'],
            ]

            attributes = [attr if attr else "" for attr in attributes]
            # 個口数（ラベル枚数）を取得
            label_count = int(_get_label_count(obj))
            quantity_list = []
            if model_name == 'mrp.production':
                sale_name = obj.sale_reference if obj.sale_reference else ""
                quantity_list = _calculate_package_contents(obj.product_qty, label_count)
            elif model_name == 'stock.move':
                sale_name = obj.sale_id.name if obj.sale_id else ""
                # 数量＞個口数 の場合は入数を計算
                if obj.product_uom_qty > 0 and obj.product_uom_qty > label_count:
                    # 入数計算（数量/個口数）
                    quantity_list = _calculate_package_contents(obj.product_uom_qty, label_count)
                else:
                    quantity_list = [1] * label_count
            else:
                sale_name = ""
                quantity_list = [""] * label_count

            data_row = {
                'prod_name': prod_name,
                'sale_name': sale_name,
                'product_uom_qty': "",  # ここは後で書き換え
                'attr_value_1': attributes[0],
                'attr_value_2': attributes[1],
                'attr_value_3': attributes[2],
                'attr_value_4': attributes[3],
                'attr_value_5': attributes[4],
                'attr_value_6': attributes[5],
                'attr_value_7': attributes[6],
                'attr_value_8': attributes[7],
            }

            for label_index in range(label_count):
                row_start = row_start_begin + count * group_size

                if label_index < len(quantity_list):
                    data_row['product_uom_qty'] = quantity_list[label_index]
                else:
                    data_row['product_uom_qty'] = ""

                if rec.label_type == '6':
                    _write_label_sheet6(location_item_row, row_heights_set, row_start, data_row)
                else:
                    _write_label_sheet8(location_item_row, row_heights_set, row_start, data_row)

                if location_item_row % 2 == 0:
                    count += 1
                location_item_row += 1



class ProductLabelStickerMrp(models.AbstractModel):
    _name = 'report.rtw_excel_report.product_label_sticker_mrp_xls'
    _inherit = 'report.report_xlsx.abstract'

    def _get_objs_for_report(self, docids, data):
        return self.env['mrp.production'].browse(docids)

    def generate_xlsx_report(self, workbook, data, lines):
        return self.env['report.rtw_excel_report.product_label_sticker_xls'].generate_xlsx_report(workbook, data, lines)
