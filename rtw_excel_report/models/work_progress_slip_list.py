from odoo import models
from datetime import datetime 

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.work_progress_slip_list_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'center','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_name_company = workbook.add_format({'align': 'center','bottom':1,'font_name': font_name,'font_size':10})
        format_left = workbook.add_format({'align': 'left','text_wrap':True,'font_name': font_name,'font_size':10})

        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC', 'border': 1,'font_name': font_name,'font_size':9})
        format_table_left = workbook.add_format({'align': 'left','valign': 'vcenter','bg_color': '#CCCCCC', 'border': 1,'font_name': font_name,'font_size':9})
        format_wrap = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        format_left_has_border = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        format_right_has_border = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True, 'border': 1,'font_name': font_name,'font_size':9})
        format_date = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'bottom': 1,'font_name': font_name,'font_size':9})
    
        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + " 年 " + month + " 月 " + day + " 日 "

        #number sheet
        company_mrp_prod_name=[]
        for  mrp_prod in lines:
            company_mrp_prod_name.append(mrp_prod.company_id.name)
        unique_name_company=list(set(company_mrp_prod_name))

        #create sheet
        for index,name_company in enumerate(unique_name_company):
            sheet_name = f"仕掛品伝票一覧 - {name_company}"  
            sheet = workbook.add_worksheet(sheet_name)
            sheet.set_column("A:A", width=8,cell_format=font_family)  
            sheet.set_column("B:B", width=18,cell_format=font_family)  
            sheet.set_column("C:C", width=15,cell_format=font_family)  
            sheet.set_column("D:D", width=30,cell_format=font_family)  
            sheet.set_column("E:E", width=15,cell_format=font_family)  
            sheet.set_column("F:F", width=15,cell_format=font_family)
            sheet.set_column("G:G", width=15,cell_format=font_family)  
            sheet.set_column("H:H", width=20,cell_format=font_family)  
            sheet.set_column("I:I", width=30,cell_format=font_family)  
            sheet.set_column("J:J", width=18,cell_format=font_family)  
            sheet.set_column("K:K", width=17,cell_format=font_family) 
            sheet.set_column("L:Z", None,cell_format=font_family) 

            sheet.merge_range(1, 5,1,7, "≪仕掛品伝票一覧≫ ", format_sheet_title)
            sheet.write(0,10, current_date, format_left)
            sheet.write(3, 0, "保管場所", format_name_company)
            sheet.merge_range(3, 1,3,2,name_company, format_name_company)

            #table title
            sheet.write(5, 0, "№", format_table)
            sheet.write(5, 1, "受注No", format_table)
            sheet.write(5, 2, "出荷予定日", format_table)
            sheet.write(5, 3, "品番", format_table_left)
            sheet.write(5, 4, "受注数", format_table)
            sheet.write(5, 5, "製作", format_table)
            sheet.write(5, 6, "工場出荷", format_table)
            sheet.write(5, 7, "部材コード ", format_table_left)
            sheet.write(5, 8, "部材名", format_table_left)
            sheet.write(5, 9, "ロット", format_table)
            sheet.write(5, 10, "使用数", format_table)

            row=6
            for  index,mrp_prod in enumerate(lines):
                if mrp_prod.company_id.name == name_company:
                    sheet.write(row, 0, index+1, format_wrap)
                    sheet.write(row, 1, mrp_prod.name, format_wrap)

                    date_planned_finished=""
                    if mrp_prod.date_planned_finished:
                        date_planned_finished =  mrp_prod.date_planned_finished.strftime("%Y/%m/%d")
                    sheet.write(row, 2,date_planned_finished, format_date)

                    p_name=""
                    if mrp_prod.product_id.product_tmpl_id.product_no:
                        p_name=mrp_prod.product_id.product_tmpl_id.product_no 
                    sheet.write(row, 3, p_name, format_left_has_border)
                
                    sheet.write(row, 4, mrp_prod.product_qty, format_right_has_border)

                    if mrp_prod.qty_producing is None or mrp_prod.qty_producing <=0 : 
                        sheet.write(row, 5, "未", format_wrap)   # 未  chua
                    else:
                        sheet.write(row, 5, "済", format_wrap)   # 済  roi

                    if mrp_prod.state == 'done' : 
                        sheet.write(row, 6, "済", format_wrap)
                    else:
                        sheet.write(row, 6, "未", format_wrap)

                    materials=self.env["stock.move"].search([("reference", "=", mrp_prod.name)])
                    material_code = ""
                    material_name = ""
                    material_lot = ""
                    material_need_to_use=""

                    if materials:
                        for index2,material in enumerate(materials):
                            if material.product_id != mrp_prod.product_id:
                                    if material.product_id.default_code :
                                        material_code += material.product_id.default_code + "\n"
                                    if  material.product_id.product_tmpl_id.name  :
                                        material_name += material.product_id.product_tmpl_id.name + "\n"
                                    if  material.product_qty  :
                                        material_need_to_use += str(material.product_qty) + "\n"

                                    material_lots=self.env["stock.production.lot"].search([("product_id", "=", material.product_id.id)])
                                    if material_lots :
                                        for x in material_lots:
                                            if x.name:
                                                material_lot += x.name + "-"
                                        material_lot=material_lot.rstrip("-")
                                        material_lot +=  "\n"
                                    else:
                                        material_lot +=  "\n"
                            
                    sheet.write(row, 7, material_code, format_left_has_border)
                    sheet.write(row, 8,material_name, format_left_has_border)
                    sheet.write(row, 9, material_lot,format_wrap)
                    sheet.write(row, 10, material_need_to_use, format_right_has_border)
                row += 1
