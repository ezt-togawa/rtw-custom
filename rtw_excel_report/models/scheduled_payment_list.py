from odoo import models, _
from datetime import datetime 
class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.scheduled_payment_list_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)         
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'center', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name})
        format_current_date = workbook.add_format({'align': 'right', 'valign': 'center', 'text_wrap':True, 'num_format': 'yyyy-mm-dd', 'font_size':10, 'font_name': font_name})
        
        format_wrap = workbook.add_format({'align': 'center', 'valign': 'top', 'text_wrap':True, 'border': 1, 'font_size':9, 'font_name': font_name})
        format_size10 = workbook.add_format({'align': 'center', 'valign': 'top', 'border': 1, 'font_size':9, 'text_wrap':True, 'font_name': font_name})
        format_date = workbook.add_format({'align': 'center', 'valign': 'top', 'text_wrap':True, 'num_format': 'yyyy-mm-dd', 'border': 1, 'font_size':9, 'font_name': font_name})
        format_left = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'border': 1, 'font_size':9, 'font_name': font_name})
        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border':1, 'top':1, 'text_wrap':True, 'font_size':9, 'font_name': font_name})

        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + _(" 年 ") + month + _(" 月 ") + day + _(" 日")

        sheet_name = _("支給予定リスト")
        sheet = workbook.add_worksheet(sheet_name)

        sheet.set_column("A:A", width=4, cell_format=font_family)
        sheet.set_column("B:B", width=10, cell_format=font_family)
        sheet.set_column("C:C", width=14, cell_format=font_family)
        sheet.set_column("D:D", width=14, cell_format=font_family)
        sheet.set_column("E:E", width=32, cell_format=font_family)
        sheet.set_column("F:F", width=18, cell_format=font_family)
        sheet.set_column("G:G", width=18, cell_format=font_family)
        sheet.set_column("H:H", width=18, cell_format=font_family)
        sheet.set_column("I:I", width=14, cell_format=font_family)
        sheet.set_column("J:J", width=12, cell_format=font_family)
        sheet.set_column("K:K", width=10, cell_format=font_family)
        sheet.set_column("L:L", width=10, cell_format=font_family) 
        sheet.set_column("M:M", width=10, cell_format=font_family)
        sheet.set_column("M:M", width=10, cell_format=font_family)
        sheet.set_column("N:Z", None, cell_format=font_family) 

        sheet.merge_range(1, 5, 1, 8, _("≪支給予定リスト≫"), format_sheet_title)
        sheet.merge_range(0, 12, 0, 13, current_date, format_current_date)

        #table title
        sheet.merge_range(5, 0, 6, 0, _("№"), format_table)
        sheet.merge_range(5, 1, 6, 1, _("工場") + "\n" + _("出荷日"), format_table)
        sheet.merge_range(5, 2, 6, 2, _("受注番号"), format_table)
        sheet.merge_range(5, 3, 6, 3, _("担当者"), format_table)
        sheet.merge_range(5, 4, 6, 4, _("張地・部材名"), format_table)
        sheet.merge_range(5, 5, 6, 5, _("送り先"), format_table)
        sheet.merge_range(5, 6, 6, 6, _("備考１"), format_table)
        sheet.merge_range(5, 7, 6, 7, _("備考２"), format_table)
        sheet.merge_range(5, 8, 6, 8, _("(M)数量"), format_table)
        sheet.merge_range(5, 9, 6, 9, _("ロット"), format_table)
        sheet.merge_range(5, 10, 6, 10, _("デシ") + "\n"  + _("換算"), format_table)
        sheet.merge_range(5, 11, 6, 11, _("実") + "\n"  + _("枚数"), format_table)
        sheet.merge_range(5, 12, 6, 12, _("実") + "\n"  + _("ロット"), format_table)
        sheet.merge_range(5, 13, 6, 13, _("実") + "\n"  + _("支給日"), format_table)

        row_start = 7
        merge_to = 7
        
        row_inside = 7
        for index,stock_picking in enumerate(lines):
            confirmed_shipping_date = ""
            user = ""
            location_dest = ""
            note = ""

            if stock_picking.confirmed_shipping_date:
                confirmed_shipping_date = str(stock_picking.confirmed_shipping_date).split("-")[1] + "/" + str(stock_picking.confirmed_shipping_date).split("-")[2]

            if stock_picking.user_id.name:
                user = stock_picking.user_id.name

            if stock_picking.location_dest_id.name:
                location_dest = stock_picking.location_dest_id.name

            if stock_picking.note:
                note = stock_picking.note 

            stock_move_lines = self.env["stock.move.line"].search([("picking_id", "=", stock_picking.id)])
            prod_name = ""
            qty_done = ""

            if stock_move_lines :
                for line in stock_move_lines:
                    p_code = ""
                    p_name = ""

                    if line.product_id.default_code:
                        p_code = "[" + line.product_id.default_code + "]"
                    if line.product_id.product_tmpl_id.name:
                        p_name = line.product_id.product_tmpl_id.name

                    prod_name = p_code + p_name
                    sheet.write(row_inside, 4, prod_name, format_left)

                    if line.qty_done or line.qty_done == 0:
                        qty_done = str(line.qty_done) 
                    else:
                        qty_done = 0
                    sheet.write(row_inside, 8, qty_done, format_wrap)

                    stock_inventory_lines = self.env["stock.inventory.line"].search([("product_id", "=", line.product_id.id)])
                    #has lot
                    if stock_inventory_lines:
                        lot = ""
                        for line in stock_inventory_lines:
                            if line.prod_lot_id.name:
                                lot += line.prod_lot_id.name + '\n'
                            else:
                                sheet.write(row_inside, 9, ' ', format_size10)
                        lot = lot.rstrip("\n")
                        sheet.write(row_inside, 9, lot, format_size10)
                    else:
                        sheet.write(row_inside, 9, ' ', format_size10)

                    row_inside += 1
            else:
                sheet.merge_range(row_start , 4, row_inside, 4, "", format_left)
                sheet.merge_range(row_start , 8, row_inside, 8, 0, format_wrap)
                sheet.merge_range(row_start , 8, row_inside, 8, "", format_size10)
                
                row_inside += 1
                
            merge_to  = row_inside - 1
            
            if row_start != merge_to:
                sheet.merge_range(row_start, 0, merge_to, 0, index + 1, format_wrap)
                sheet.merge_range(row_start, 1, merge_to, 1, confirmed_shipping_date, format_date)
                sheet.merge_range(row_start, 2, merge_to, 2, stock_picking.name, format_wrap)
                sheet.merge_range(row_start, 3, merge_to, 3, user, format_wrap)
                sheet.merge_range(row_start, 5, merge_to, 5, location_dest, format_wrap)
                sheet.merge_range(row_start, 6, merge_to, 6, note, format_wrap)
                sheet.merge_range(row_start, 7, merge_to, 7, "", format_wrap)
                sheet.merge_range(row_start, 10, merge_to, 10, "", format_wrap)
                sheet.merge_range(row_start, 11, merge_to, 11, "", format_wrap)
                sheet.merge_range(row_start, 12, merge_to, 12, "", format_wrap)
                sheet.merge_range(row_start, 13, merge_to, 13, "", format_wrap)
            else:
                sheet.write(row_start, 0, index + 1, format_wrap)
                sheet.write(row_start, 1, confirmed_shipping_date, format_date)
                sheet.write(row_start, 2, stock_picking.name, format_wrap)
                sheet.write(row_start, 3, user, format_wrap)
                sheet.write(row_start, 5, location_dest, format_wrap)
                sheet.write(row_start, 6, note, format_wrap)
                sheet.write(row_start, 7, "", format_wrap)
                sheet.write(row_start, 10, "", format_wrap)
                sheet.write(row_start, 11, "", format_wrap)
                sheet.write(row_start, 12, "", format_wrap)
                sheet.write(row_start, 13, "", format_wrap)
                
            row_start = merge_to + 1
