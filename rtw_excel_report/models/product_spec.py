from odoo import models, _
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
        self = self.with_context(lang=self.env.user.lang)             
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

        def resize_keep_aspect(image_path, target_width):
            img = PILImage.open(image_path).convert('RGB')
            w, h = img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio)
            img = img.resize((target_width, target_height), PILImage.LANCZOS)
            return img

        def resize_contain(image_bytes, frame_w, frame_h):
            img = PILImage.open(io.BytesIO(image_bytes)).convert('RGB')
            w, h = img.size
            ratio = min(frame_w / w, frame_h / h)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), PILImage.LANCZOS)
            background = PILImage.new('RGB', (frame_w, frame_h), (255, 255, 255))
            left = (frame_w - new_w) // 2
            top = (frame_h - new_h) // 2
            background.paste(img, (left, top))
            return background

        def resize_to_square(image_bytes, size):
            img = PILImage.open(io.BytesIO(image_bytes)).convert('RGB')
            w, h = img.size
            if w == 0 or h == 0:
                return PILImage.new('RGB', (size, size), (255, 255, 255))
            min_dimension = min(w, h)
            left = (w - min_dimension) // 2
            top = (h - min_dimension) // 2
            right = left + min_dimension
            bottom = top + min_dimension
            img = img.crop((left, top, right, bottom))
            img = img.resize((size, size), PILImage.LANCZOS)
            return img

        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'R_log.jpg')
        logo_R = resize_keep_aspect(image_logo_R, 86)
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
        format_text_with_bottom_border = workbook.add_format({ 'align': 'left', 'valign': 'top', 'font_name': font_name, 'font_size': 11, 'text_wrap': False, 'bottom': 5, 'bottom_color': '#d9d9d9'})
        
        
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
            sheet.set_header( f'{"&"}R No．{so.name  if so.name else ""}', margin=margin_header) 
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
            sheet.merge_range(1, 5, 3, 11, _("商品仕様書"), format_sheet_title) 
            sheet.merge_range(2, 43, 2, 48, so.sale_order_current_date if so.sale_order_current_date else "", format_date)
            sheet.merge_range(5, 2, 5, 3, _("件名"), format_text)
            sheet.merge_range(5, 4, 5, 48, so.title if so.title else "", format_text_14)
            
            pagebreaks = 0    

            if so.order_line:
                lines = so.order_line.filtered(lambda x: x.display_type not in ['line_note', 'line_section'] and not x.is_pack_outside and x.config_ok)
                length = len(lines)
                if length > 0:
                    more_height = 0 
                    for i,sol in enumerate(lines):
                        try:
                            line_index = so.order_line.ids.index(sol.id)
                        except ValueError:
                            line_index = -1

                        line_note_content = ""
                        if 0 <= line_index < len(so.order_line) - 1:
                            next_line = so.order_line[line_index + 1]
                            if next_line.display_type == 'line_note':
                                line_note_content = next_line.name or ""

                        # if line_note_content:
                            product_pos = (i + 1) % 4
                            height_ln = 0
                            width_ln = 0

                            if product_pos == 1:
                                height_ln = 0
                                width_ln = 0
                            elif product_pos == 2:
                                width_ln = 24
                            elif product_pos == 3:
                                height_ln = 23
                                width_ln = 0
                            elif product_pos == 0:
                                height_ln = 23
                                width_ln = 24

                            row_ln = 28 + height_ln + more_height
                            sheet.set_row(row_ln, 13.8)
                            sheet.merge_range(
                                row_ln, 2 + width_ln,
                                row_ln, 22 + width_ln,
                                line_note_content,
                                format_text_with_bottom_border 
                            )
                            format_border_with_bottom = workbook.add_format({
                                'bg_color': '#d9d9d9',
                                'bottom': 5,
                                'bottom_color': '#d9d9d9'
                            })
                            sheet.write(row_ln, 1 + width_ln, "", format_border_with_bottom)
                            sheet.write(row_ln, 23 + width_ln, "", format_border_with_bottom)

                        pagebreaks += 1
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
                        
                        product_name_with_no = f"No{i} {sol.product_id.name}" if sol.product_id and sol.product_id.name else f"No{i}"
                        sheet.merge_range(7 + height + more_height, 2 + width, 7 + height + more_height, 22 + width, product_name_with_no, format_text_12)
                        
                        # all 12 attributes
                        attr_all = ''
                        if sol.sale_order_product_attr_all:
                            attr_arr = sol.sale_order_product_attr_all.split(',')
                            for a in attr_arr:
                                attr_all += a.strip() + "\n"
                        sheet.merge_range(9 + height + more_height, 16 + width, 23 + height + more_height, 22 + width, attr_all, format_text_top)

                        # price and size
                        price_and_size = ""
                        price = ""
                        size = ""
                        
                        price += _('定価：') + str('{0:,.0f}'.format(sol.price_subtotal))
                        
                        if sol.currency_id.symbol:
                            price += sol.currency_id.symbol
                            
                        if sol.product_size:
                            size = sol.product_size
                        
                        price_and_size += price + '\n'+ _('サイズ：') + size 
                        
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
                                frame_w, frame_h = 185, 110
                                background = resize_contain(image_product_db, frame_w, frame_h)
                                big_img_2 = BytesIO()
                                background.save(big_img_2, 'JPEG')
                                big_img_2.seek(0)

                                sheet.insert_image(
                                    10 + height + more_height,
                                    2 + width,
                                    "test",
                                    {
                                        'image_data': big_img_2,
                                        'x_offset': 0.5,
                                        'y_offset': 0
                                    }
                                ) 
                                
                        # big image 2
                        if sol.item_sale_attach_ids and sol.item_sale_attach_ids[0] and sol.item_sale_attach_ids[0].attach_file:
                            image_product_db = base64.b64decode(sol.item_sale_attach_ids[0].attach_file)
                            if image_product_db:
                                frame_w, frame_h = 175, 110
                                background = resize_contain(image_product_db, frame_w, frame_h)
                                big_img_1 = BytesIO()
                                background.save(big_img_1, 'JPEG')
                                big_img_1.seek(0)

                                sheet.insert_image(
                                    10 + height + more_height,
                                    9 + width,
                                    "test",
                                    {
                                        'image_data': big_img_1,
                                        'x_offset': 10,
                                        'y_offset': 0
                                    }
                                )
   
                        ## 4 picture + 4 attributes
                        if sol.product_id:
                            
                            attr_child_count = 0
                            attr_child_ids =[]
                            img_attr = None
                            attr = ""
                            for parent_attr in sol.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                                if attr_child_count >= 4:
                                    break
                                if parent_attr.id in attr_child_ids or not parent_attr.image:
                                    for child_attr in parent_attr.child_attribute_ids:
                                        if child_attr.image and child_attr.mapped('child_attribute_id') in sol.product_id.product_template_attribute_value_ids.mapped('product_attribute_value_id'):
                                            attr_child_count += 1
                                            attr_child_ids.append(child_attr.child_attribute_id.id)
                                            image_attr_db = base64.b64decode(child_attr.image)
                                            square_size = 60
                                            background = resize_to_square(image_attr_db, square_size)
                                            img_attr = BytesIO()
                                            background.save(img_attr, 'JPEG')
                                            img_attr.seek(0)

                                            attr = (child_attr.child_attribute_id.attribute_id.name + ":" + "\n" + child_attr.child_attribute_id.name)
                                else:
                                    attr_child_count += 1
                                    image_attr_db = base64.b64decode(parent_attr.image)
                                    square_size = 60
                                    background = resize_to_square(image_attr_db, square_size)
                                    img_attr = BytesIO()
                                    background.save(img_attr, 'JPEG')
                                    img_attr.seek(0)

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
                                if img_attr:          
                                   sheet.insert_image(18 + att_height + height + more_height, 2 + att_width + width , "attribute_img", {'image_data': img_attr,'x_offset': 17, 'y_offset': 5})    
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
                                sheet.merge_range(more_height + 1, 5, more_height + 3, 11, _("商品仕様書"), format_sheet_title) 
                                sheet.merge_range(more_height + 2, 43,more_height + 2, 48, so.sale_order_current_date if so.sale_order_current_date else "", format_date)
                                sheet.merge_range(more_height + 5, 2, more_height + 5, 3, _("件名"), format_text)
                                sheet.merge_range(more_height + 5, 4, more_height + 5, 48, so.title if so.title else "", format_text_14)
