from odoo import models, _
from datetime import datetime 
import math
class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.shipping_list_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)         
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        # different format  width font 
        format_sheet_title = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name})
        format_current_date = workbook.add_format({'align': 'center', 'valign': 'top', 'num_format': 'yyyy-mm-dd', 'font_size':10, 'font_name': font_name})

        format_table = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border':1, 'top':1, 'font_size':9, 'font_name': font_name})
        format_wrap = workbook.add_format({'align': 'center', 'valign': 'top', 'text_wrap':True, 'border': 1, 'font_size':9, 'font_name': font_name})
        format_left = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'border': 1, 'font_size':9, 'font_name': font_name})
        format_attr = workbook.add_format({'align': 'left', 'valign': 'top', 'border': 1, 'font_size':9, 'text_wrap':True, 'font_size':9, 'font_name': font_name})

        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + _(" 年 ") + month + _(" 月 ") + day + _(" 日")

        sheet = workbook.add_worksheet(_('出荷予定リスト'))
        
        sheet.set_column("A:A", width=4, cell_format=font_family)  
        sheet.set_column("B:B", width=5, cell_format=font_family)  
        sheet.set_column("C:C", width=14 ,cell_format=font_family)  
        sheet.set_column("D:D", width=5, cell_format=font_family ) 
        sheet.set_column("E:E", width=30, cell_format=font_family)  
        sheet.set_column("F:F", width=15, cell_format=font_family)
        sheet.set_column("G:G", width=15, cell_format=font_family)  
        sheet.set_column("H:H", width=4, cell_format=font_family)  
        sheet.set_column("I:I", width=4, cell_format=font_family)
        sheet.set_column("J:J", width=12, cell_format=font_family) 
        sheet.set_column("K:K", width=12, cell_format=font_family)  
        sheet.set_column("L:L", width=8, cell_format=font_family )
        sheet.set_column("M:M", width=8, cell_format=font_family ) 
        sheet.set_column("N:N", width=12, cell_format=font_family ) 
        sheet.set_column("O:O", width=12, cell_format=font_family )  
        sheet.set_column("P:P", width=14, cell_format=font_family )  
        sheet.set_column("Q:Z", None, cell_format=font_family )  
        
        sheet.merge_range(1, 6, 1, 9, _("≪出荷予定リスト≫ "), format_sheet_title)
        sheet.write(0, 15, current_date, format_current_date)

        #table title
        sheet.merge_range(5, 0, 6, 0, _("№"), format_table)
        sheet.merge_range(5, 1, 6, 1, _("出荷日"), format_table)
        sheet.merge_range(5, 2, 6, 2, _("受注番号"), format_table)
        sheet.merge_range(5, 3, 6, 3, _("作成済"), format_table)
        sheet.merge_range(5, 4, 6, 4, _("商品名"), format_table)
        sheet.merge_range(5, 5, 6, 6, _("仕様"), format_table)
        sheet.merge_range(5, 7, 6, 7, _("数量"), format_table)
        sheet.merge_range(5, 8, 6, 8, _("個口"), format_table)
        sheet.merge_range(5, 9, 6, 9, _("備考１"), format_table)
        sheet.merge_range(5, 10, 6, 10, _("備考２"), format_table)
        sheet.merge_range(5, 11, 5, 12, _("着日"), format_table)
        sheet.write(6, 11, _("白谷"), format_table)
        sheet.write(6, 12, _("デポ"), format_table)
        sheet.merge_range(5, 13, 6, 14, _("送り先"), format_table)
        sheet.merge_range(5, 15, 6, 15, _("手段"), format_table)

        row_start=7
        merge_to = 7
        
        row_inside = 7
        for index,stock_picking in enumerate(lines):
            confirmed_shipping_date= ""
            order_number= ""
            status = ""
            company_name= ""
            city = ""
            state = ""

            if stock_picking.confirmed_shipping_date:
                confirmed_shipping_date =  stock_picking.confirmed_shipping_date.strftime("%m/%d")

            if stock_picking.name:
                order_number= stock_picking.name

            # if stock_picking.state and (stock_picking.state=='done' or stock_picking.state == 'assigned'):
            if stock_picking.state and (stock_picking.state=='done'):
                status = _("済") 
            else:
                status = _("未") 
            
            if stock_picking.partner_id.commercial_company_name :
                company_name = stock_picking.partner_id.commercial_company_name
            else:
                if stock_picking.partner_id.name :
                    company_name = stock_picking.partner_id.name
            
            if stock_picking.partner_id.city :
                city = stock_picking.partner_id.city 
            if stock_picking.partner_id.state_id.name :
                state = stock_picking.partner_id.state_id.name

            prod_name = ""
            attrs = ""
            prod_qty = 0
            note = ""
            shiratani_date = ""
            depo_date = ""
            
            stock_moves = self.env["stock.move"].search([("picking_id", "=",stock_picking.id)])
            if stock_moves :
                for line in stock_moves:
                    if line.product_id.product_tmpl_id.categ_id.name:
                        prod_name = line.product_id.product_tmpl_id.categ_id.name

                    prod = self.env["product.product"].search([("id", "=", line.product_id.id)])
                    attribute = prod.product_template_attribute_value_ids

                    if attribute:
                        len_attr = len(attribute)
                        if len_attr == 2:
                            sheet.set_row(row_inside, height=30)
                        elif len_attr == 3:
                            sheet.set_row(row_inside, height=40)
                        elif len_attr >= 4:
                            sheet.set_row(row_inside, height=50)
                        
                        attrs = "\n".join(f"{attr.attribute_id.name}:{attr.product_attribute_value_id.name}" for attr in attribute[:4])
                    
                    if line.product_qty :
                        prod_qty = line.product_qty

                    if stock_picking.note :
                        note = stock_picking.note

                    if line.sale_line_id:
                        sale_lines = self.env["sale.order.line"].search([("id", "=", line.sale_line_id.id)])
                        if sale_lines:
                            for l in sale_lines:
                                if l.shiratani_date :
                                    shiratani_split = str(l.shiratani_date).split("-")
                                    shiratani_date = f"{shiratani_split[1]}/{shiratani_split[2]}"
                                if l.depo_date: 
                                    depo_date_split = str(l.depo_date).split("-")
                                    depo_date = f"{depo_date_split[1]}/{depo_date_split[2]}"

                    sheet.write(row_inside, 4 , prod_name, format_left)
                    sheet.merge_range(row_inside, 5, row_inside, 6, attrs, format_attr)
                    sheet.write(row_inside, 7, prod_qty, format_wrap)
                    sheet.write(row_inside, 8, line.product_package_quantity if line.product_package_quantity else 0, format_wrap)

                    row_inside += 1
            else:
                sheet.write(row_inside, 4 , prod_name, format_left)
                sheet.merge_range(row_inside, 5, row_inside, 6, attrs, format_attr)
                sheet.write(row_inside, 7, prod_qty, format_wrap)
                sheet.write(row_inside, 8, 0, format_wrap)

                row_inside += 1
                    
            merge_to  = row_inside - 1

            if row_start == merge_to:
                sheet.write(row_start, 0, index+1, format_wrap)
                sheet.write(row_start, 1, confirmed_shipping_date, format_wrap)
                sheet.write(row_start, 2, order_number, format_wrap)
                sheet.write(row_start, 3, status, format_wrap)
                sheet.write(row_start, 9, note, format_wrap)
                sheet.write(row_start, 10, "", format_wrap)
                sheet.write(row_start, 11, shiratani_date, format_wrap)
                sheet.write(row_start, 12, depo_date ,format_wrap)
                sheet.write(row_start, 13, company_name ,format_wrap)
                sheet.write(row_start, 14, city + "\n" + state, format_wrap)
                sheet.write(row_start, 15, "", format_wrap)
            else:
                sheet.merge_range(row_start, 0, merge_to, 0, index+1, format_wrap)
                sheet.merge_range(row_start, 1, merge_to, 1, confirmed_shipping_date, format_wrap)
                sheet.merge_range(row_start, 2, merge_to, 2, order_number, format_wrap)
                sheet.merge_range(row_start, 3, merge_to, 3, status, format_wrap)
                sheet.merge_range(row_start, 9, merge_to, 9, note, format_wrap)
                sheet.merge_range(row_start, 10, merge_to, 10,"", format_wrap)
                sheet.merge_range(row_start, 11, merge_to, 11, shiratani_date, format_wrap)
                sheet.merge_range(row_start, 12, merge_to, 12, depo_date ,format_wrap)
                sheet.merge_range(row_start, 13, merge_to, 13, company_name, format_wrap)
                sheet.merge_range(row_start, 14, merge_to, 14, city + "\n" + state, format_wrap)
                sheet.merge_range(row_start, 15, merge_to, 15, "", format_wrap)

            row_start = merge_to + 1
