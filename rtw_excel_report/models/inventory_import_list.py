from odoo import models
from datetime import datetime 

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.inventory_import_list_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        format = workbook.add_format({'align': 'center','valign': 'vcenter','font_name': font_name})
        format_sheet_title = workbook.add_format({ 'align': 'center','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_current_date = workbook.add_format({'align': 'left','text_wrap':True,'font_name': font_name,'font_size':10})
        format_name_company = workbook.add_format({'align': 'center','bottom':1,'font_name': font_name,'font_size':10})
        format_left = workbook.add_format({'align': 'left','text_wrap':True,'font_name': font_name,'font_size':10})
        format_right = workbook.add_format({'align': 'right','text_wrap':True,'font_name': font_name,'font_size':10})
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC', 'border': 1,'font_name': font_name,'font_size':9})

        format_wrap = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        format_left_has_border = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        format_right_has_border = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        
        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + " 年 " + month + " 月 " + day + " 日 "

        #number sheet
        company_name=[]
        for  stock_quant in lines:
            company_name.append(stock_quant.company_id.name)
        unique_company_name=list(set(company_name))

        #create sheet
        for index,name_company in enumerate(unique_company_name):
            sheet_name = f"棚卸記入リスト - {name_company}"  
            sheet = workbook.add_worksheet(sheet_name)

            sheet.set_column("A:A", width=8,cell_format=font_family) 
            sheet.set_column("B:B", width=12,cell_format=font_family) 
            sheet.set_column("C:C", width=26,cell_format=font_family) 
            sheet.set_column("D:D", width=14,cell_format=font_family) 
            sheet.set_column("E:E", width=16,cell_format=font_family) 
            sheet.set_column("F:F", width=14,cell_format=font_family)
            sheet.set_column("G:G", width=15,cell_format=font_family) 
            sheet.set_column("H:H", width=15,cell_format=font_family) 
            sheet.set_column("I:I", width=15,cell_format=font_family) 
            sheet.set_column("J:J", width=20,cell_format=font_family) 
            sheet.set_column("K:Z", None,cell_format=font_family)

            sheet.merge_range(1,3,1,5, "≪棚卸記入リスト≫ ", format_sheet_title)
            sheet.write(0,9, current_date, format_current_date)
            sheet.write(3, 0, "保管場所", format_name_company)
            sheet.merge_range(3, 1,3,2,name_company, format_name_company)

            sheet.write(3, 6, "担当（", format_right)
            sheet.merge_range(3, 7,3,8, "", format)
            sheet.write(3, 9, ")", format_left)

            #table title
            sheet.merge_range(5, 0,6,0, "№", format_table)
            sheet.merge_range(5, 1,6,1, "部材コード", format_table)
            sheet.merge_range(5, 2,6,2, "部材名", format_table)
            sheet.merge_range(5, 3,6,3, "ロット", format_table)
            sheet.merge_range(5, 4,6,4, "帳簿在庫数", format_table)
            sheet.merge_range(5, 5,6,5, "製作中在庫", format_table)
            sheet.merge_range(5, 6,6,6, "実在庫", format_table)
            sheet.merge_range(5, 7,5,8, "棚卸実数 ", format_table)
            sheet.write(6, 7, "製作中", format_table)
            sheet.write(6, 8, "棚卸数", format_table)
            sheet.merge_range(5, 9, 6, 9, "ﾁｪｯｸ", format_table)

            row=7
            for  index,stock_quant in enumerate(lines):
                material_lot=""

                if stock_quant.company_id.name == name_company:
                    sheet.write(row, 0, index+1, format_wrap)
                    sheet.write(row, 1,  stock_quant.product_id.default_code, format_left_has_border)
                    sheet.write(row, 2,  stock_quant.product_id.product_tmpl_id.name, format_left_has_border)

                    material_lots=self.env["stock.production.lot"].search(
                                [("product_id", "=", stock_quant.product_id.id)]
                            )
                    if material_lots :
                        for x in material_lots:
                            material_lot += x.name + " "
                            material_lot +=  "\n"
                    else:
                        material_lot +=  "\n"
                    sheet.write(row, 3, material_lot , format_wrap)

                    sheet.write(row, 4, stock_quant.quantity , format_wrap)
                    sheet.write(row, 6, stock_quant.quantity - stock_quant.reserved_quantity , format_wrap)
                    sheet.write(row, 5,stock_quant.quantity -(stock_quant.quantity - stock_quant.reserved_quantity ) , format_wrap)

                    sheet.write(row, 7, "ｾｯﾄ" ,format_right_has_border)
                    sheet.write(row, 8, "ｾｯﾄ" , format_right_has_border)
                    sheet.write(row, 9, "" , format_left_has_border)
                row += 1
