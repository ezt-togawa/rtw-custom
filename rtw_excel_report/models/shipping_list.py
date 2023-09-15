from odoo import models
from datetime import datetime 
import math

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.shipping_list_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format = workbook.add_format({'align': 'center','valign': 'top', 'text_wrap':True, 'border': 1})
        format_wrap = workbook.add_format({'align': 'center','valign': 'top','text_wrap':True, 'border': 1})
        format_date = workbook.add_format({'align': 'center','valign': 'top','text_wrap':True,'num_format': 'yyyy-mm-dd', 'border': 1})
        format_current_date = workbook.add_format({'align': 'center','valign': 'top','text_wrap':True,'num_format': 'yyyy-mm-dd'})
        format_left = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'border': 1})

        format_sheet_title = workbook.add_format({ 
            'align': 'center',
            'valign': 'vcenter',
            'font_size':16,
            'bold': True
            })
        
        format_table = workbook.add_format({ 
            'align': 'center',
            'valign': 'vcenter',
            'border':1,
            'top':1
            })
        
        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + " 年" + month + "月 " + day + "日 "

        sheet_name = f"出荷予定リスト"  
        sheet = workbook.add_worksheet(sheet_name)

        sheet.set_column("A:A", width=4)  
        sheet.set_column("B:B", width=8)  
        sheet.set_column("C:C", width=14)  
        sheet.set_column("D:D", width=8)  
        sheet.set_column("E:E", width=35)  
        sheet.set_column("F:F", width=18)
        sheet.set_column("G:G", width=18)  
        sheet.set_column("H:H", width=6)  
        sheet.set_column("I:I", width=6) 
        sheet.set_column("J:J", width=15) 
        sheet.set_column("K:K", width=15)  
        sheet.set_column("L:L", width=8) 
        sheet.set_column("M:M", width=8)  
        sheet.set_column("N:N", width=12) 
        sheet.set_column("O:O", width=12)  
        sheet.set_column("P:P", width=14)  
        sheet.merge_range(1,6,1,9, "≪出荷予定リスト≫ ", format_sheet_title)
        sheet.write(0,15, current_date, format_current_date)

        #table title
        sheet.merge_range(5, 0,6,0, "№", format_table)
        sheet.merge_range(5, 1,6,1, "出荷日", format_table)
        sheet.merge_range(5, 2,6,2, "受注番号", format_table)
        sheet.merge_range(5, 3,6,3, "作成済", format_table)
        sheet.merge_range(5, 4,6,4, "商品名", format_table)
        sheet.merge_range(5, 5,6,6, "仕様", format_table)
        sheet.merge_range(5, 7,6,7, "数量", format_table)
        sheet.merge_range(5, 8,6,8, "個口", format_table)
        sheet.merge_range(5, 9,6,9, "備考１", format_table)
        sheet.merge_range(5, 10,6,10, "備考２", format_table)
        sheet.merge_range(5, 11,5,12, "着日", format_table)
        sheet.write(6, 11, "白谷", format_table)
        sheet.write(6, 12,"デポ", format_table)
        sheet.merge_range(5, 13,6,14, "送り先", format_table)
        sheet.merge_range(5, 15,6,15, "手段", format_table)

        row=7
        for  index,stock_picking in enumerate(lines):
            sheet.write(row, 0, index+1, format_wrap)
            if stock_picking.confirmed_shipping_date:
                confirmed_shipping_date=str(stock_picking.confirmed_shipping_date).split("-")[1] + "/" + str(stock_picking.confirmed_shipping_date).split("-")[2]
                sheet.write(row, 1, confirmed_shipping_date, format_date)
            else:
                sheet.write(row, 1,"", format_date)

            sheet.write(row, 2,  stock_picking.name, format_wrap)

            if stock_picking.state and (stock_picking.state=='done' or stock_picking.state == 'assigned'):
                sheet.write(row, 3, "済", format_wrap)    
            else:
                sheet.write(row, 3, "未", format_wrap)   

            if stock_picking.partner_id :
                sheet.write(row, 13,stock_picking.partner_id.commercial_company_name , format_wrap)   
                sheet.write(row, 14,stock_picking.partner_id.city + "\n" + stock_picking.partner_id.state_id.name , format_wrap)   
            else:
                sheet.write(row, 13, "", format_wrap)    
                sheet.write(row, 14, "", format_wrap)    

            stock_moves=self.env["stock.move"].search(
                        [("picking_id", "=",stock_picking.id)]
                    )

            p_detail=""
            prod_attrs=""
            qty=""
            packages_number=""
            shiratani_date=""
            depo_date=""
            note=""
            
            for line in stock_moves:
                # p_code=""
                # p_name=""
                # if line.product_id.default_code:
                #     p_code= "[" + line.product_id.default_code + "]"
                # if line.product_id.product_tmpl_id.name:
                #     p_name=line.product_id.product_tmpl_id.name
                # p_detail += p_code + p_name + "\n\n\n\n" 

                attribute = line.product_id.product_template_attribute_value_ids
                if attribute:
                    if len(attribute)==1:
                        prod_attrs +=attribute[0].attribute_id.name + ":" + attribute[0].product_attribute_value_id.name+ "\n\n\n\n" 
                    if len(attribute)==2:
                        prod_attrs += attribute[0].attribute_id.name + ":" + attribute[0].product_attribute_value_id.name+"\n"+ attribute[1].attribute_id.name + ":" + attribute[1].product_attribute_value_id.name +"\n\n\n"                    
                    if len(attribute)==3:
                        prod_attrs += attribute[0].attribute_id.name + ":" + attribute[0].product_attribute_value_id.name+"\n"+ attribute[1].attribute_id.name + ":" + attribute[1].product_attribute_value_id.name +"\n"+ attribute[2].attribute_id.name + ":" + attribute[2].product_attribute_value_id.name +"\n\n" 
                    if len(attribute)>=4:
                        prod_attrs += attribute[0].attribute_id.name + ":" + attribute[0].product_attribute_value_id.name+"\n"+ attribute[1].attribute_id.name + ":" + attribute[1].product_attribute_value_id.name +"\n"+ attribute[2].attribute_id.name + ":" + attribute[2].product_attribute_value_id.name+"\n"+ attribute[3].attribute_id.name + ":" + attribute[3].product_attribute_value_id.name +"\n" 

                if line.product_qty or line.product_qty == 0:
                    qty += str(line.product_qty) + "\n\n\n\n" 

                if line.product_id.two_legs_scale:
                    packages_number +=str( math.ceil(
                        line.product_uom_qty / line.product_id.two_legs_scale
                    ))  + "\n\n\n\n" 
                else:
                    packages_number += str(line.product_uom_qty) + "\n\n\n\n" 

                if stock_picking.note :
                    note +=stock_picking.note

                if line.sale_line_id:
                    sale_lines = self.env["sale.order.line"].search(
                [("id", "=", line.sale_line_id.id)]
                    )
                    if sale_lines:
                        for l in sale_lines:
                            
                            if l.shiratani_date :
                                shiratani_d = str(l.shiratani_date).split("-")
                                shiratani_date += f"{shiratani_d[1]}/{shiratani_d[2]}" + "\n\n\n\n" 
                            if l.depo_date: 
                                depo_d = str(l.depo_date).split("-")
                                depo_date += f"{depo_d[1]}/{depo_d[2]}" + "\n\n\n\n"

            # p_type = "\n"
            # if line.move_id.p_type:
            #     if line.move_id.p_type == "special":
            #         p_type = "\n" + "別注" 
            #     elif line.move_id.p_type == "custom":
            #         p_type = "\n" + "特注"
            if line.product_id.product_tmpl_id.categ_id.name:
                p_detail += str(line.product_id.product_tmpl_id.categ_id.name) +"\n\n\n" 
        
            sheet.write(row, 4,p_detail, format_left)
            sheet.merge_range(row, 5,row,6,prod_attrs , format_left)
            sheet.write(row, 7, qty, format_wrap)
            sheet.write(row, 8,  packages_number, format_wrap)
            sheet.write(row, 9,  note, format)
            sheet.write(row, 10, " ", format)
            sheet.write(row, 11,  shiratani_date, format)
            sheet.write(row, 12,  depo_date, format)
            sheet.write(row, 15,  " ", format_left)
            row += 1
