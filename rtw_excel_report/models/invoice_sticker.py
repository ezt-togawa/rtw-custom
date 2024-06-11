from odoo import models, _

class productLabelSticker(models.AbstractModel):
    _name = 'report.rtw_excel_report.invoice_sticker_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)             
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        merge_format = workbook.add_format({'align': 'left','valign': 'vcenter','font_name': font_name})
        format_p_name = workbook.add_format({'align': 'left','valign': 'vcenter','font_size':28,'font_name': font_name})
        format_sale_title = workbook.add_format({'align': 'left','valign': 'vcenter','font_size':14,'font_name': font_name})
        format_top = workbook.add_format({'align': 'left','valign': 'top','font_name': font_name})
        format_date = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd','font_name': font_name})
        ship_date = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd','font_size':10 ,'font_name': font_name})
        depo_date = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True,'num_format': 'yyyy-mm-dd', 'font_size':12,'bold':True,'font_name': font_name})

        for stock_picking in lines :
            stock_moves=self.env["stock.move"].search([("picking_id", "=", stock_picking.id)])
            if stock_moves:
                for index,line in enumerate(stock_moves):
                    prod_name=""
                    p_detail=""
                    if line.product_id.product_tmpl_id.name:
                        prod_name=line.product_id.product_tmpl_id.name

                    p_type = "\n"
                    if line.p_type:
                        if line.p_type == "special":
                            p_type = "\n" + _("別注")
                        elif line.p_type == "custom":
                            p_type = "\n" + _("特注")
                    if line.product_id.product_tmpl_id.categ_id.name:
                        p_detail += str(line.product_id.product_tmpl_id.categ_id.name) + p_type +"\n\n\n" 
                                
                    sheet_name = f"{prod_name}_{index}"
                    sheet_name=sheet_name.replace(" ", "")
                    sheet_main= workbook.add_worksheet(sheet_name)
                    sheet_main.set_column("A:Z", None,cell_format=font_family)
                    sheet_data= workbook.add_worksheet(f"data_{index}")

                    row_offset = 0  
                    for count in range(2):
                        row_start = count * 16 + row_offset
                        sheet_main.merge_range(row_start + 1, 1, row_start + 2, 5, f"=data_{index}!A" + str(count * 1 + 1), format_p_name)

                        sheet_main.merge_range(row_start + 1, 7, row_start + 1, 8, f"=data_{index}!B" + str(count * 1 + 1), ship_date)
                        sheet_main.merge_range(row_start + 2, 7, row_start + 2, 8, f"=data_{index}!C" + str(count * 1 + 1), depo_date)
                        sheet_main.merge_range(row_start + 3, 1, row_start + 3, 4, f"=data_{index}!D" + str(count * 1 + 1), merge_format)
                        sheet_main.set_row(row_start + 3,18)

                        sheet_main.merge_range(row_start + 5, 1, row_start + 5, 9, f"=data_{index}!E" + str(count * 1 + 1), format_sale_title)
                        sheet_main.set_row(row_start + 3,16)
                        sheet_main.merge_range(row_start + 6, 1, row_start + 6, 9, f"=data_{index}!F" + str(count * 1 + 1), merge_format)
                        sheet_main.merge_range(row_start + 7, 1, row_start + 7, 9, f"=data_{index}!G" + str(count * 1 + 1), merge_format)
                        sheet_main.merge_range(row_start + 8, 1, row_start + 8, 9, f"=data_{index}!H" + str(count * 1 + 1), merge_format)
                        sheet_main.merge_range(row_start + 9, 1, row_start + 9, 9, f"=data_{index}!I" + str(count * 1 + 1), merge_format)

                        sheet_main.merge_range(row_start + 10, 1, row_start + 10, 4, f"=data_{index}!J" + str(count * 1 + 1), merge_format)
                        sheet_main.merge_range(row_start + 11, 1, row_start + 11, 4, f"=data_{index}!K" + str(count * 1 + 1), merge_format)
                        sheet_main.merge_range(row_start + 12, 1, row_start + 15, 7, f"=data_{index}!L" + str(count * 1 + 1), format_top)
                        row_offset += 1

                        sheet_data.write(count, 0,p_detail, merge_format)

                        if  stock_picking.confirmed_shipping_date :
                            sheet_data.write(count, 1, stock_picking.confirmed_shipping_date, format_date) 
                        else:
                            sheet_data.write(count, 1, " ", format_date) 

                        if line.depo_date :
                            sheet_data.write(count, 2, line.depo_date, format_date)
                        else:
                            sheet_data.write(count, 2, " ", format_date)
                        
                        prod_attrs=" "
                        attribute = line.product_id.product_template_attribute_value_ids
                        if attribute:
                            for attr in attribute:
                                prod_attrs += attr.attribute_id.name + "/" 
                            prod_attrs = prod_attrs.rstrip("/")
                        sheet_data.write(count, 3, prod_attrs, merge_format)

                        if line.sale_line_id.order_id.title:
                            sheet_data.write(count, 4, line.sale_line_id.order_id.title, merge_format)
                        else:
                            sheet_data.write(count, 4, " ", merge_format)

                        if stock_picking.partner_id :
                            sheet_data.write(count, 5, stock_picking.partner_id.display_name + _("様"), merge_format)
                        else:
                            sheet_data.write(count, 5, " ", merge_format)

                        zip =" "
                        city =" "
                        state =" "
                        street =" "
                        phone =" "
                        order_number =" "

                        if stock_picking.partner_id.zip :
                            zip = stock_picking.partner_id.zip 

                        if stock_picking.partner_id.city :
                            city = stock_picking.partner_id.city 

                        if stock_picking.partner_id.state_id.name :
                            state = stock_picking.partner_id.state_id.name

                        if stock_picking.partner_id.street :
                            street = stock_picking.partner_id.street 

                        if stock_picking.partner_id.phone :
                            phone = stock_picking.partner_id.phone 

                        if line.reference :
                            order_number = line.reference

                        sheet_data.write(count, 6, f"{zip} {city} {state}", merge_format) 
                        sheet_data.write(count, 7, street, merge_format) 

                        if stock_picking.partner_id.commercial_company_name:
                            sheet_data.write(count, 8, stock_picking.partner_id.commercial_company_name, merge_format)
                        else:
                            if stock_picking.partner_id.name:
                                sheet_data.write(count, 8, stock_picking.partner_id.name, merge_format)
                            else:
                                sheet_data.write(count, 8, " ", merge_format)

                        sheet_data.write(count, 9, phone, merge_format)

                        sheet_data.write(count, 10, order_number, merge_format)
                        
                        if stock_picking.note:
                            sheet_data.write(count, 11, stock_picking.note, format_top)
                        else:
                            sheet_data.write(count, 11, " ", format_top)
