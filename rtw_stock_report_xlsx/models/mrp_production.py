from odoo import models
from odoo.modules.module import get_module_resource
import xlrd
import xlsxwriter
import math

class MrpProductionXlsx(models.AbstractModel):
    _name = 'report.rtw_stock_report_xlsx.mrp_production_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        # text_file_path = get_module_resource('rtw_stock_report_xlsx', 'static', 'seal_template.xlsx')
        # print(text_file_path)
        # workbook = xlsxwriter.Workbook(text_file_path)
        sheet_main = workbook.add_worksheet("印刷")
        sheet = workbook.add_worksheet("data")
        bold = workbook.add_format({'bold': True})
        merge_format = workbook.add_format({'align': 'center'})
        page_count = 1
        r = 0
        c = 0
        r = math.ceil(len(lines)+12/2)
        print(r)
        for count in range(r):
            sheet_main.merge_range(count*7+0, 0, count*7+2, 5, "=data!A"+str(count*2+1), merge_format)
            sheet_main.merge_range(count*7+0, 7, count*7+2, 12, "=data!A"+str(count*2+2), merge_format)

            sheet_main.merge_range((count * 7) + 3, 0, count * 7 + 4, 2, "=data!C" + str(count * 2 + 1), merge_format)
            sheet_main.merge_range((count * 7) + 3, 7, count * 7 + 4, 9, "=data!C" + str(count * 2 + 2), merge_format)

            sheet_main.merge_range((count * 7) + 5, 0, count * 7 + 6, 2, "=data!D" + str(count * 2 + 1), merge_format)
            sheet_main.merge_range((count * 7) + 5, 7, count * 7 + 6, 9, "=data!D" + str(count * 2 + 2), merge_format)

            sheet_main.merge_range((count * 7) + 3, 3, count * 7 + 6, 5, "=data!B" + str(count * 2 + 1), merge_format)
            sheet_main.merge_range((count * 7) + 3, 10, count * 7 + 6, 12, "=data!B" + str(count * 2 + 2), merge_format)
        for count, obj in enumerate(lines):
            #データシート
            sheet.write(count, 0, obj.product_id.name, bold)
            # for l in obj.product_template_attribute_value_ids:
            x = ",".join(str(v.name) for v in obj.product_id.product_template_attribute_value_ids)
            sheet.write(count, 1, x, bold)
            sheet.write(count, 2, obj.origin, bold)
            sheet.write(count, 3, obj.product_qty, bold)
            #メインシート

            if (count+1) % 2 == 0:
                pos = 7
            else:
                pos = 0
            # sheet_main.merge_range(math.ceil((count+1)/2)*7-7, pos,
            #                        2+(math.ceil((count+1)/2)*7)-7, pos + 5,
            #                        obj.product_id.name,
            #                        merge_format)
            page_count += 1
        # for obj in partners:
        #     report_name = "test"
            # One sheet by partner
            # sheet = workbook.add_worksheet("Sheet1")
            # bold = workbook.add_format({'bold': True})
            # sheet.write(0, 0, "Sheet1", bold)
