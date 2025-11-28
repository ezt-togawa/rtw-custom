from odoo import models , _
from odoo.modules.module import get_module_resource
from PIL import Image as PILImage
from io import BytesIO
from datetime import datetime 
from itertools import groupby
from collections import defaultdict
from operator import itemgetter
from odoo.http import content_disposition, request, route
class ReportMrpExcel(models.AbstractModel):
    _name = 'report.rtw_excel_report.report_purchase_order_for_part_xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, objects):
        
        purchase_order = None
        if objects._name == 'purchase.order':
            purchase_order = objects
        else:
            if len(objects) > 1:
                today_str = datetime.now().strftime('%Y-%m-%dT%H%M%S')
                report = request.env["ir.actions.report"]._get_report_from_name("rtw_excel_report.purchase_order_line_for_part_xls")
                # if not report.report_file:
                report.write({'report_file':"発注書(部材用) -" + today_str})
            purchase_order = objects.order_id
        self = self.with_context(lang=self.env.user.lang)             
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})
        
        image_logo_R = get_module_resource('rtw_excel_report', 'img', 'logo.png')
        logo_R = PILImage.open(image_logo_R)
        logo_R = logo_R.convert('RGB')
        logo_R = logo_R.resize((86, 62))
        img_io_R = BytesIO()
        logo_R.save(img_io_R, 'PNG')
        img_io_R.seek(0)

        image_logo_ritzwell = get_module_resource('rtw_excel_report', 'img', 'ritzwell.png')
        img_ritzwell = PILImage.open(image_logo_ritzwell)
        img_ritzwell = img_ritzwell.convert('RGB')
        img_ritzwell = img_ritzwell.resize((215, 40))
        img_io_ritzwell = BytesIO()
        img_ritzwell.save(img_io_ritzwell, 'PNG')
        img_io_ritzwell.seek(0)

        # different format  width font 
        format_sheet_title = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':18,'font_name': font_name})
        format_sheet_partner = workbook.add_format({ 'align': 'left','valign': 'vcenter','font_size':16,'font_name': font_name})
        format_text = workbook.add_format({'align': 'left','font_name': font_name,'font_size':12})
        format_text_wrap = workbook.add_format({'align': 'left','font_name': font_name,'font_size':11,'text_wrap':True})
        format_resend = workbook.add_format({'align': 'left','font_name': font_name,'font_size':13,'text_wrap':True})
        format_text_right = workbook.add_format({'align': 'right','font_name': font_name,'font_size':11})
        format_note = workbook.add_format({'align': 'left','valign': 'top','text_wrap':True,'font_name': font_name,'font_size':10})

        format_date = workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_name': font_name,'font_size':10})
        format_address = workbook.add_format({'align': 'right','valign': 'top','text_wrap':True, 'font_name': font_name,'font_size':10})
    
        format_table = workbook.add_format({'align': 'center','valign': 'vcenter','bg_color': '#999999', 'font_name': font_name,'font_size':11,'color':'white','bold':True})
    
        format_lines_note = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bottom':1})
        format_lines_section= workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':11,'bg_color':'#e9ecef','bottom':1})
        
        format_lines_10 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_10_right = workbook.add_format({'align': 'right','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_11_left = workbook.add_format({'align': 'left','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':10,'bottom':1})
        format_lines_13 = workbook.add_format({'align': 'center','valign': 'vcenter', 'text_wrap':True,'font_name': font_name,'font_size':13,'bottom':1})
        
        sheet_name = _("発注書(部材用)") 
        sheet= workbook.add_worksheet(sheet_name)
        sheet_data= workbook.add_worksheet("data")
        sheet_data.hide()
        
        sheet.set_paper(9)  #A4
        sheet.set_landscape()
        sheet.set_print_scale(77)
        
        margin_header = 0.3
        margin_footer = 0.3
        left_margin = 0.8
        right_margin = 0.7
        top_margin = 0.5
        bottom_margin = 0.5
        sheet.set_margins(left=left_margin, right=right_margin, top=top_margin,bottom= bottom_margin)
        
        sheet.set_footer(f'{"&"}P/{"&"}N',margin=margin_footer)   

        sheet.set_column("A:A", width=15, cell_format=font_family)  
        sheet.set_column("B:B", width=20, cell_format=font_family)  
        sheet.set_column("C:C", width=18, cell_format=font_family)  

        sheet.set_column("D:D", width=16, cell_format=font_family)  

        sheet.set_column("E:E", width=0, cell_format=font_family)  
        sheet.set_column("F:F", width=0, cell_format=font_family)

        sheet.set_column("G:G", width=0, cell_format=font_family)  
        sheet.set_column("H:H", width=11, cell_format=font_family)  

        sheet.set_column("I:I", width=16, cell_format=font_family) 
         
        sheet.set_column("J:J", width=6.5, cell_format=font_family)  
        sheet.set_column("K:K", width=10, cell_format=font_family)  
        sheet.set_column("L:L", width=14.5, cell_format=font_family) 

        sheet.set_column("M:M", width=14.5, cell_format=font_family) 
        sheet.set_column("N:N", width=14.5, cell_format=font_family) 
        sheet.set_column("O:Z", None, cell_format=font_family) 
        
        sheet.set_row(1, 46)
        sheet.set_row(2, 17)
        sheet.set_row(3, 17)
        sheet.set_row(5, 15)
        sheet.set_row(6, 15)
        sheet.set_row(7, 15)
        sheet.set_row(8, 13)
        sheet.set_row(9, 12)
        sheet.set_row(11, 22)
        sheet.set_row(12, 24)
        sheet.set_row(13, 22)
        
        sheet.insert_image(1, 0, "logo", {'image_data': img_io_R, 'x_offset': 5, 'y_offset': 1})
        sheet.insert_image(1, 12, "logo2", {'image_data': img_io_ritzwell})
        
        langJP = False
        if self.env.user.lang == 'ja_JP':
            langJP = True
        
        for po in purchase_order[0]:
        #     # y,x
            sheet.write(1, 1, _("発注書(部材用)"), format_sheet_title)
            sheet.write(1, 3, po.purchase_order_company , format_sheet_partner)
            
        #     sheet.merge_range(2, 0,3,2,  po.dear_to if po.dear_to else '', format_name_company)
            sheet.write(3, 0, _("発注番号"), format_text) 
            

            sheet.write(6, 0, _("送り先着日"), format_text) 
            sheet.write(6, 1, po.purchase_line_date_planned, format_text)
            
            sheet.write(9, 0, _("送り先:"), format_text) 
            sheet.merge_range(
                9, 1, 9, 4,
                po.dest_address_id.display_name if (po.picking_type_id and po.picking_type_id.name == "Dropship")
                else (po.picking_type_id.display_name if (po.picking_type_id and po.picking_type_id.name) else ""),
                format_text_wrap
            )
            sheet.write(10, 0, _("住所:"), format_text) 
            sheet.merge_range(10, 1, 10, 4, po.purchase_order_address, format_text_wrap) 
            sheet.write(11, 0, _("TEL:"), format_text) 

            partner_phone = ''
            if po.picking_type_id:
                if po.picking_type_id.name == "Dropship" and po.dest_address_id:
                    partner_phone = po.dest_address_id.phone or ''
                elif po.picking_type_id.warehouse_id.partner_id:
                    partner_phone = po.picking_type_id.warehouse_id.partner_id.phone or ''

            sheet.merge_range(11, 1, 11, 4, partner_phone, format_text_wrap) 
            
            sheet.merge_range(3, 7, 3, 10, po.resend if po.resend else "", format_resend) 

            sheet.write(9, 7, _("送り先注記:"), format_address) 
            sheet.merge_range(9, 8, 11, 10, po.destination_note if po.destination_note else '', format_note)
            
            sheet.write(11, 12, _("販売価格合計:"), format_text_right) 

            sheet.merge_range(0, 12, 0, 13, po.purchase_order_current_date if po.purchase_order_current_date else '' , format_date )
            
            hr_employee = ""
            if po.hr_employee_company:
                hr_employee += po.hr_employee_company + "\n"
            if po.hr_employee_department:
                hr_employee += po.hr_employee_department + "\n"
            if po.hr_employee_zip:
                hr_employee += po.hr_employee_zip + "\n"
            if po.hr_employee_info:
                hr_employee += po.hr_employee_info + "\n"
            if po.hr_employee_tel:
                hr_employee += po.hr_employee_tel + "\n"
            if po.hr_employee_fax:
                hr_employee += po.hr_employee_fax + "\n"
            if po.hr_employee_printer:
                hr_employee += _("発注者 ")+ po.hr_employee_printer
                
            sheet.merge_range(2, 12, 9, 13, hr_employee.rstrip('\n') , format_address) 

            #table title
            sheet.write(13, 0, _("№"), format_table)
            sheet.merge_range(13, 1, 13, 3, _("品名・仕様"), format_table)
            sheet.merge_range(13, 7, 13, 8, _("数量"), format_table)
            sheet.write(13, 9, "", format_table)
            sheet.write(13, 10, _("単価 "), format_table)
            sheet.write(13, 11, _("発注金額"), format_table)
            sheet.merge_range(13, 12, 13, 13, "Custom", format_table)
        
        allow_print = False
        if len(purchase_order) == 1:
            allow_print = True
        else:
            if objects._name == 'purchase.order':
                list_partner_id =[]
                for list in purchase_order:
                    list_partner_id.append(list.partner_id.id or '')

                if list_partner_id:
                    for id in list_partner_id[1:]:
                        if id == list_partner_id[0]:
                            allow_print = True
                        else:
                            allow_print = False
                            break
            else:
                list_partner_id =[]
                for list in purchase_order:
                    list_partner_id.append(list.partner_id.id or '')

                if list_partner_id:
                    for id in list_partner_id[1:]:
                        if id == list_partner_id[0]:
                            allow_print = True
                        else:
                            allow_print = False
                            break

        po_name = ""
        po_origin = ""
        po_amount_untaxed = 0
        row = 14
        list_order_line = []
        if allow_print :
            for po in purchase_order:
                list_order_line += po.order_line
                po_name += po.name + ', '
                po_origin += po.purchase_order_origin + ', '
                po_amount_untaxed += int(po.amount_untaxed)
            arr = po_origin.split(', ')
            arr2 = []
            for item in arr:
                if item not in arr2:
                    arr2.append(item)
            po_origin = ' , '.join(arr2)
                   
            if "," in po_name:
                po_name = po_name.rstrip(', ')
            if "," in po_origin:   
                po_origin = po_origin.rstrip(', ')
            if  objects._name == 'purchase.order':
                if list_order_line:
                    # merge_line = 3 
                    data = []
                    for ind,line in enumerate(list_order_line):
                        purchase_order_line = line.product_id
                        if purchase_order_line:
                            name_ir_data = self.env['ir.model.data'].search([  ('res_id', '=', purchase_order_line.id)], limit=1)
                            data.append({
                                "sequence": line.sequence or ind,
                                "purchase_order_index":line.purchase_order_index,
                                "ir_model_id":name_ir_data.id if name_ir_data else None,
                                "purchase_order_prod_name":line.purchase_order_prod_name,
                                "purchase_order_line_product_uom_qty":line.purchase_order_line_product_uom_qty,
                                "product_uom_name":line.product_uom.name,
                                "display_type":line.display_type,
                                "purchase_order_sell_unit_price":line.purchase_order_sell_unit_price,
                                "price_subtotal":line.price_subtotal,
                                "product_template_attribute_value_ids":line.product_id.product_template_attribute_value_ids,
                                "name":line.name                                 
                            })
                        else:
                            data.append({
                                "sequence": line.sequence or ind,
                                "purchase_order_index":line.purchase_order_index,
                                "ir_model_id":None,
                                "purchase_order_prod_name":line.purchase_order_prod_name,
                                "purchase_order_line_product_uom_qty":line.purchase_order_line_product_uom_qty,
                                "product_uom_name":line.product_uom.name,
                                "display_type":line.display_type,
                                "purchase_order_sell_unit_price":line.purchase_order_sell_unit_price,
                                "price_subtotal":line.price_subtotal,
                                "product_template_attribute_value_ids":line.product_id.product_template_attribute_value_ids if line.product_id else [],
                                "name":line.name
                            })

                    ir_model_ids = [item['ir_model_id'] for item in data if item['ir_model_id'] is not None]
                    has_duplicates = len(ir_model_ids) != len(set(ir_model_ids))
                    
                    if has_duplicates:
                        data_with_model_id = [item for item in data if item['ir_model_id'] is not None]
                        data_without_model_id = [item for item in data if item['ir_model_id'] is None]

                        def aggregate_purchase_data(data):
                            aggregated_data = defaultdict(lambda: {
                                "sequence": float('inf'),
                                "purchase_order_index":0,
                                "purchase_order_prod_name": "",
                                "purchase_order_line_product_uom_qty": 0.0,
                                "product_uom_name": "",
                                "purchase_order_sell_unit_price": "",
                                "price_subtotal": 0
                                })
                            for item in data:
                                key = item["ir_model_id"]
                                qty = float(item["purchase_order_line_product_uom_qty"].replace(",", ""))
                                subtotal = float(str(item["price_subtotal"]).replace(",", ""))
                                
                                if item["sequence"] < aggregated_data[key]["sequence"]:
                                    aggregated_data[key]["sequence"] = item["sequence"]
                                    
                                aggregated_data[key]["purchase_order_prod_name"] = item["purchase_order_prod_name"]
                                aggregated_data[key]["product_uom_name"] = item["product_uom_name"]
                                aggregated_data[key]["purchase_order_sell_unit_price"] = item["purchase_order_sell_unit_price"]
                                aggregated_data[key]["product_template_attribute_value_ids"] = item["product_template_attribute_value_ids"]
                                aggregated_data[key]["display_type"] = item["display_type"]
                                aggregated_data[key]["name"] = item["name"]
                                aggregated_data[key]["purchase_order_line_product_uom_qty"] += int(qty * 100)
                                aggregated_data[key]["price_subtotal"] += subtotal
                            result = []
                            for key, value in aggregated_data.items():
                                value["purchase_order_line_product_uom_qty"] = str(value["purchase_order_line_product_uom_qty"] / 100)
                                value["price_subtotal"] = f"{value['price_subtotal']:,}"
                                value["ir_model_id"] = key
                                result.append(value)
                            return sorted(result, key=lambda x: x['sequence'])
                        
                        aggregated_items = aggregate_purchase_data(data_with_model_id)
                        
                        result = []
                        aggregated_dict = {item['ir_model_id']: item for item in aggregated_items}
                        processed_ids = set()
                        
                        for original_item in sorted(data, key=lambda x: x['sequence']):
                            if original_item['ir_model_id'] is None:
                                result.append(original_item)
                            elif original_item['ir_model_id'] not in processed_ids:
                                result.append(aggregated_dict[original_item['ir_model_id']])
                                processed_ids.add(original_item['ir_model_id'])
                    else:
                        result = sorted(data, key=lambda x: x['sequence'])
                    product_index = 0
                    for item in result:
                        if item.get('display_type') not in ['line_note', 'line_section']:
                            product_index += 1
                            item['purchase_order_index'] = str(product_index)
                        else:
                            item['purchase_order_index'] = ''
                            
                    for ind,line in enumerate(result):
                        merge_line = 2 + len(line['product_template_attribute_value_ids']) if len(line['product_template_attribute_value_ids']) > 1 else 2
                        if line['display_type'] == 'line_note':
                            sheet.merge_range(row, 0, row, 13, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                            sheet_data.write(ind, 0, line['name'] if line['name']  else '', format_lines_note) 
                            row += 1
                        elif line['display_type'] == 'line_section':
                            sheet.merge_range(row, 0, row, 13, "=data!B" + str(ind * 1 + 1) , format_lines_section)
                            sheet_data.write(ind, 1, line['name']  if line['name']  else '' , format_lines_section)
                            row += 1
                        else:
                            sheet.merge_range(row, 0, row + merge_line, 0, line['purchase_order_index'] if line['purchase_order_index'] else '' , format_lines_10) 
                            sheet.merge_range(row, 1, row + merge_line, 3, line['purchase_order_prod_name'] if line['purchase_order_prod_name'] else '' , format_lines_11_left) 
                            sheet.merge_range(row, 7, row + merge_line, 8, line['purchase_order_line_product_uom_qty'] if line['purchase_order_line_product_uom_qty'] else 0 , format_lines_13) 
                            sheet.merge_range(row, 9, row + merge_line, 9, line['product_uom_name'] if line['product_uom_name'] else "", format_lines_10) 
                            sheet.merge_range(row, 10, row + merge_line, 10, "{:,.0f}".format(line['purchase_order_sell_unit_price']) if line['purchase_order_sell_unit_price'] else 0 , format_lines_13) 
                            sheet.merge_range(row, 11, row + merge_line, 11,line['price_subtotal']  if line['price_subtotal'] else 0 , format_lines_13)
                            sheet.merge_range(row, 12, row + merge_line, 13, '' , format_lines_13)
                            row += merge_line + 1
                
            else:
                if objects:
                    # merge_line = 3 
                    for ind,line in enumerate(objects):
                        merge_line = 2 + len(line.product_id.product_template_attribute_value_ids) if len(line.product_id.product_template_attribute_value_ids) > 1 else 2
                        if line.display_type == 'line_note':
                            sheet.merge_range(row, 0, row, 13, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                            sheet_data.write(ind, 0, line.name if line.name else '', format_lines_note) 
                            row += 1
                        elif line.display_type == 'line_section':
                            sheet.merge_range(row, 0, row, 13, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                            sheet_data.write(ind, 1, line.name if line.name else '' , format_lines_section) 
                            row += 1
                        else:
                            sheet.merge_range(row, 0, row + merge_line, 0, line.purchase_order_index if line.purchase_order_index else '' , format_lines_10) 
                            sheet.merge_range(row, 1, row + merge_line, 3, line.purchase_order_prod_name if line.purchase_order_prod_name else '' , format_lines_11_left) 
                            sheet.merge_range(row, 7, row + merge_line, 8, line.purchase_order_line_product_uom_qty if line.purchase_order_line_product_uom_qty else 0 , format_lines_13) 
                            sheet.merge_range(row, 9, row + merge_line, 9, line.product_uom.name if line.product_uom.name else "", format_lines_10) 
                            sheet.merge_range(row, 10, row + merge_line, 10, line.purchase_order_sell_unit_price if line.purchase_order_sell_unit_price else 0 , format_lines_13) 
                            sheet.merge_range(row, 11, row + merge_line, 11, line.price_subtotal if line.price_subtotal else 0 , format_lines_13) 
                            sheet.merge_range(row, 12, row + merge_line, 13, '' , format_lines_13) 
                            row += merge_line + 1
        else:
            for po in purchase_order[0]:
                po_name += po.name if po.name else ""
                po_origin += po.origin if po.origin else ""
                po_amount_untaxed += int(sum(line.price_subtotal for line in po.order_line))
                if po.order_line:
                    # merge_line = 3 
                    for ind,line in enumerate(po.order_line):
                        merge_line = 2 + len(line.product_id.product_template_attribute_value_ids) if len(line.product_id.product_template_attribute_value_ids) > 1 else 2
                        if line.display_type == 'line_note':
                            sheet.merge_range(row, 0, row ,13, "=data!A" + str(ind * 1 + 1) , format_lines_note) 
                            sheet_data.write(ind, 0, line.name if line.name else '', format_lines_note) 
                            row += 1
                        elif line.display_type == 'line_section':
                            sheet.merge_range(row, 0, row, 13, "=data!B" + str(ind * 1 + 1) , format_lines_section) 
                            sheet_data.write(ind, 1, line.name if line.name else '', format_lines_section) 
                            row += 1
                        else:
                            sheet.merge_range(row, 0, row + merge_line, 0, line.purchase_order_index if line.purchase_order_index else '' , format_lines_10) 
                            sheet.merge_range(row, 1, row + merge_line, 3, line.purchase_order_prod_name if line.purchase_order_prod_name else '' , format_lines_11_left) 
                            sheet.merge_range(row, 7, row + merge_line, 8, line.purchase_order_line_product_uom_qty if line.purchase_order_line_product_uom_qty else 0 , format_lines_13) 
                            sheet.merge_range(row, 9, row + merge_line, 9, line.product_uom.name if line.product_uom.name else "", format_lines_10) 
                            sheet.merge_range(row, 10, row + merge_line, 10, "{:,.0f}".format(line.purchase_order_sell_unit_price) if line.purchase_order_sell_unit_price else 0 , format_lines_13) 
                            sheet.merge_range(row, 11, row + merge_line, 11, "{:,.0f}".format(line.price_subtotal) if line.price_subtotal else 0 , format_lines_13) 
                            sheet.merge_range(row, 12, row + merge_line, 13, '' , format_lines_13) 
                            row += merge_line + 1
                            
        sheet.set_header( f'{"&"}R {po_name if po_name else ""}', margin=margin_header)
        sheet.write(4, 1, po_name if po_name else "", format_text)
        sheet.write(3, 1, po_origin if po_name else "", format_text)
        sheet.write(11, 13, "{:,.0f}".format(po_amount_untaxed), format_text_right)


class ReportMrpExcelPurchaseLine(models.AbstractModel):
    _name = 'report.rtw_excel_report.purchase_order_line_for_part_xls'
    _inherit = 'report.rtw_excel_report.report_purchase_order_for_part_xls'

    

    