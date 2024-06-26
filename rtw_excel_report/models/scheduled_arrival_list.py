from odoo import models, _
from datetime import datetime 
class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.scheduled_arrival_list_xls'
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
        format_left = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'border': 1, 'font_size':9, 'font_name': font_name})
        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border':1, 'top':1, 'text_wrap':True, 'bg_color':"#CCCCCC", 'font_size':9,'font_name': font_name})

        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + _(" 年") + month + _("月 ") + day + _("日 ")

        sheet_name = _("入荷予定リスト")  
        sheet = workbook.add_worksheet(sheet_name)

        sheet.set_column("A:A", width=2,cell_format=font_family)
        sheet.set_column("B:B", width=10,cell_format=font_family)
        sheet.set_column("C:C", width=14,cell_format=font_family)
        sheet.set_column("D:D", width=15,cell_format=font_family)
        sheet.set_column("E:E", width=16,cell_format=font_family)
        sheet.set_column("F:F", width=16,cell_format=font_family)
        sheet.set_column("G:G", width=12,cell_format=font_family)
        sheet.set_column("H:H", width=13,cell_format=font_family)
        sheet.set_column("I:I", width=15,cell_format=font_family)
        sheet.set_column("J:J", width=15,cell_format=font_family)
        sheet.set_column("K:K", width=17,cell_format=font_family)
        sheet.set_column("L:L", width=12,cell_format=font_family) 
        sheet.set_column("M:M", width=20,cell_format=font_family)
        sheet.set_column("N:N", width=4,cell_format=font_family)
        sheet.set_column("M:Z", None,cell_format=font_family)

        sheet.merge_range(1, 5, 1, 8, _("≪入荷予定リスト≫ "), format_sheet_title)
        sheet.merge_range(0, 12, 0, 13, current_date, format_current_date)

        #table title
        sheet.merge_range(5, 0, 6, 0, _("№"), format_table)
        sheet.merge_range(5, 1, 6, 1, _("入荷") +"\n"+ _("予定日"), format_table)
        sheet.merge_range(5, 2, 6, 2, _("発注") +"\n"+ _("番号"), format_table)
        sheet.merge_range(5, 3, 6, 3, _("発注先"), format_table)
        sheet.merge_range(5, 4, 6, 5, _("部材名"), format_table)
        sheet.merge_range(5, 6, 6, 6, _("発注数") , format_table)
        sheet.merge_range(5, 7, 6, 7, _("入荷") + "\n" + _("残数") , format_table)
        sheet.merge_range(5, 8, 6, 8, _("入荷") + "\n" + _("予定数"), format_table)
        sheet.merge_range(5, 9, 6, 9, _("入荷数"), format_table)
        sheet.merge_range(5, 10, 6, 10, _("要検品"), format_table)
        sheet.merge_range(5, 11, 6, 11, _("受注") + "\n" + _("番号"), format_table)
        sheet.merge_range(5, 12, 6, 12, _("記入メモ"), format_table)
        sheet.merge_range(5, 13, 6, 13, _("済"), format_table)

        row_start = 7
        merge_to = 7
        
        row_inside = 7
        for index,stock_picking in enumerate(lines):
            scheduled_date=""
            order_number=""
            partner=""
            prod_tmpl=""

            if stock_picking.scheduled_date:
                scheduled_date = stock_picking.scheduled_date.strftime("%m/%d")

            if stock_picking.name:
                order_number = stock_picking.name

            if stock_picking.partner_id.name:
                partner = stock_picking.partner_id.name

            stock_move_lines = self.env["stock.move.line"].search([("picking_id", "=", stock_picking.id)])

            if stock_move_lines :
                for line in stock_move_lines:
                    p_code = ""
                    prod_tmpl = ""
                    demand = 0
                    qty_done = 0

                    if line.product_id.default_code:
                        p_code = "[" + line.product_id.default_code + "]"

                    if line.product_id.product_tmpl_id.name:
                        prod_tmpl = line.product_id.product_tmpl_id.name

                    if line.product_uom_qty:
                        demand = line.product_uom_qty

                    if line.qty_done:
                        qty_done = line.qty_done

                    qty_remain = demand - qty_done
                    
                    sheet.write(row_inside, 4, p_code, format_left)
                    sheet.write(row_inside, 5, prod_tmpl, format_left)
                    sheet.write(row_inside, 6, demand, format_wrap)
                    sheet.write(row_inside, 7, qty_remain, format_wrap)
                    sheet.write(row_inside, 8, qty_done, format_wrap)
                    sheet.write(row_inside, 9, "", format_wrap)
                    row_inside += 1
            else:
                sheet.write(row_inside, 4, "", format_left)
                sheet.write(row_inside, 5, "", format_left)
                sheet.write(row_inside, 6, "", format_wrap)
                sheet.write(row_inside, 7, "", format_wrap)
                sheet.write(row_inside, 8, "qty_done", format_wrap)
                sheet.write(row_inside, 9, "", format_wrap)
                row_inside += 1
                
            merge_to = row_inside - 1

            if row_start == merge_to:
                sheet.write(row_start , 0, index + 1, format_wrap)
                sheet.write(row_start , 1, scheduled_date, format_wrap)
                sheet.write(row_start , 2, order_number, format_wrap)
                sheet.write(row_start , 3, partner, format_wrap)
                sheet.write(row_start , 10, "", format_wrap)
                sheet.write(row_start , 11, order_number, format_wrap)
                sheet.write(row_start , 12, "", format_wrap)
                sheet.write(row_start , 13, "", format_wrap)
            else:
                sheet.merge_range(row_start , 0, merge_to,0, index + 1, format_wrap)
                sheet.merge_range(row_start , 1, merge_to,1, scheduled_date, format_wrap)
                sheet.merge_range(row_start , 2, merge_to,2, order_number, format_wrap)
                sheet.merge_range(row_start , 3, merge_to,3, partner, format_wrap)
                sheet.merge_range(row_start , 10, merge_to,10,"", format_wrap)
                sheet.merge_range(row_start , 11, merge_to,11, order_number, format_wrap)
                sheet.merge_range(row_start , 12, merge_to,12, "", format_wrap)
                sheet.merge_range(row_start , 13, merge_to,13, "", format_wrap)

            row_start = merge_to + 1 
