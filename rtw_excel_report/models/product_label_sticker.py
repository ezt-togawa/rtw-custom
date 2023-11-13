from odoo import models

class productLabelSticker(models.AbstractModel):
    _name = "report.rtw_excel_report.product_label_sticker_xls"
    _inherit = "report.report_xlsx.abstract"

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

        format_title = workbook.add_format({"align": "center", "valign": "vcenter", "font_size": 26,"shrink": True })
        format_detail_prod = workbook.add_format({"align": "center", "valign": "vcenter", "font_size": 16,"shrink": True})

        location_item_row = 1

        last_mrp_prod = self.env["mrp.location_item_excel_prod_label"].search([], order="create_date desc", limit=1)
        if last_mrp_prod:
            location_item_row = last_mrp_prod.location_item_row
            records_to_delete = self.env["mrp.location_item_excel_prod_label"].search([("create_date", "<", last_mrp_prod.create_date)])
            if records_to_delete:
                records_to_delete.unlink()
        else: 
            location_item_row = 1
        row_start_begin = (location_item_row - 1) // 2 * 9

        count = 0
    
        for obj in lines:
            prod_name = ""
            mrp_name =""
            mrp_qty =""
            scheduled_date_month = ""
            scheduled_date_day = ""
            attributes = []

            if obj.product_id.product_tmpl_id.product_no:
                prod_name = obj.product_id.product_tmpl_id.product_no

            if obj.name:
                mrp_name = obj.name

            if obj.product_uom_qty:
                mrp_qty = str(obj.product_uom_qty).split(".")[0]

            if obj.date_planned_start:
                scheduled_date_month = obj.date_planned_start.strftime("%m")
                scheduled_date_day = obj.date_planned_start.strftime("%d")

            attrs = obj.product_id.product_template_attribute_value_ids
            if attrs:
                for attri in attrs[:2]:
                    attributes.append(attri.attribute_id.name + ":" + attri.product_attribute_value_id.name )

            row_start = row_start_begin +  count * 9
            if location_item_row % 2 != 0 :  # location odd 
                sheet_main.merge_range(row_start + 0,1,row_start + 2,5,prod_name ,format_title)
                sheet_main.merge_range(row_start + 3,1,row_start + 4,2,mrp_name ,format_detail_prod)
                sheet_main.merge_range(row_start + 5,1,row_start + 6,2,mrp_qty + "(Ｒ " + scheduled_date_month + "月" + scheduled_date_day + "日）" ,format_detail_prod)
                sheet_main.merge_range(row_start + 3,4,row_start + 4,5,attributes[0] if len(attributes)== 1 or len(attributes)== 2  else " " ,format_detail_prod)
                sheet_main.merge_range(row_start + 5,4,row_start + 6,5,attributes[1]  if len(attributes)== 2 else " ",format_detail_prod)
            else :  # location even
                sheet_main.merge_range(row_start + 0,7,row_start + 2,11,prod_name,format_title)
                sheet_main.merge_range(row_start + 3,7,row_start + 4,8,mrp_name ,format_detail_prod)
                sheet_main.merge_range(row_start + 5,7,row_start + 6,8,mrp_qty + "(Ｒ " + scheduled_date_month + "月" + scheduled_date_day + "日）" ,format_detail_prod)
                sheet_main.merge_range(row_start + 3,10,row_start + 4,11,attributes[0] if len(attributes)== 1 or len(attributes)== 2  else " " ,format_detail_prod)
                sheet_main.merge_range(row_start + 5,10,row_start + 6,11,attributes[1]  if len(attributes)== 2 else " " ,format_detail_prod)
                count += 1
            
            location_item_row += 1
