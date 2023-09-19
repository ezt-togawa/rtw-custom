from odoo import models
import math

class productLabelSticker(models.AbstractModel):
    _name = 'report.rtw_excel_report.product_label_sticker_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet_main = workbook.add_worksheet("商品ラベルシール")
        sheet_main.set_column("A:A", width=0)  
        sheet_main.set_column("B:B", width=15)  
        sheet_main.set_column("D:D", width=5)  
        sheet_main.set_column("F:F", width=15)  
        sheet_main.set_column("G:G", width=4)  
        sheet_main.set_column("J:J", width=5)  
        sheet_main.set_column("H:H", width=15)  
        sheet_main.set_column("L:L", width=15)  
        sheet_main.set_column("M:M", width=0)  

        sheet = workbook.add_worksheet("data")
        merge_format = workbook.add_format({'align': 'center','valign': 'vcenter'})
        format_title = workbook.add_format({'align': 'center','valign': 'top','font_size':24})
        format_detail_prod = workbook.add_format({'align': 'center','valign': 'vcenter','font_size':16})

        r = 0
        r = math.ceil(len(lines) + 9 )
        row_offset = 0  
        for count in range(r):
            row_start = count * 7 + row_offset

            sheet_main.merge_range(row_start + 0, 1, row_start + 2, 5, "=data!A" + str(count * 2 + 1), format_title)
            sheet_main.merge_range(row_start + 0, 7, row_start + 2, 11, "=data!A" + str(count * 2 + 2),format_title)

            sheet_main.merge_range(row_start + 3, 1, row_start + 4, 2, "=data!B" + str(count * 2 + 1), format_detail_prod)
            sheet_main.merge_range(row_start + 3, 7, row_start + 4, 8, "=data!B" + str(count * 2 + 2), format_detail_prod)

            sheet_main.merge_range(row_start + 5, 1, row_start + 6, 2, "=data!C" + str(count * 2 + 1), format_detail_prod)
            sheet_main.merge_range(row_start + 5, 7, row_start + 6, 8, "=data!C" + str(count * 2 + 2), format_detail_prod)

            sheet_main.merge_range(row_start + 3, 4, row_start + 4, 5, "=data!D" + str(count * 2 + 1), format_detail_prod)
            sheet_main.merge_range(row_start + 3, 10, row_start + 4, 11, "=data!D" + str(count * 2 + 2), format_detail_prod)

            sheet_main.merge_range(row_start + 5, 4, row_start + 6, 5, "=data!E" + str(count * 2 + 1), format_detail_prod)
            sheet_main.merge_range(row_start + 5, 10, row_start + 6, 11, "=data!E" + str(count * 2 + 2), format_detail_prod)

            # row_offset is distance every line
            row_offset += 1
        count = 0 
        att=[]
        for obj in lines:
            attrs = obj.product_id.product_template_attribute_value_ids
            if attrs:
                for attri in attrs[:2] :
                    att.append(attri.attribute_id.name + ":" + attri.product_attribute_value_id.name) 

        for _ in range(20):

            # p_type = ""
            # if obj.move_id.p_type:
            #     if obj.p_type == "special":
            #         p_type = "別注"
            #     elif obj.move_id.p_type == "custom":
            #         p_type = "特注"
            prod_name=""
            if obj.product_id.product_tmpl_id.categ_id.name:
                prod_name=obj.product_id.product_tmpl_id.categ_id.name 
                # prod_name=obj.product_id.product_tmpl_id.categ_id.name + "\n" + p_type
                
            sheet.write(count, 0,prod_name , merge_format)
            sheet.write(count, 1, str(obj.name), merge_format)
            sheet.write(count, 2, str(obj.product_qty), merge_format)
            if len(att) == 1:
                sheet.write(count, 3, att[0], merge_format)
            elif len(att) > 1 :
                sheet.write(count, 3, att[0], merge_format)
                sheet.write(count, 4, att[1], merge_format)
            else:
                sheet.write(count, 3, " ", merge_format)
                sheet.write(count, 4, " ", merge_format)
            
            count += 1
