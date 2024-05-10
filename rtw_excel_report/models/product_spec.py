from odoo import models
from odoo.modules.module import get_module_resource

from datetime import datetime 
import base64
from PIL import Image
import io
import os
import shutil

from io import BytesIO
from PIL import Image as PILImage
class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.product_spec_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, so_data):
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
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

        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        logo_R = PILImage.open(image_logo_R)
        logo_R = logo_R.convert('RGB')
        logo_R = logo_R.resize((70, 45))
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name})
        format_text = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':10, 'text_wrap':True})
        format_text_top = workbook.add_format({'align': 'left', 'valign': 'top', 'font_name': font_name, 'font_size':10, 'text_wrap':True})
        format_text_top_size9 = workbook.add_format({'align': 'left', 'valign': 'top', 'font_name': font_name, 'font_size':9, 'text_wrap':True})
        format_text_center_size9 = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':9, 'text_wrap':True})
        format_text_bottom_center = workbook.add_format({'align': 'center', 'valign': 'bottom', 'font_name': font_name, 'font_size':8, 'text_wrap':True})
        format_date = workbook.add_format({'align': 'right','font_name': font_name,'font_size':9})
        format_text_14 = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':14})
        format_text_12 = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_name': font_name, 'font_size':12})
        
        format_border = workbook.add_format({'bg_color': '#d9d9d9'})
        #create sheet
        for index,so in enumerate(so_data):
            sheet_name = f"{so.name}" 
            sheet= workbook.add_worksheet(sheet_name)
            sheet.set_paper(9)  #A4
            sheet.set_landscape()
            sheet.set_print_scale(71)
            
            margin_header = 0.3
            margin_footer = 0.3
            left_margin = 0.8
            right_margin = 0.7
            top_margin = 0.5
            bottom_margin = 0.5
            sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
            sheet.set_header( f'{"&"}R {so.name  if so.name else ""}', margin=margin_header) 
            sheet.set_footer(f'{"&"}L page{" "}{"&"}P/{"&"}N',margin=margin_footer)    
                    
            sheet.set_column("A:A", width=0.81, cell_format=font_family)  
            sheet.set_column("B:B", width=0.63, cell_format=font_family)  
            sheet.set_column("C:H", width=3.67, cell_format=font_family)  
            sheet.set_column("I:I", width=0.63, cell_format=font_family)  
            sheet.set_column("J:O", width=3.67, cell_format=font_family)  
            sheet.set_column("P:P", width=0.63, cell_format=font_family)
            sheet.set_column("Q:W", width=3.67, cell_format=font_family)
            sheet.set_column("X:X", width=0.63, cell_format=font_family)
            sheet.set_column("Y:Y", width=1.22, cell_format=font_family)
            sheet.set_column("Z:Z", width=0.63, cell_format=font_family)
            sheet.set_column("AA:AF", width=3.67, cell_format=font_family)
            sheet.set_column("AG:AG", width=0.63, cell_format=font_family)
            sheet.set_column("AH:AM", width=3.67, cell_format=font_family)
            sheet.set_column("AN:AN", width=0.63, cell_format=font_family)
            sheet.set_column("AO:AU", width=3.67, cell_format=font_family)
            sheet.set_column("AV:AV", width=0.63, cell_format=font_family)
            sheet.set_column("AW:AW", width=0.81, cell_format=font_family)
            
            sheet.set_row(0, 14.4)
            sheet.set_row(1, 14.4)
            sheet.set_row(2, 14.4)
            sheet.set_row(3, 14.4)
            sheet.set_row(4, 5.4)
            
            
            sheet.set_row(5, 22.2)
            
            # row 7 -> row 28
            sheet.set_row(6, 6)
            sheet.set_row(7, 24)
            sheet.set_row(8, 6)
            sheet.set_row(9, 13.8)
            sheet.set_row(10, 13.8)
            sheet.set_row(11, 13.8)
            sheet.set_row(12, 13.8)
            sheet.set_row(13, 13.8)
            sheet.set_row(14, 13.8)
            sheet.set_row(15, 13.8)
            sheet.set_row(16, 13.8)
            sheet.set_row(17, 6)
            sheet.set_row(18, 13.8)
            sheet.set_row(19, 13.8)
            sheet.set_row(20, 13.8)
            sheet.set_row(21, 13.8)
            sheet.set_row(22, 6)
            sheet.set_row(23, 13.8)
            sheet.set_row(24, 13.8)
            sheet.set_row(25, 13.8)
            sheet.set_row(26, 13.8)
            sheet.set_row(27, 6)
            
            # space
            sheet.set_row(28, 10.8)
            
            # row 30 -> row 51
            sheet.set_row(29, 6)
            sheet.set_row(30, 24)
            sheet.set_row(31, 6)
            sheet.set_row(32, 13.8)
            sheet.set_row(33, 13.8)
            sheet.set_row(34, 13.8)
            sheet.set_row(35, 13.8)
            sheet.set_row(36, 13.8)
            sheet.set_row(37, 13.8)
            sheet.set_row(38, 13.8)
            sheet.set_row(39, 13.8)
            sheet.set_row(40, 6)
            sheet.set_row(41, 13.8)
            sheet.set_row(42, 13.8)
            sheet.set_row(43, 13.8)
            sheet.set_row(44, 13.8)
            sheet.set_row(45, 6)
            sheet.set_row(46, 13.8)
            sheet.set_row(47, 13.8)
            sheet.set_row(48, 13.8)
            sheet.set_row(49, 13.8)
            sheet.set_row(50,6)
            
            sheet.set_row(51, 13.8)
            sheet.set_row(52, 14.4)
            sheet.set_row(53, 14.4)
            
            sheet.insert_image(1, 2, "logo", {'image_data': img_io_R, 'x_offset': 0, 'y_offset': 0})
            # y,x,y,x
            sheet.merge_range(1, 5, 3, 11, "商品仕様書", format_sheet_title) 
            sheet.merge_range(2, 43, 2, 48, so.sale_order_current_date if so.sale_order_current_date else "", format_date)
            sheet.merge_range(5, 2, 5, 3, "件名", format_text)
            sheet.merge_range(5, 4, 5, 48, so.title if so.title else "", format_text_14)
            
            pagebreaks = 0    

            if so.order_line:
                length = len(so.order_line.filtered(lambda x: not x.is_pack_outside))
                
                if length > 0:
                    more_height = 0 
                    for i,sol in enumerate(so.order_line.filtered(lambda x: not x.is_pack_outside)):
                        height = 0
                        width = 0
                        i = i+1
                        
                        if i % 4 == 1:
                            height = 0
                            width = 0
                        elif i % 4 == 2:
                            width = 24 
                        elif i % 4 == 3:
                            height = 23
                        elif i % 4 == 0:
                            height = 23
                            width = 24 
                        
                        # border
                        sheet.merge_range(6 + height + more_height, 2 + width, 6 + height + more_height, 22 + width, "", format_border)
                        sheet.merge_range(8 + height + more_height, 2 + width, 8 + height + more_height, 22 + width, "", format_border)
                        sheet.merge_range(17 + height + more_height, 2 + width, 17 + height + more_height, 14 + width, "", format_border)
                        sheet.merge_range(22 + height + more_height, 2 + width, 22 + height + more_height, 14 + width, "", format_border)
                        sheet.merge_range(27 + height + more_height, 2 + width, 27 + height + more_height, 22 + width, "", format_border)
                                        
                        sheet.merge_range(6 + height + more_height, 1 + width, 27 + height + more_height, 1 + width, "", format_border)
                        sheet.merge_range(6 + height + more_height, 23 + width, 27 + height + more_height, 23 + width, "", format_border)
                                        
                        sheet.merge_range(9 + height + more_height, 8 + width, 16 + height + more_height, 8 + width, "", format_border)
                        sheet.merge_range(18 + height + more_height, 8 + width, 21 + height + more_height, 8 + width, "", format_border)
                        sheet.merge_range(23 + height + more_height, 8 + width, 26 + height + more_height, 8 + width, "", format_border)
                                        
                        sheet.merge_range(9 + height + more_height, 15 + width, 26 + height + more_height, 15 + width, "", format_border)
                        
                        # name product
                        sheet.merge_range(7 + height + more_height, 2 + width, 7 + height + more_height, 22 + width, sol.name if sol.name else "", format_text_12)
                        
                        # all 12 attribute
                        sheet.merge_range(9 + height + more_height, 16 + width, 23 + height + more_height , 22 + width , sol.sale_order_all_attribute if sol.sale_order_all_attribute else "", format_text_top)
                        
                        # price and size
                        price_and_size = ""
                        price = ""
                        size = ""
                        size2 = ""
                        size3 = ""
                        if sol.price_subtotal:
                            price += '定価：'+ str('{0:,.0f}'.format(sol.price_subtotal))
                        
                        if price and sol.currency_id.symbol:
                            price += sol.currency_id.symbol
                            
                        if sol.product_id:
                            prod_tmpl = sol.product_id.product_tmpl_id
                            if prod_tmpl:
                                
                                if prod_tmpl.width:
                                    size += ("W" + str(int(prod_tmpl.width)) + "x")
                                if prod_tmpl.depth:
                                    size += ("D" + str(int(prod_tmpl.depth)) + "x")
                                if prod_tmpl.height:
                                    size += ("H" + str(int(prod_tmpl.height)) + "x")
                                    
                                if prod_tmpl.ah:
                                    size2 += ("AH" + str(int(prod_tmpl.ah)) + "x")
                                    size3 += "SH" + str(int(prod_tmpl.sh))
                                    
                                if prod_tmpl.sh:
                                    size2 += ("SH" + str(int(prod_tmpl.sh)) + "x")
                                    size3 += "AH" + str(int(prod_tmpl.ah)) + " "
                                    
                        size = size.strip('x')
                        size2 = size2.strip('x')
                        size3 = size3.strip(' ')

                        if price and size and size2:
                            price_and_size += price + '\n'+ 'サイズ：' + size + '\n' + '                ' + size2
                        elif price and size:
                            price_and_size +=  price + '\n'+ 'サイズ：' + size 
                        elif price and size2:
                            price_and_size +=  price + '\n'+ 'サイズ：' + size2
                        elif size and size2:
                            price_and_size += 'サイズ：' + size + '\n' + '                ' + size2
                        elif price:
                            price_and_size +=  price
                        elif size:
                            price_and_size +=  'サイズ：' + size 
                        elif size2:
                            price_and_size +=  'サイズ：' + size2 
                        sheet.merge_range(24 + height + more_height, 16 + width, 26 + height + more_height, 22 + width , price_and_size if price_and_size else "", format_text_top_size9)
                        
                        #empty bg image 1 
                        sheet.merge_range(9 + height + more_height, 2 + width, 16 + height + more_height, 7 + width , "", format_text)
                        #empty bg  image 2 
                        sheet.merge_range(9 + height + more_height, 9 + width, 16 + height + more_height, 14 + width , "", format_text)
                        
                        #empty bg image attribute1 
                        sheet.merge_range(18 + height + more_height, 2 + width, 21 + height + more_height, 4 + width , "", format_text)
                        #empty bg image attribute2
                        sheet.merge_range(18 + height + more_height, 9 + width, 21 + height + more_height, 11 + width , "", format_text)
                        #empty bg image attribute3
                        sheet.merge_range(23 + height + more_height, 2 + width, 26 + height + more_height, 4 + width , "", format_text)
                        #empty bg image attribute4
                        sheet.merge_range(23 + height + more_height, 9 + width, 26 + height + more_height, 11 + width , "", format_text)
                        
                        #empty bg text attribute1 
                        sheet.merge_range(18 + height + more_height, 5 + width, 21 + height + more_height, 7 + width , "", format_text)
                        #empty bg text attribute2
                        sheet.merge_range(18 + height + more_height, 12 + width, 21 + height + more_height, 14 + width , "", format_text)
                        #empty bg text attribute3
                        sheet.merge_range(23 + height + more_height, 5 + width, 26 + height + more_height, 7 + width , "", format_text)
                        #empty bg text attribute4
                        sheet.merge_range(23 + height + more_height, 12 + width, 26 + height + more_height, 14 + width , "", format_text)
                        
                        
                        # big image 1
                        if sol.product_id.image_256:
                            image_product_db = base64.b64decode(sol.product_id.image_256)
                            if image_product_db:
                                image = Image.open(io.BytesIO(image_product_db))
                                image_path = os.path.join(image_product, f"sol_{sol.id}_big_img2.png")
                                image.save(image_path, 'PNG')
                                img = PILImage.open(image_path)
                                img = img.convert('RGB')
                                img = img.resize((185, 110))
                                big_img_2 = BytesIO()
                                img.save(big_img_2, 'JPEG')
                                big_img_2.seek(2)
                                sheet.insert_image(10 + height + more_height, 2 + width,"test",{'image_data': big_img_2,'x_offset': 0.5, 'y_offset': 0})  
                                
                        # big image 2
                        if sol.item_sale_attach_ids and sol.item_sale_attach_ids[0] and sol.item_sale_attach_ids[0].attach_file:
                            image_product_db = base64.b64decode(sol.item_sale_attach_ids[0].attach_file)
                            if image_product_db:
                                image = Image.open(io.BytesIO(image_product_db))
                                image_path = os.path.join(image_product, f"sol_{sol.id}_big_img1.png")
                                image.save(image_path, 'PNG')
                                img = PILImage.open(image_path)
                                img = img.convert('RGB')
                                img = img.resize((164, 110))
                                big_img_1 = BytesIO()
                                img.save(big_img_1, 'JPEG')
                                big_img_1.seek(2)
                                sheet.insert_image(10 + height + more_height, 9 + width,"test",{'image_data': big_img_1,'x_offset': 10, 'y_offset': 0})    

                                
                        # if need size under big image2    
                        # size_of_image1 = ""
                        # if size and size3:
                        #     size_of_image1 += size + ' ' +  size3
                        # elif size:
                        #     size_of_image1 += size 
                        # elif size3:
                        #     size_of_image1 += size3
                        # sheet.write(9 + height + more_height, 2 + width, size_of_image1 if size_of_image1 else "", format_text_bottom_center)

                                
                        ## 4 picture + 4 attributes
                        if sol.product_id:
                            
                            attr_child_count = 0
                            attr_child_ids =[]
                            for parent_attr in sol.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                                if attr_child_count >= 4:
                                    break
                                
                                if parent_attr.id in attr_child_ids or not parent_attr.image:
                                    for child_attr in parent_attr.child_attribute_ids:
                                        if child_attr.image and child_attr.mapped('child_attribute_id') in sol.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                                            attr_child_count += 1
                                            attr_child_ids.append(child_attr.child_attribute_id.id)
                                            # attributes picture            
                                            image_attr_db= base64.b64decode(child_attr.image)
                                            image = Image.open(io.BytesIO(image_attr_db))
                                            path = os.path.join(image_attribute_product, f"sol_{sol.id}_attr_{attr_child_count}.png")
                                            image.save(path, 'PNG')
                                            img = PILImage.open(path)
                                            img = img.convert('RGB')
                                            img = img.resize((70, 60))
                                            img_attr = BytesIO()
                                            img.save(img_attr, 'JPEG')
                                            img_attr.seek(2)
                                            # attributes value
                                            attr = child_attr.child_attribute_id.attribute_id.name + ":" + "\n" + child_attr.child_attribute_id.name
                                else:
                                    attr_child_count += 1
                                    # attributes picture            
                                    image_attr_db= base64.b64decode(parent_attr.image)
                                    image = Image.open(io.BytesIO(image_attr_db))
                                    path = os.path.join(image_attribute_product, f"sol_{sol.id}_attr_{attr_child_count}.png")
                                    image.save(path, 'PNG')
                                    img = PILImage.open(path)
                                    img = img.convert('RGB')
                                    img = img.resize((70, 60))
                                    img_attr = BytesIO()
                                    img.save(img_attr, 'JPEG')
                                    img_attr.seek(2)
                                    # attributes value
                                    attr = parent_attr.attribute_id.name + ":" + "\n" + parent_attr.name
                                    
                                att_height = 0
                                att_width = 0
                                if attr_child_count == 2:
                                    att_width = 7
                                elif attr_child_count == 3:
                                    att_height = 5
                                elif attr_child_count == 4:
                                    att_height = 5
                                    att_width = 7
                                # attributes picture write excel             
                                sheet.insert_image(18 + att_height + height + more_height, 2 + att_width + width , "attribute_img", {'image_data': img_attr,'x_offset': 11, 'y_offset': 7})    
                                # attributes value write excel 
                                sheet.write(18 + att_height + height + more_height, 5 + att_width + width, attr, format_text_center_size9)
                                            
                            #break page 
                            if i % 4 == 0:
                                pagebreaks += 52
                                more_height += 52
                                sheet.set_h_pagebreaks([pagebreaks])
                                
                                sheet.set_row(more_height + 0, 14.4)
                                sheet.set_row(more_height + 1, 14.4)
                                sheet.set_row(more_height + 2, 14.4)
                                sheet.set_row(more_height + 3, 14.4)
                                sheet.set_row(more_height + 4, 5.4)
                                
                                
                                sheet.set_row(more_height + 5, 22.2)
                                
                                # row 7 -> row 28
                                sheet.set_row(more_height + 6, 6)
                                sheet.set_row(more_height + 7, 24)
                                sheet.set_row(more_height + 8, 6)
                                sheet.set_row(more_height + 9, 13.8)
                                sheet.set_row(more_height + 10, 13.8)
                                sheet.set_row(more_height + 11, 13.8)
                                sheet.set_row(more_height + 12, 13.8)
                                sheet.set_row(more_height + 13, 13.8)
                                sheet.set_row(more_height + 14, 13.8)
                                sheet.set_row(more_height + 15, 13.8)
                                sheet.set_row(more_height + 16, 13.8)
                                sheet.set_row(more_height + 17, 6)
                                sheet.set_row(more_height + 18, 13.8)
                                sheet.set_row(more_height + 19, 13.8)
                                sheet.set_row(more_height + 20, 13.8)
                                sheet.set_row(more_height + 21, 13.8)
                                sheet.set_row(more_height + 22, 6)
                                sheet.set_row(more_height + 23, 13.8)
                                sheet.set_row(more_height + 24, 13.8)
                                sheet.set_row(more_height + 25, 13.8)
                                sheet.set_row(more_height + 26, 13.8)
                                sheet.set_row(more_height + 27, 6)
                                
                                # space
                                sheet.set_row(more_height + 28, 10.8)
                                
                                # row 30 -> row 51
                                sheet.set_row(more_height + 29, 6)
                                sheet.set_row(more_height + 30, 24)
                                sheet.set_row(more_height + 31, 6)
                                sheet.set_row(more_height + 32, 13.8)
                                sheet.set_row(more_height + 33, 13.8)
                                sheet.set_row(more_height + 34, 13.8)
                                sheet.set_row(more_height + 35, 13.8)
                                sheet.set_row(more_height + 36, 13.8)
                                sheet.set_row(more_height + 37, 13.8)
                                sheet.set_row(more_height + 38, 13.8)
                                sheet.set_row(more_height + 39, 13.8)
                                sheet.set_row(more_height + 40, 6)
                                sheet.set_row(more_height + 41, 13.8)
                                sheet.set_row(more_height + 42, 13.8)
                                sheet.set_row(more_height + 43, 13.8)
                                sheet.set_row(more_height + 44, 13.8)
                                sheet.set_row(more_height + 45, 6)
                                sheet.set_row(more_height + 46, 13.8)
                                sheet.set_row(more_height + 47, 13.8)
                                sheet.set_row(more_height + 48, 13.8)
                                sheet.set_row(more_height + 49, 13.8)
                                sheet.set_row(more_height + 50,6)
                                
                                sheet.set_row(more_height + 51, 13.8)
                                sheet.set_row(more_height + 52, 14.4)
                                sheet.set_row(more_height + 53, 14.4)
                                
                                sheet.insert_image(more_height + 1, 2, "logo", {'image_data': img_io_R, 'x_offset': 0, 'y_offset': 0})
                                # y,x,y,x
                                sheet.merge_range(more_height + 1, 5, more_height + 3, 11, "商品仕様書", format_sheet_title) 
                                sheet.merge_range(more_height + 2, 43,more_height + 2, 48, so.sale_order_current_date if so.sale_order_current_date else "", format_date)
                                sheet.merge_range(more_height + 5, 2, more_height + 5, 3, "件名", format_text)
                                sheet.merge_range(more_height + 5, 4, more_height + 5, 48, so.title if so.title else "", format_text_14)
