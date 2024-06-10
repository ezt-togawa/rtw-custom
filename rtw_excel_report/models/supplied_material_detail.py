from odoo import models, _
from datetime import datetime 
from odoo.modules.module import get_module_resource
from io import BytesIO
from PIL import Image as PILImage
import math

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.supplied_material_detail_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)         
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        format_wrap = workbook.add_format({'align': 'center','valign': 'top','text_wrap':True, 'border': 1,'font_size':10,'font_name': font_name})
        format_size10 = workbook.add_format({'align': 'center','valign': 'top','font_size':10,'text_wrap':True,'border': 1,'font_name': font_name})
        format_left = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True, 'border': 1,'font_size':10,'font_name': font_name})
        format_current_date = workbook.add_format({'align': 'right','valign': 'right','text_wrap':True,'num_format': 'yyyy-mm-dd','font_size':10,'font_name': font_name})
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'top':1,'text_wrap':True,'font_size':10,'font_name': font_name})
        format_title = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True,'bg_color':"yellow",'font_size':18,'bold':True,'font_name': font_name})
        format_table_yellow = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'top':1,'text_wrap':True,'bg_color':"yellow",'font_size':10,'font_name': font_name})
        format_bold_left = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True,'bold':True,'bottom':1,'font_name': font_name})
        format_bold_left2 = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True,'bold':True,'font_name': font_name})
        format_add_user_login = workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True,'font_size':8,'font_name': font_name})

        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + _(" 年 ") + month + _(" 月 ") + day + _(" 日 ")


        sheet_name = _("張地支給明細")  
        sheet = workbook.add_worksheet(sheet_name)
        sheet.set_column("A:A", width=7,cell_format=font_family)   
        sheet.set_column("B:B", width=15,cell_format=font_family)   
        sheet.set_column("C:C", width=25,cell_format=font_family)   
        sheet.set_column("D:D", width=25,cell_format=font_family)   
        sheet.set_column("E:E", width=15,cell_format=font_family)   
        sheet.set_column("F:F", width=4,cell_format=font_family) 
        sheet.set_column("G:G", width=12,cell_format=font_family)  
        sheet.set_column("H:H", width=15,cell_format=font_family)  
        sheet.set_column("I:Z", None,cell_format=font_family) 
        sheet.merge_range(1,3,3,4, _("張地支給明細 "), format_title)
        sheet.merge_range(0,6,0,7, current_date, format_current_date)
        sheet.write(7,0, _("届先名"), format_bold_left)
        sheet.write(9,0, _("月日"), format_bold_left)
        
        #table title
        sheet.merge_range(12, 0,13,0, _("№"), format_table)
        sheet.merge_range(12, 1,13,1, _("受注番号"), format_table_yellow)
        sheet.merge_range(12, 2,13,2, _("物件名"), format_table)
        sheet.merge_range(12, 3,13,3, _("部材名"), format_table_yellow)
        sheet.merge_range(12, 4,13,4, _("納期"), format_table_yellow)
        sheet.merge_range(12, 5,13,6, _("ロット"), format_table)
        sheet.merge_range(12, 7,13,7, _("要尺"), format_table_yellow)

        row_no_merge = 14
        row_remember=14
        merge_to = 14

        company_name=""
        confirmed_shipping_date=""
        address=""
        phone=""
        responsible=""

        image_logo = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        img = PILImage.open(image_logo)
        img = img.convert('RGB')
        img = img.resize((35, 40))
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(2)
        sheet.insert_image(5,5,"logo",{'image_data': img_io})
        
        login_user_name=self.env.user
        if login_user_name.partner_id.state_id.name:
            address += login_user_name.partner_id.state_id.name + " "
        if login_user_name.partner_id.city:
            address += login_user_name.partner_id.city
        if login_user_name.partner_id.street:
            address += login_user_name.partner_id.street
        if login_user_name.partner_id.zip:
            address += login_user_name.partner_id.zip
        phone = login_user_name.partner_id.phone
        responsible = login_user_name.partner_id.name
        
        sheet.merge_range(6, 6, 6, 7, _("株式会社 リッツウェル"), format_bold_left2)
        sheet.merge_range(7, 5, 7, 7, address, format_add_user_login)
        sheet.merge_range(8, 5, 8, 6, _("TEL: ") + phone, format_add_user_login)
        sheet.merge_range(9, 5, 9, 6, _("担当: ") + responsible, format_add_user_login)

        for  index,stock_picking in enumerate(lines):
            if stock_picking.partner_id.commercial_company_name:
                company_name=stock_picking.partner_id.commercial_company_name 
            elif stock_picking.partner_id.name:
                company_name=stock_picking.partner_id.name 
                
            if stock_picking.lang_code == "ja_JP":
                company_name +=  "様"
            else:
                company_name = "Mr/Mrs. " + company_name
                    
            if stock_picking.confirmed_shipping_date:
                confirmed_shipping_date= str(stock_picking.confirmed_shipping_date).split("-")[0] + _(" 年 ") + str(stock_picking.confirmed_shipping_date).split("-")[1] + _(" 月 ") + str(stock_picking.confirmed_shipping_date).split("-")[2]

            sheet.merge_range(7,1,7,2,company_name, format_bold_left)
            sheet.write(9,1,confirmed_shipping_date, format_bold_left)
            
            order_number=" "
            sale_title=" "
            lot=" "
            confirmed_shipping_date=" "
            prod_tmpl=" "
            package=0
            
            if stock_picking.confirmed_shipping_date:
                confirmed_shipping_date=str(stock_picking.confirmed_shipping_date).split("-")[1] + _(" 月 ") + str(stock_picking.confirmed_shipping_date).split("-")[2] + _(" 日 ")

            if stock_picking.name:
                order_number= stock_picking.name

            if stock_picking.sale_id.name:
                sale_title= stock_picking.sale_id.name

            stock_moves=self.env["stock.move"].search([("picking_id", "=",stock_picking.id)])

            if stock_moves :
                for line in stock_moves:
                    
                    if line.product_id.two_legs_scale and line.product_uom_qty:
                        package= math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
                    else:
                        if line.product_uom_qty :
                            package = line.product_uom_qty   

                    if line.product_id.product_tmpl_id.name:
                        prod_tmpl=line.product_id.product_tmpl_id.name

                    stock_inventory_lines=self.env["stock.inventory.line"].search([("product_id", "=",line.product_id.id)])
                    #has lot
                    for line in stock_inventory_lines:
                        if line.prod_lot_id.name:
                            lot += line.prod_lot_id.name +'\n'
                    lot=lot.rstrip("\n")
                    sheet.merge_range(row_no_merge, 5 ,row_no_merge, 6 , lot, format_size10)
    
                    
                    sheet.write(row_no_merge, 3, prod_tmpl, format_left)
                    sheet.write(row_no_merge , 7, package, format_wrap)

                    row_no_merge += 1
    
                merge_to=merge_to + len(stock_moves)-1
                if(len(stock_moves)==1):
                    sheet.write(row_remember , 0, index+1, format_wrap)
                    sheet.write(row_remember , 1, order_number, format_wrap)
                    sheet.write(row_remember , 2, sale_title, format_wrap)
                    sheet.write(row_remember , 4, confirmed_shipping_date, format_wrap)
                else:
                    sheet.merge_range(row_remember , 0, merge_to,0, index+1, format_wrap)
                    sheet.merge_range(row_remember , 1, merge_to,1, order_number, format_wrap)
                    sheet.merge_range(row_remember , 2, merge_to,2, sale_title, format_wrap)
                    sheet.merge_range(row_remember , 4, merge_to,4, confirmed_shipping_date, format_wrap)
            else :
                stock_move_lines=self.env["stock.move.line"].search([("picking_id", "=",stock_picking.id)])
                # if stock_move_lines :
                for line in stock_move_lines:
                        
                        if line.product_id.two_legs_scale and line.product_uom_qty:
                            package= math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
                        else:
                            if line.product_uom_qty :
                                package = line.product_uom_qty 

                        if line.product_id.product_tmpl_id.name:
                            prod_tmpl=line.product_id.product_tmpl_id.name

                        stock_inventory_lines=self.env["stock.inventory.line"].search([("product_id", "=",line.product_id.id)])
                        #has lot
                        for line in stock_inventory_lines:
                            if line.prod_lot_id.name:
                                lot += line.prod_lot_id.name +'\n'
                        lot=lot.rstrip("\n")
                        sheet.merge_range(row_no_merge, 5 ,row_no_merge, 6 , lot, format_size10)
                    
                        sheet.write(row_no_merge, 3, prod_tmpl, format_left)
                        sheet.write(row_no_merge , 7, package, format_wrap)

                        row_no_merge += 1

                merge_to=merge_to + len(stock_move_lines)-1

                if(len(stock_move_lines)==1):
                    sheet.write(row_remember , 0, index+1, format_wrap)
                    sheet.write(row_remember , 1, order_number, format_wrap)
                    sheet.write(row_remember , 2, sale_title, format_wrap)
                    sheet.write(row_remember , 4, confirmed_shipping_date, format_wrap)
                else:
                    sheet.merge_range(row_remember , 0, merge_to,0, index+1, format_wrap)
                    sheet.merge_range(row_remember , 1, merge_to,1, order_number, format_wrap)
                    sheet.merge_range(row_remember , 2, merge_to,2, sale_title, format_wrap)
                    sheet.merge_range(row_remember , 4, merge_to,4, confirmed_shipping_date, format_wrap)

            merge_to = merge_to + 1 
            row_remember = merge_to 
