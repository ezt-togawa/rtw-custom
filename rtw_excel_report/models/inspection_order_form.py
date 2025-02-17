from odoo import models, _
from datetime import datetime 
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.inspection_order_form_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, mrp_data):
        self = self.with_context(lang=self.env.user.lang)             
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        logo_R = PILImage.open(image_logo_R)
        logo_R = logo_R.convert('RGB')
        logo_R = logo_R.resize((78, 58))
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        image_logo_ritzwell = get_module_resource('rtw_excel_report', 'img', 'ritzwell.png')
        img_ritzwell = PILImage.open(image_logo_ritzwell)
        img_ritzwell = img_ritzwell.convert('RGB')
        img_ritzwell = img_ritzwell.resize((188, 25))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left', 'valign': 'vcenter', 'font_size':18, 'font_name': font_name,})
        format_text = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':11})
        format_text_right = workbook.add_format({'align': 'right', 'valign': 'top', 'font_name': font_name, 'font_size':11})
        format_text_13 = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':13})
        format_text_13_right = workbook.add_format({'align': 'right', 'font_name': font_name, 'font_size':13})
        format_resend_so = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13,'text_wrap':True})
        format_text_14 = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14})
        format_date = 'yyyy-MM-dd'
        if self.env.user.lang == "ja_JP":
            format_date = 'yyyy年M月d日'
        format_text_date = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':14, 'num_format': format_date})
        format_text_12 = workbook.add_format({'align': 'left', 'font_name': font_name, 'font_size':12})
        format_remark_note = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10})
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':11, 'color':'white','bold':True})
        format_lines_13 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':13, 'bottom':1})
        format_lines_12 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':12, 'bottom':1})
        format_lines_10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':10, 'bottom':1})
        format_lines_9_left= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':9, 'bottom':1})
        format_lines_10_left= workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap':True, 'font_name': font_name, 'font_size':10, 'bottom':1})
        format_lines_custom= workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap':True, 'font_name': font_name, 'font_size':10, 'bottom':1})
        
        allow_print = False
        if len(mrp_data) == 1:
            allow_print = True
        else:   
            for mrp_check in mrp_data[1:]:
                if mrp_check.origin == mrp_data[0].origin:
                    allow_print = True
                else:
                    allow_print = False
                    break
                    
        #create sheet            
        if allow_print :
            for mrp in mrp_data[0]:
                sheet_name = _("検品発注書") 
                sheet = workbook.add_worksheet(sheet_name)
                sheet.set_paper(9)  #A4
                sheet.set_landscape()
                # sheet.set_print_scale(66)
                isLinkeSale = mrp.sale_order_count >= 1

                margin_header = 0.3
                margin_footer = 0.3
                left_margin = 0.8
                right_margin = 0.7
                top_margin = 0.5
                bottom_margin = 0.5
                sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
                if isLinkeSale:
                    sheet.set_header( f'{"&"}R {mrp.sale_order.name  if mrp.sale_order.name else ""} \n {mrp.sale_order.sale_order_current_date  if mrp.sale_order.sale_order_current_date else ""}', margin=margin_header)
                else:
                    current_date = mrp._format_date(datetime.now(), mrp.lang_code, False)
                    sheet.set_header( f'{"&"}R {mrp.name  if mrp.name else ""} \n {current_date if current_date else ""}', margin=margin_header)
                sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)
                
                sheet.set_column("A:A", width=11,cell_format=font_family)  
                sheet.set_column("B:B", width=30,cell_format=font_family)  
                sheet.set_column("C:C", width=30,cell_format=font_family)  
                sheet.set_column("D:D", width=30,cell_format=font_family) 
                sheet.set_column("E:E", width=7,cell_format=font_family)  
                sheet.set_column("F:F", width=5,cell_format=font_family)  
                sheet.set_column("G:G", width=5,cell_format=font_family)
                sheet.set_column("H:H", width=0,cell_format=font_family)  
                sheet.set_column("I:I", width=23,cell_format=font_family)  
                sheet.set_column("J:J", width=26,cell_format=font_family)  
                sheet.set_column("K:K", width=27,cell_format=font_family)  
                sheet.set_column("L:Z", None,cell_format=font_family) 
                
                sheet.set_row(0, 18)
                sheet.set_row(5, 18)
                sheet.set_row(6, 18)
                sheet.set_row(8, 18)
                sheet.set_row(11, 18)
                sheet.set_row(12, 18)
                sheet.set_row(13, 18)
                sheet.set_row(17, 32)
                
                sheet.insert_image(0, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
                sheet.insert_image(1, 9, "logo2", {'image_data': img_io_ritzwell})
                
                # y,x
                sheet.write(1, 8, _('海外')if isLinkeSale and mrp.sale_order.check_oversea else '', format_text_13_right)
                sheet.write(1, 1, _("検品発注書"), format_sheet_title) 
                sheet.write(5, 0, _("発注番号"), format_text) 
                sheet.write(5, 1,  mrp.sale_reference if mrp.sale_reference else mrp.name, format_text) 
                sheet.merge_range(3, 3, 3, 6, mrp.resend_so if mrp.resend_so else "", format_resend_so)
                sheet.write(6, 0, _("配達希望日"), format_text)
                if mrp.is_child_mo:
                    sheet.write(6, 1, mrp.mrp_child_mo_desired_delivery_date if mrp.mrp_child_mo_desired_delivery_date else '', format_text_date) 
                elif mrp.picking_type_id.warehouse_id and mrp.picking_type_id.warehouse_id.name == "糸島工場" :
                    if mrp.mrp_mo_date:
                        sheet.write(6, 1, mrp.mrp_mo_date if mrp.mrp_mo_date else '', format_text_date) 
                    else:
                        so = self.env["sale.order"].search([('name', '=', mrp.sale_reference)], limit=1)
                        if so:
                            sheet.write(6, 1, so.mo_shiratani_entry_date if so.mo_shiratani_entry_date else '', format_text_date)                               
                elif mrp.picking_type_id.warehouse_id and mrp.picking_type_id.warehouse_id.name != "糸島工場" :
                    so = self.env["sale.order"].search([('name', '=', mrp.sale_reference)], limit=1)
                    if so:
                        if mrp.address_ship == '直送':
                            sheet.write(6, 1, so.preferred_delivery_date if so.preferred_delivery_date else '', format_text_date)
                        elif mrp.address_ship == '倉庫' or mrp.address_ship == 'デポ１':
                            sheet.write(6, 1, so.warehouse_arrive_date if so.warehouse_arrive_date else '', format_text_date)
                        elif mrp.address_ship == 'デポ２':
                            sheet.write(6, 1, so.warehouse_arrive_date_2 if so.warehouse_arrive_date_2 else '', format_text_date)
                elif mrp.sale_order.sipping_to == 'direct':

                    sheet.write(6, 1, mrp.sale_order.sale_order_preferred_delivery_date if mrp.sale_order.sale_order_preferred_delivery_date else '', format_text_date) 
                elif isLinkeSale:
                    sheet.write(6, 1, mrp.sale_order.so_warehouse_arrive_date_has_day if mrp.sale_order.so_warehouse_arrive_date_has_day else '', format_text_14) 
                elif not isLinkeSale:
                    sheet.write(6, 1, mrp._format_date(mrp.estimated_shipping_date, mrp.lang_code) if mrp.estimated_shipping_date else '', format_text_date)

                sheet.write(8, 0, _("物件名"), format_text) 
                sheet.write(8, 3, _("送り先注記"), format_text_right)
                
                if mrp.picking_type_id.warehouse_id.partner_id:
                    if mrp.lang_code == "ja_JP":
                        if mrp.mrp_workorder_state == 'wk_001':
                            sheet.write(3, 0, _('糸島工場 御中'), format_text) 
                        elif mrp.mrp_workorder_state == 'wk_002':
                            sheet.write(3, 0, _('品質管理部 御中'), format_text)
                        else:
                            sheet.write(3, 0, mrp.picking_type_id.warehouse_id.partner_id.name + ' 御中', format_text) 
                    else:
                        if mrp.mrp_workorder_state == 'wk_001':
                            sheet.write(3, 0, 'Dear Itoshima Factory', format_text) 
                        elif mrp.mrp_workorder_state == 'wk_002':
                            sheet.write(3, 0, 'Dear Quality Control', format_text)
                        else:
                            sheet.write(3, 0, "Dear " + mrp.picking_type_id.warehouse_id.partner_id.name, format_text)
                
                sheet.write(11, 0, _("送り先"), format_text) 
                
                if mrp.address_ship == "倉庫":
                        sheet.write(12, 0, _("住所"), format_text) 
                        sheet.write(13, 0, _("TEL"), format_text)
                        sheet.write(11, 1, mrp.mrp_choose_option_find_warehouse_company_name if mrp.mrp_choose_option_find_warehouse_company_name else '', format_text_12) 
                        sheet.write(12, 1, mrp.mrp_choose_option_find_warehouse_address if mrp.mrp_choose_option_find_warehouse_address else '', format_text_12) 
                        sheet.write(13, 1, mrp.mrp_choose_option_find_warehouse_phone if mrp.mrp_choose_option_find_warehouse_phone else '', format_text_12)
                sheet.write(12, 0, _("住所"), format_text) 
                sheet.write(13, 0, _("TEL"), format_text)
                if mrp.address_ship and mrp.address_ship == "直送":
                    sheet.write(11, 1, mrp.mrp_production_so_id.shipping_destination_text  if mrp.mrp_production_so_id.shipping_destination_text  else '', format_text_12) 
                    sheet.set_row(12, 0)
                    sheet.set_row(13, 0)
                elif mrp.address_ship and mrp.address_ship == "デポ１":
                        sheet.write(11, 1, mrp.mrp_production_so_id.waypoint.last_name if mrp.mrp_production_so_id.waypoint.last_name else '', format_text_12) 
                        sheet.write(12, 1, mrp.mrp_production_so_id.sale_order_waypoint_address if mrp.mrp_production_so_id.sale_order_waypoint_address else '', format_text_12) 
                        sheet.write(13, 1, mrp.mrp_production_so_id.waypoint.phone if mrp.mrp_production_so_id.waypoint.phone else '', format_text_12)
                elif mrp.address_ship and mrp.address_ship == "デポ２":
                        sheet.write(11, 1, mrp.mrp_production_so_id.waypoint_2.last_name if mrp.mrp_production_so_id.waypoint.last_name else '', format_text_12) 
                        sheet.write(12, 1, mrp.mrp_production_so_id.sale_order_waypoint_address if mrp.mrp_production_so_id.sale_order_waypoint_address else '', format_text_12) 
                        sheet.write(13, 1, mrp.mrp_production_so_id.waypoint_2.phone if mrp.mrp_production_so_id.waypoint.phone else '', format_text_12) 
                sheet.set_row(14, 0)
                sheet.set_row(15, 0)
                
                sheet.write(8, 1, mrp.sale_order.title if isLinkeSale and mrp.sale_order.title else '', format_text_14)
                sheet.write(9, 1, mrp.sale_order.sale_order_info_cus if isLinkeSale and mrp.sale_order.sale_order_info_cus else '', format_text_12)
                
                # y,x,y,x
                sheet.merge_range(8, 4, 11, 7, mrp.mrp_note[:244] if mrp.mrp_note else '', format_remark_note)
                sheet.merge_range(3, 9, 9, 9, mrp.mrp_hr_employee if mrp.mrp_hr_employee else '', format_remark_note)

                #table title
                sheet.write(17, 0, _("№"), format_table)
                sheet.write(17, 1, _("品名"), format_table)
                sheet.write(17, 2, _("仕様・詳細１"), format_table)
                sheet.write(17, 3, _("仕様・詳細２"), format_table)
                sheet.write(17, 4, _("数量"), format_table)
                sheet.write(17, 5, "", format_table)
                sheet.write(17, 6, _("取説"), format_table)
                sheet.write(17, 8, _("Custom"), format_table)
                sheet.write(17, 9, _("メモ"), format_table)
            
            row = 18
            height = 6
            for index,mrp in enumerate(mrp_data):
                sheet.merge_range(row, 0, row + height, 0, index+1, format_lines_10)
                sheet.merge_range(row, 1, row + height, 1, mrp.mrp_product_name_excel, format_lines_9_left)
                
                sheet.merge_range(row, 2, row + height, 2, mrp.mrp_product_attribute, format_lines_10_left)
                sheet.merge_range(row, 3, row + height, 3, mrp.mrp_product_attribute2, format_lines_10_left )
                
                
                sheet.merge_range(row, 4, row + height, 4, mrp.mrp_product_product_qty, format_lines_13)
                
                if mrp.product_id.product_tmpl_id.uom_id.name:
                    sheet.merge_range(row, 5, row + height, 5, mrp.product_id.product_tmpl_id.uom_id.name, format_lines_12)
                else:
                    sheet.merge_range(row, 5, row + height, 5, "", format_lines_12)
                    
                sheet.merge_range(row, 6, row + height, 6, _("有") if mrp.mrp_production_order_line.instruction_status else '', format_lines_13)
                sheet.merge_range(row, 8, row + height, 8, mrp.mrp_product_config_cus_excel, format_lines_custom)
                sheet.merge_range(row, 9, row + height, 9, mrp.production_memo, format_lines_13)
                
                row += height + 1
        else:   
            for mrp in mrp_data[0]:
                sheet_name = _("検品発注書" )
                sheet = workbook.add_worksheet(sheet_name)
                sheet.set_paper(9)  #A4
                sheet.set_landscape()
                # sheet.set_print_scale(66)
                isLinkeSale = mrp.sale_order_count >= 1
                
                margin_header = 0.3
                margin_footer = 0.3
                left_margin = 0.8
                right_margin = 0.7
                top_margin = 0.5
                bottom_margin = 0.5
                sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
                if isLinkeSale:
                    sheet.set_header( f'{"&"}R {mrp.sale_order.name  if mrp.sale_order.name else ""} \n {mrp.sale_order.sale_order_current_date  if mrp.sale_order.sale_order_current_date else ""}', margin=margin_header)
                else:
                    current_date = mrp._format_date(datetime.now(), mrp.lang_code, False)
                sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)
                
                sheet.set_column("A:A", width=11,cell_format=font_family)  
                sheet.set_column("B:B", width=20,cell_format=font_family)  
                sheet.set_column("C:C", width=30,cell_format=font_family)  
                sheet.set_column("D:D", width=30,cell_format=font_family) 
                sheet.set_column("E:E", width=15,cell_format=font_family)  
                sheet.set_column("F:F", width=7.5,cell_format=font_family)  
                sheet.set_column("G:G", width=7.5,cell_format=font_family)
                sheet.set_column("H:H", width=0,cell_format=font_family)  
                sheet.set_column("I:I", width=23,cell_format=font_family)  
                sheet.set_column("J:J", width=26,cell_format=font_family)  
                sheet.set_column("K:K", width=27,cell_format=font_family)  
                sheet.set_column("L:Z", None,cell_format=font_family) 
                
                sheet.set_row(0, 18)
                sheet.set_row(5, 18)
                sheet.set_row(6, 18)
                sheet.set_row(8, 18)
                sheet.set_row(11, 18)
                sheet.set_row(12, 18)
                sheet.set_row(13, 18)
                sheet.set_row(17, 32)
                
                sheet.insert_image(0, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
                sheet.insert_image(1, 9, "logo2", {'image_data': img_io_ritzwell})
                
                # y,x
                sheet.write(1, 8, _("海外") if isLinkeSale and mrp.sale_order.check_oversea else '', format_text_13_right)
                sheet.write(1, 1, _("検品発注書"), format_sheet_title) 
                sheet.write(5, 0, _("発注番号"), format_text) 
                sheet.write(5, 1,  mrp.sale_reference if mrp.sale_reference else mrp.name, format_text)
                sheet.write(6, 0, _("配達希望日"), format_text)
                if isLinkeSale and mrp.is_child_mo:
                    sheet.write(6, 1, mrp.mrp_child_mo_desired_delivery_date if mrp.mrp_child_mo_desired_delivery_date else '', format_text_date) 
                elif isLinkeSale and mrp.sale_order.sipping_to == 'direct':
                    sheet.write(6, 1, mrp.sale_order.sale_order_preferred_delivery_date if mrp.sale_order.sale_order_preferred_delivery_date else '', format_text_date) 
                elif isLinkeSale:
                    sheet.write(6, 1, mrp.sale_order.so_warehouse_arrive_date_has_day if mrp.sale_order.so_warehouse_arrive_date_has_day else '', format_text_14) 
                elif not isLinkeSale:
                    sheet.write(6, 1, mrp._format_date(mrp.estimated_shipping_date, mrp.lang_code) if mrp.estimated_shipping_date else '', format_text_date)

                sheet.write(8, 0, _("物件名"), format_text) 
                sheet.write(8, 3, _("送り先注記"), format_text_right)
                
                if mrp.picking_type_id.warehouse_id.partner_id:
                    if mrp.lang_code == "ja_JP":
                        if mrp.mrp_workorder_state == 'wk_001':
                            sheet.write(3, 0, _('糸島工場 御中'), format_text) 
                        elif mrp.mrp_workorder_state == 'wk_002':
                            sheet.write(3, 0, _('品質管理部 御中'), format_text)
                        else:
                            sheet.write(3, 0, mrp.picking_type_id.warehouse_id.partner_id.name + ' 御中', format_text) 
                    else:
                        if mrp.mrp_workorder_state == 'wk_001':
                            sheet.write(3, 0, 'Dear Itoshima Factory', format_text) 
                        elif mrp.mrp_workorder_state == 'wk_002':
                            sheet.write(3, 0, 'Dear Quality Control', format_text)
                        else:
                            sheet.write(3, 0, "Dear " + mrp.picking_type_id.warehouse_id.partner_id.name, format_text)
            
                sheet.write(11, 0, _("送り先"), format_text) 
                
                if mrp.mrp_production_so_id.sipping_to == 'direct':
                    if mrp.address_ship == "倉庫":
                        sheet.write(12, 0, _("住所"), format_text) 
                        sheet.write(13, 0, _("TEL"), format_text)
                        sheet.write(11, 1, mrp.mrp_choose_option_find_warehouse_company_name if mrp.mrp_choose_option_find_warehouse_company_name else '', format_text_12) 
                        sheet.write(12, 1, mrp.mrp_choose_option_find_warehouse_address if mrp.mrp_choose_option_find_warehouse_address else '', format_text_12) 
                        sheet.write(13, 1, mrp.mrp_choose_option_find_warehouse_phone if mrp.mrp_choose_option_find_warehouse_phone else '', format_text_12)
                    else:
                        sheet.write(11, 1, mrp.mrp_production_so_id.shipping_destination_text  if mrp.mrp_production_so_id.shipping_destination_text  else '', format_text_12) 
                        sheet.set_row(12, 0)
                        sheet.set_row(13, 0)
                else:
                    sheet.write(12, 0, _("住所"), format_text) 
                    sheet.write(13, 0, _("TEL"), format_text)
                    if mrp.address_ship and mrp.address_ship == "デポ/直送":
                        sheet.write(11, 1, mrp.sale_order.sale_order_waypoint_name if isLinkeSale and mrp.sale_order.sale_order_waypoint_name else '', format_text_12)
                        sheet.write(12, 1, mrp.sale_order.sale_order_waypoint_address if isLinkeSale and mrp.sale_order.sale_order_waypoint_address else '', format_text_12)
                        sheet.write(13, 1, mrp.sale_order.waypoint.phone if isLinkeSale and mrp.sale_order.waypoint.phone else '', format_text_12)
                    else:                            
                        sheet.write(11, 1, mrp.mrp_choose_option_find_warehouse_company_name if mrp.mrp_choose_option_find_warehouse_company_name else '', format_text_12) 
                        sheet.write(12, 1, mrp.mrp_choose_option_find_warehouse_address if mrp.mrp_choose_option_find_warehouse_address else '', format_text_12) 
                        sheet.write(13, 1, mrp.mrp_choose_option_find_warehouse_phone if mrp.mrp_choose_option_find_warehouse_phone else '', format_text_12) 
                sheet.set_row(14, 0)
                sheet.set_row(15, 0)
                
                sheet.write(8, 1, mrp.sale_order.title if isLinkeSale and mrp.sale_order.title else '', format_text_14)
                sheet.write(9, 1, mrp.sale_order.sale_order_info_cus if isLinkeSale and mrp.sale_order.sale_order_info_cus else '', format_text_12)
                
                # y,x,y,x
                sheet.merge_range(8, 4, 11, 7, mrp.mrp_note[:244] if mrp.mrp_note else '', format_remark_note)
                sheet.merge_range(3, 9, 9, 9, mrp.mrp_hr_employee if mrp.mrp_hr_employee else '', format_remark_note)

                #table title
                sheet.write(17, 0, _("№"), format_table)
                sheet.write(17, 1, _("品名"), format_table)
                sheet.write(17, 2, _("仕様・詳細１"), format_table)
                sheet.write(17, 3, _("仕様・詳細２"), format_table)
                sheet.write(17, 4, _("数量"), format_table)
                sheet.write(17, 5, "", format_table)
                sheet.write(17, 6, _("取説"), format_table)
                sheet.write(17, 8, _("Custom"), format_table)
                sheet.write(17, 9, _("メモ"), format_table)
            
                row = 18
                height = 6
                sheet.merge_range(row, 0, row + height, 0, 1, format_lines_10)
                sheet.merge_range(row, 1, row + height, 1, mrp.mrp_product_name_excel, format_lines_9_left)
                
                sheet.merge_range(row, 2, row + height, 2, mrp.mrp_product_attribute, format_lines_10_left)
                sheet.merge_range(row, 3, row + height, 3, mrp.mrp_product_attribute2, format_lines_10_left )
                
                
                sheet.merge_range(row, 4, row + height, 4, mrp.mrp_product_product_qty, format_lines_13)
                
                if mrp.product_id.product_tmpl_id.uom_id.name:
                    sheet.merge_range(row, 5, row + height, 5, mrp.product_id.product_tmpl_id.uom_id.name, format_lines_12)
                else:
                    sheet.merge_range(row, 5, row + height, 5, "", format_lines_12)
                    
                sheet.merge_range(row, 6, row + height, 6, _("有") if mrp.mrp_production_order_line.instruction_status else '', format_lines_13)
                sheet.merge_range(row, 8, row + height, 8, mrp.mrp_product_config_cus_excel, format_lines_10_left)
                sheet.merge_range(row, 9, row + height, 9, mrp.production_memo, format_lines_13)
