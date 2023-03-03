from odoo import models


class StockMoveLineXlsx(models.AbstractModel):
    _name = 'report.rtw_stock_report_xlsx.stock_move_line_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Sheet1")
        bold = workbook.add_format({'bold': True})
        for count, obj in enumerate(lines):
            print(obj.product_id.name)
            sheet.write(count, 0, obj.product_id.name, bold)
        # for obj in partners:
        #     report_name = "test"
            # One sheet by partner
            # sheet = workbook.add_worksheet("Sheet1")
            # bold = workbook.add_format({'bold': True})
            # sheet.write(0, 0, "Sheet1", bold)
