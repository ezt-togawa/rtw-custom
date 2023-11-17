from odoo import models
from odoo.modules.module import get_module_resource

import math
from datetime import datetime 
import base64
from PIL import Image
import io
import os
import shutil

from io import BytesIO
from PIL import Image as PILImage
import math

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.product_spec_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_product = os.path.join(current_directory, "img_product")
        image_attribute_product = os.path.join(current_directory, "img_attribute_product")

        if os.path.exists(image_product):
            shutil.rmtree(image_product)
            os.makedirs(image_product)
        else:
            os.makedirs(image_product)

        if os.path.exists(image_attribute_product):
            shutil.rmtree(image_attribute_product)
            os.makedirs(image_attribute_product)
        else:
            os.makedirs(image_attribute_product)

        sheet_main = workbook.add_worksheet("商品仕様書(EXCEL)")
        sheet = workbook.add_worksheet("data")

        bold = workbook.add_format({'bold': True})
        wrap_format = workbook.add_format({'text_wrap': True,'align': 'center','valign': 'vcenter'})
        merge_format = workbook.add_format({'align': 'center','valign': 'vcenter'})
        merge_format_left = workbook.add_format({'align': 'left','valign': 'vcenter'})
        
        r = ""
        # image main of product
        image_logo = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        img = PILImage.open(image_logo)
        img = img.convert('RGB')
        img = img.resize((70, 70))
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(2)

        #current time
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = year + " 年 " + month + " 月 " + day + " 日 "
        
        # template number
        r = math.ceil(len(lines.order_line)/4)

        row_logo=0
        row_title=2
        col_title=1
        row_print_time=0
        col_print_time=17
        col_title_name=5
        row_title_name_db=5
        col_title_name_db=1

        order_title =""
        for sale_order in lines:
            if sale_order.title:
                order_title=sale_order.title
        sheet_main.merge_range(row_title_name_db, col_title_name_db, row_title_name_db, col_title_name_db+1,order_title, merge_format)

        sheet_main.insert_image(row_logo,0,"logo",{'image_data': img_io})
        sheet_main.merge_range(row_title, col_title, row_title, col_title+1, "商品仕様書", merge_format)
        sheet_main.write(row_print_time, col_print_time,current_date , merge_format)
        sheet_main.write(col_title_name, 0,"商品", merge_format)

        for count in range(r):
                
            sheet_main.merge_range(count*52 + 8, 0, count*52+9, 0, "=data!A"+str(count * 4+1), merge_format)
            sheet_main.merge_range(count*52 + 8, 5, count*52+9, 5, "=data!A"+str(count* 4+2), merge_format)
            sheet_main.merge_range(count*52 + 8, 10, count*52+9, 10, "=data!A"+str(count * 4+3), merge_format)
            sheet_main.merge_range(count*52 + 8, 15, count*52+9, 15, "=data!A"+str(count * 4+4), merge_format)
            
            sheet_main.merge_range((count * 52) + 8, 1, count * 52 + 8, 3, "=data!B" + str(count * 4 + 1), merge_format_left)
            sheet_main.merge_range((count * 52) + 8, 6, count * 52 + 8, 8, "=data!B" + str(count * 4 + 2), merge_format_left)
            sheet_main.merge_range((count * 52) + 8, 11, count * 52 + 8, 13, "=data!B" + str(count * 4 + 3), merge_format_left)
            sheet_main.merge_range((count * 52) + 8, 16, count * 52 + 8, 18, "=data!B" + str(count * 4 + 4), merge_format_left)
            
            sheet_main.merge_range((count * 52) + 9, 1, count * 52 + 9, 3, "=data!C" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 9,6, count * 52 + 9, 8, "=data!C" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 9,11, count * 52 + 9, 13, "=data!C" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 9,16, count * 52 + 9, 18, "=data!C" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 10, 0, count * 52 + 22, 3, "=data!D" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 10, 5, count * 52 + 22, 8, "=data!D" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 10, 10, count * 52 + 22, 13, "=data!D" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 10, 15, count * 52 + 22, 18, "=data!D" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 23, 0, count * 52 + 30, 3, "=data!E" + str(count * 4 + 1), wrap_format)
            sheet_main.merge_range((count * 52) + 23, 5, count * 52 + 30, 8, "=data!E" + str(count * 4 + 2), wrap_format)
            sheet_main.merge_range((count * 52) + 23, 10, count * 52 + 30, 13, "=data!E" + str(count * 4 + 3), wrap_format)
            sheet_main.merge_range((count * 52) + 23, 15, count * 52 + 30, 18, "=data!E" + str(count * 4 + 4), wrap_format)
            
            # #attribute image
            sheet_main.merge_range((count * 52) + 31, 0, count * 52 + 36, 1, "=data!F" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 31, 5, count * 52 + 36, 6, "=data!F" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 31, 10, count * 52 + 36, 11, "=data!F" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 31, 15, count * 52 + 36, 16, "=data!F" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 31, 2, count * 52 + 36, 3, "=data!G" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 31, 7, count * 52 + 36, 8, "=data!G" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 31, 12, count * 52 + 36, 13, "=data!G" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 31, 17, count * 52 + 36, 18, "=data!G" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 39, 0, count * 52 + 44, 1, "=data!H" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 39, 5, count * 52 + 44, 6, "=data!H" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 39, 10, count * 52 + 44, 11, "=data!H" + str(count * 4 +  3), merge_format)
            sheet_main.merge_range((count * 52) + 39, 15, count * 52 + 44, 16, "=data!H" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 39, 2, count * 52 + 44, 3, "=data!I" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 39, 7, count * 52 + 44, 8, "=data!I" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 39, 12, count * 52 + 44, 13, "=data!I" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 39, 17, count * 52 + 44, 18, "=data!I" + str(count * 4 + 4), merge_format)

            # #attribute detail 
            sheet_main.merge_range((count * 52) + 37, 0, count * 52 + 38, 1, "=data!J" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 37, 5, count * 52 + 38, 6, "=data!J" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 37, 10, count * 52 + 38, 11, "=data!J" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 37, 15, count * 52 + 38, 16, "=data!J" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 37, 2, count * 52 + 38, 3, "=data!K" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 37, 7, count * 52 + 38, 8, "=data!K" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 37, 12, count * 52 + 38, 13, "=data!K" + str(count * 4 +  3), merge_format)
            sheet_main.merge_range((count * 52) + 37, 17, count * 52 + 38, 18, "=data!K" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 45, 0, count * 52 + 46, 1, "=data!L" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 45, 5, count * 52 + 46, 6, "=data!L" + str(count * 4 + 2), merge_format)
            sheet_main.merge_range((count * 52) + 45, 10, count * 52 + 46, 11, "=data!L" + str(count * 4 + 3), merge_format)
            sheet_main.merge_range((count * 52) + 45, 15, count * 52 + 46, 16, "=data!L" + str(count * 4 + 4), merge_format)

            sheet_main.merge_range((count * 52) + 45, 2, count * 52 + 46, 3, "=data!M" + str(count * 4 + 1), merge_format)
            sheet_main.merge_range((count * 52) + 45, 7, count * 52 + 46, 8, "=data!M" + str(count * 4 +2), merge_format)
            sheet_main.merge_range((count * 52) + 45, 12, count * 52 + 46, 13, "=data!M" + str(count * 4 +  3), merge_format)
            sheet_main.merge_range((count * 52) + 45, 17, count * 52 + 46, 18, "=data!M" + str(count * 4 + 4), merge_format)

            sheet.write(count, 5, " ", wrap_format)
            sheet.write(count, 6, " ", wrap_format)
            sheet.write(count, 7, " ", wrap_format)
            sheet.write(count, 8, " ", wrap_format)

            sheet.write(count, 9, " ", wrap_format)
            sheet.write(count, 10, " ", wrap_format)
            sheet.write(count, 11, " ", wrap_format)
            sheet.write(count, 12, " ", wrap_format)
        count = 0  

        for sale_order in lines:
            sale_order_lines=self.find_sale_order_line(sale_order.id)
            if sale_order_lines :
                for index,sl in enumerate(sale_order_lines.filtered(lambda x: not x.is_pack_outside)):
                    prod_name=""
                    p_type=""
                    if sl.product_id.product_tmpl_id.categ_id.name:
                        prod_name = sl.product_id.product_tmpl_id.categ_id.name 
                    if sl.p_type:
                        if sl.p_type == "special":
                            p_type = "別注"
                        elif sl.p_type == "custom":
                            p_type = "特注"    

                    sheet.write(index, 0,sl.product_uom_qty, bold)
                    sheet.write(index, 1, prod_name + " " + p_type, wrap_format)
                    sheet.write(index, 2,"ダイアナ:" + str(sl.price_total), bold)

                    if sl.product_id.image_256:
                        image_product_db = base64.b64decode(sl.product_id.image_256)
                        if image_product_db:
                            image = Image.open(io.BytesIO(image_product_db))
                            image_path = os.path.join(image_product, f"{sl.id}.png")
                            image.save(image_path, 'PNG')
                            img = PILImage.open(image_path)
                            img = img.convert('RGB')
                            img = img.resize((252, 252))
                            img_io = BytesIO()
                            img.save(img_io, 'JPEG')
                            img_io.seek(2)

                            count = index // 4  # col number attribute, even when past 4 col so count + 1
                            row = 10 + count * 52
                            col = (index % 4) * 5

                            sheet_main.insert_image(row,col,"test",{'image_data': img_io})
                            
                    attributes = sl.product_id.product_template_attribute_value_ids
                    attr=""
                    if attributes:
                        for attribute in attributes :
                            attr += attribute.attribute_id.name + ":" + attribute.product_attribute_value_id.name + "\n"
                            sheet.write(index, 4, attr, wrap_format)
                        
                        # take first 4 element of record
                        attrs_has_img = [x for x in sl.product_id.product_template_attribute_value_ids if x.product_attribute_value_id.image][:4]

                        if attrs_has_img:
                            for index2,attr_img in enumerate(attrs_has_img) : 
                                image_attr_db= base64.b64decode(attr_img.product_attribute_value_id.image)
                                image = Image.open(io.BytesIO(image_attr_db))
                                path = os.path.join(image_attribute_product, f"{sl.id}_{index2}.png")
                                image.save(path, 'PNG')
                                img = PILImage.open(path)
                                img = img.convert('RGB')
                                img = img.resize((125, 125))
                                img_io = BytesIO()
                                img.save(img_io, 'JPEG')
                                img_io.seek(2)

                                # loop image with recipe
                                count_attr_img = index // 4  
                                row_attr_img = 31 + count_attr_img * 52
                                col_attr_img = (index % 4)*5

                                if index2 == 1:
                                    col_attr_img += 2
                                elif index2 == 2:
                                    row_attr_img +=8
                                elif index2 == 3:
                                    row_attr_img +=8
                                    col_attr_img += 2
                                
                                # image attribute 
                                sheet_main.insert_image(row_attr_img, col_attr_img,"test",{'image_data': img_io})
                                sheet.write(count, 5, " ", wrap_format)
                                sheet.write(count, 6, " ", wrap_format)
                                sheet.write(count, 7, " ", wrap_format)
                                sheet.write(count, 8, " ", wrap_format)
                                # detail attribute 
                                if attr_img.attribute_id.name and attr_img.product_attribute_value_id.name:
                                    sheet.write(index, index2+9,attr_img.attribute_id.name + ":" + attr_img.product_attribute_value_id.name + "\n", bold)    
                    else:
                        sheet.write(index, 4, " ", wrap_format)
                        
    def find_sale_order_line(self,order_id):
        return self.env["sale.order.line"].search([("order_id", "=", order_id)])
