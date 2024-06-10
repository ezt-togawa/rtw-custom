from odoo import api, models, _
from datetime import datetime ,timedelta
from odoo.tools import float_is_zero, format_datetime, float_round
from collections import defaultdict

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.stock_status_list_xls'
    _inherit = ['report.report_xlsx.abstract','report.stock.report_product_product_replenishment']

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)         
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        format_title = workbook.add_format({'align': 'center','valign': 'left','bg_color':'#ccffff','font_name': font_name,'font_size': 9})
        format_left = workbook.add_format({'align': 'left','text_wrap':True,'bold':True,'font_name': font_name,'font_size': 9})
        format_table = workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#d6dce4','border':1,'font_name': font_name,'font_size': 9})
        format_cell_white = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bg_color': '#F2F2F2','font_name': font_name,'font_size': 9})
        format_cell_white_right = workbook.add_format({'align': 'right','valign': 'vcenter','border':1,'bg_color': '#F2F2F2','font_name': font_name,'font_size': 9})
        format_cell_yellow = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bg_color': '#FFFFCC','font_name': font_name,'font_size': 9})
        format_cell_yellow_right = workbook.add_format({'align': 'right','valign': 'vcenter','border':1,'bg_color': '#FFFFCC','font_name': font_name,'font_size': 9})
        format_cell_green = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bg_color': '#CCFFCC','font_name': font_name,'font_size': 9})
        format_cell_green_right = workbook.add_format({'align': 'right','valign': 'vcenter','border':1,'bg_color': '#CCFFCC','font_name': font_name,'font_size': 9})
        format_cell_blue = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bg_color': '#ccffff','font_name': font_name,'font_size': 9})
        format_cell_blue_right = workbook.add_format({'align': 'right','valign': 'vcenter','border':1,'bg_color': '#ccffff','font_name': font_name,'font_size': 9})
        format_cell_purple = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bg_color': '#FFCCFF','font_name': font_name,'font_size': 9})
        format_cell_purple_right = workbook.add_format({'align': 'right','valign': 'vcenter','border':1,'bg_color': '#FFCCFF','font_name': font_name,'font_size': 9})
        format_cell_gray= workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'bg_color': '#7f7f7f','font_name': font_name,'font_size': 9})
        format_cell_gray_right= workbook.add_format({'align': 'right','valign': 'vcenter','text_wrap':True, 'border': 1,'bg_color': '#7f7f7f','font_name': font_name,'font_size': 9})
        format_cell_gray_left= workbook.add_format({'align': 'left','valign': 'vcenter','text_wrap':True, 'border': 1,'bg_color': '#7f7f7f','font_name': font_name,'font_size': 9})

        #current time
        current_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        end_date = current_date + timedelta(days=90)  

        row_start=3
        for p_template in lines :
            product_supplierinfo= self.env["product.supplierinfo"].search([("product_tmpl_id", "=",  p_template.id)])
            delay=0
            if product_supplierinfo:
                for x in product_supplierinfo:
                    if int(x.delay) > delay:
                        delay = int(x.delay)

            prod_name=""
            if p_template.name:
                prod_name=p_template.name

            sheet_name = prod_name
            sheet = workbook.add_worksheet(sheet_name)
            sheet.set_column("A:A", None,cell_format=font_family ) 
            sheet.set_column("B:B", width=12,cell_format=font_family)
            sheet.set_column("C:C", width=14,cell_format=font_family)
            sheet.set_column("D:D", None,cell_format=font_family ) 
            sheet.set_column("E:E", width=14,cell_format=font_family)
            sheet.set_column("F:F", width=15,cell_format=font_family)
            sheet.set_column("G:G", width=15,cell_format=font_family)
            sheet.set_column("H:H", width=15,cell_format=font_family)
            sheet.set_column("I:I", width=15,cell_format=font_family)
            sheet.set_column("J:J", width=0,cell_format=font_family)
            sheet.set_column("K:K", width=27,cell_format=font_family)
            sheet.set_column("L:L", None,cell_format=font_family ) 
            sheet.set_column("M:M", None,cell_format=font_family ) 
            sheet.set_column("N:N", width=12,cell_format=font_family)
            sheet.set_column("O:O", width=12,cell_format=font_family)
            sheet.set_column("P:P", width=12,cell_format=font_family)
            sheet.set_column("Q:Z", None,cell_format=font_family ) 

            sheet.merge_range(0,1,0,3,prod_name , format_title)
            sheet.merge_range(1,1,1,2,_("■入荷予定データ") , format_left)
            sheet.merge_range(2,1,2,3,_("仕入先") , format_table)
            sheet.merge_range(2,4,2,6,_("コメント") , format_table)
            sheet.write(2,7,_("入荷予定数") , format_table)
            sheet.write(2,8,_("入荷予定日") , format_table)

            #purchase order lines confirmed but has not done --> show table 1 
            purchase_order_lines = self.env["purchase.order.line"].search([("product_id.product_tmpl_id", "=", p_template.id) ])
            purchase_order_filter=purchase_order_lines.filtered(lambda po: po.product_qty != po.qty_received and po.state == "purchase")
            data_table1=[]

            if purchase_order_filter:
                vendor = ""
                note = ""
                qty = ""
                date_planned=""
                for pol in purchase_order_filter:

                    if pol.partner_id.name:
                        vendor = pol.partner_id.name 

                    if pol.product_qty:
                        qty = str(pol.product_qty) 

                    note= ""

                    purchase_orders= self.env["purchase.order"].search([("id", "=", pol.order_id.id)])
                    if purchase_orders:
                        for po in purchase_orders:
                                stock_pickings= self.env["stock.picking"].search([("origin", "=", po.name), ("state", "in", ["assigned", "confirmed"])])
                                if stock_pickings:
                                    for sp in stock_pickings:
                                            date_planned =  sp.scheduled_date.strftime("%m/%d/%Y")

                    data_table1.append({'qty':qty,'date_planned':date_planned})

                    sheet.merge_range(row_start,1,row_start,3, vendor, format_cell_gray_left)
                    sheet.merge_range(row_start,4,row_start,6, note, format_cell_gray)
                    sheet.write(row_start,7,qty , format_cell_gray_right)
                    sheet.write(row_start,8,date_planned , format_cell_gray_right)
                    row_start += 1
            else:
                sheet.merge_range(row_start,1,row_start,3, " ", format_cell_gray_left)
                sheet.merge_range(row_start,4,row_start,6, " ", format_cell_gray)
                sheet.write(row_start,7," " , format_cell_gray_right)
                sheet.write(row_start,8," " , format_cell_gray_right) 
                row_start += 1  

            #Table 2 
            # table2 start with table_name
            sheet.merge_range(row_start,1,row_start,2, _("■仮押・受注データ") , format_left)

            # table2 start with  titles in table_name
            row_start +=1
            sheet.write(row_start,1, _("受注日"), format_table)
            sheet.write(row_start,2, _("受注No"), format_table)
            sheet.merge_range(row_start,3,row_start,4, _("得意先名"), format_table)
            sheet.write(row_start,5, _("発注期限日"), format_table)
            sheet.write(row_start,6, _("引当基準日"), format_table)
            sheet.write(row_start,7, _("数量"), format_table)
            sheet.write(row_start,8, _("伝票区分"), format_table)

            # table2 start with location data
            row_start +=1
            data= self._get_report_data( lines.ids, None)
            data_table2 = []
            voucher_class = _("受注引当") 
            if data['lines']:
                for x in data['lines']:
                    if x['move_out']:# cause data['lines'] res all remaining  product_number (check last data['lines']) 
                        stock_move = self.env["stock.move"].search([("id", "=", x['move_out'].ids)])
                        if stock_move:
                            stock_picking = self.env["stock.picking"].search([("name", "=", stock_move.reference)])
                            if stock_picking:
                                for sp in stock_picking:
                                    format_date =""
                                    if sp.date:
                                        format_date=sp.date.strftime("%m/%d/%Y")

                                    sheet.write(row_start,1,format_date, format_cell_gray_right)

                                    if sp.origin and (str(sp.origin).startswith("S") or str(sp.origin).startswith("P")):
                                        sheet.write(row_start, 2, sp.origin, format_cell_gray_right)
                                    else:
                                        sheet.write(row_start, 2, sp.name, format_cell_gray_right)

                                    if sp.partner_id.name:
                                        sheet.merge_range(row_start,3,row_start,4, sp.partner_id.name , format_cell_gray_left)
                                    else:
                                        sheet.merge_range(row_start,3,row_start,4, " " , format_cell_gray_left)

                                    if sp.scheduled_date:
                                        sheet.write(row_start,5,(sp.scheduled_date - timedelta(days=delay)).strftime("%m/%d/%Y")  , format_cell_gray_right)
                                        sheet.write(row_start,6,sp.scheduled_date.strftime("%m/%d/%Y") , format_cell_gray_right)
                                    else:
                                        sheet.write(row_start,5,(sp.scheduled_date - timedelta(days=delay)).strftime("%m/%d/%Y")  , format_cell_gray_right)
                                        sheet.write(row_start,6,sp.scheduled_date.strftime("%m/%d/%Y") , format_cell_gray_right)

                                    data_table2.append({
                                        'date':(sp.scheduled_date - timedelta(days=delay)).strftime("%Y-%m-%d"),
                                        'qty':x['quantity'],
                                        'voucher_class':voucher_class
                                        })

                        # if x['replenishment_filled']:
                        sheet.write(row_start,7,x['quantity'] , format_cell_gray_right)
                        # else:
                        #     sheet.write(row_start,7, - x['quantity'] , format_wrap)

                        sheet.write(row_start,8,voucher_class, format_cell_gray)
                        row_start +=1
            else:
                    sheet.write(row_start,1," ", format_cell_gray_right)
                    sheet.write(row_start, 2," ", format_cell_gray_right)
                    sheet.merge_range(row_start,3,row_start,4, " " , format_cell_gray_left)
                    sheet.write(row_start,5," ", format_cell_gray_right)
                    sheet.write(row_start,6," " , format_cell_gray_right)
                    sheet.write(row_start,7," ", format_cell_gray_right)
                    sheet.write(row_start,8," ", format_cell_gray)
                    row_start +=1
            
            #TABLE 3 
            sheet.write(2, 10, "" , format_cell_white)
            sheet.write(2, 11, _("入荷"), format_cell_yellow)
            sheet.write(2, 12, _("受注引当"), format_cell_green)
            sheet.write(2, 13, _("仮押え"), format_cell_yellow)
            sheet.write(2, 14, _("引当のみ"), format_cell_blue)
            sheet.write(2, 15, _("仮押え込み"), format_cell_purple)

            sheet.write(3, 10, _("帳簿在庫") , format_cell_white)
            sheet.write(3, 11, data['quantity_on_hand'] , format_cell_yellow_right)
            sheet.write(3, 12, "" , format_cell_green_right)
            sheet.write(3, 13, "" , format_cell_yellow_right)
            sheet.write(3, 14, data['quantity_on_hand'] , format_cell_blue_right)
            sheet.write(3, 15, data['quantity_on_hand'] , format_cell_purple_right)

            sheet.write(4, 10, _("過去分"), format_cell_white)
            past_qty_table1 = 0
            future_qty_table1 = 0
            if data_table1:
                for x in data_table1 :
                    if x['date_planned'] < current_date.strftime("%Y-%m-%d") :
                        past_qty_table1 += float(x['qty'])
                    
                    if x['date_planned'] > end_date.strftime("%Y-%m-%d") :
                        future_qty_table1 += float(x['qty'])

            sheet.write(4,11,past_qty_table1 , format_cell_yellow_right)

            past_qty_table2_受注引当 = 0
            future_qty_table2_受注引当 = 0

            past_qty_table2_仮押え = 0
            future_qty_table2_仮押え = 0
            if data_table2 :
                for x in data_table2 :
                    if x['voucher_class'] == "受注引当" and  x['date'] < current_date.strftime("%Y-%m-%d") :
                        past_qty_table2_受注引当 += float(x['qty'])

                    if x['voucher_class'] == "受注引当" and  x['date'] > end_date.strftime("%Y-%m-%d") :
                        future_qty_table2_受注引当 += float(x['qty'])

                    if x['voucher_class'] == "仮押え" and  x['date'] < current_date.strftime("%Y-%m-%d"):
                        past_qty_table2_仮押え += float(x['qty'])

                    if x['voucher_class'] == "仮押え" and  x['date'] > end_date.strftime("%Y-%m-%d"):
                        future_qty_table2_仮押え += float(x['qty'])

            sheet.write(4,12,past_qty_table2_受注引当 , format_cell_green_right)
            sheet.write(4,13,past_qty_table2_仮押え , format_cell_yellow_right)
            
            qty_table_3_reserve_only = int(data['quantity_on_hand']) +  past_qty_table1 - past_qty_table2_受注引当
            qty_table_3_temporary_pressing = int(data['quantity_on_hand']) +  past_qty_table1 - past_qty_table2_受注引当 -past_qty_table2_仮押え

            sheet.write(4,14,qty_table_3_reserve_only , format_cell_blue_right)
            sheet.write(4,15,qty_table_3_temporary_pressing, format_cell_purple_right)

            
            date_list = []
            while current_date <= end_date:
                date_list.append(current_date.strftime("%A, %B %d, %Y"))
                current_date += timedelta(days=1)
            # print list date
            start_row=5
            current_date2 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

            qty_table_3_reserve_only_one_above_cell=qty_table_3_reserve_only
            qty_table_3_temporary_pressing_one_above_cell=qty_table_3_temporary_pressing
            qty_table_3_reserve_only_every_row = 0
            qty_table_3_temporary_pressing__every_row = 0
            for date in date_list:
                sheet.write(start_row, 10, date, format_cell_white_right)
                date_obj = datetime.strptime(date,"%A, %B %d, %Y")
                list_date = date_obj.strftime("%Y-%m-%d")    # string 2023-09-19
                quantity_by_day_of_table_1 = 0
                quantity_day_of_table_2_type_受注引当 = 0
                quantity_day_of_table_2_type_仮押え = 0

                if data_table1:
                    for x in data_table1 :
                        if x['date_planned'] == list_date :
                            quantity_by_day_of_table_1 += float(x['qty'])

                if data_table2:
                    for x in data_table2:
                        if x['date'] == list_date and x['voucher_class'] == '受注引当':
                            quantity_day_of_table_2_type_受注引当 += float(x['qty'])
                        if x['date'] == list_date and x['voucher_class'] == '仮押え':
                            quantity_day_of_table_2_type_仮押え += float(x['qty'])

                if qty_table_3_reserve_only_one_above_cell and qty_table_3_temporary_pressing_one_above_cell :
                    qty_table_3_reserve_only_every_row= qty_table_3_reserve_only_one_above_cell  + quantity_by_day_of_table_1 - quantity_day_of_table_2_type_受注引当 
                    qty_table_3_temporary_pressing__every_row= qty_table_3_temporary_pressing_one_above_cell  + quantity_by_day_of_table_1 - quantity_day_of_table_2_type_受注引当 -quantity_day_of_table_2_type_仮押え
                
                qty_table_3_reserve_only_one_above_cell = qty_table_3_reserve_only_every_row
                qty_table_3_temporary_pressing_one_above_cell= qty_table_3_temporary_pressing__every_row

                sheet.write(start_row, 11, quantity_by_day_of_table_1, format_cell_yellow_right)
                sheet.write(start_row, 12, quantity_day_of_table_2_type_受注引当, format_cell_green_right)
                sheet.write(start_row, 13, quantity_day_of_table_2_type_仮押え, format_cell_yellow_right)
                sheet.write(start_row, 14, qty_table_3_reserve_only_every_row, format_cell_blue_right)
                sheet.write(start_row, 15, qty_table_3_temporary_pressing__every_row, format_cell_purple_right)
                start_row += 1

            # future
            sheet.write(start_row,10,_("これ以降"), format_cell_white)
            sheet.write(start_row,11,future_qty_table1, format_cell_yellow_right)
            sheet.write(start_row,12,future_qty_table2_受注引当, format_cell_green_right)
            sheet.write(start_row,13,future_qty_table2_仮押え, format_cell_yellow_right)
            sheet.write(start_row,14,qty_table_3_reserve_only_every_row + future_qty_table1 - future_qty_table2_受注引当, format_cell_blue_right)
            sheet.write(start_row,15,qty_table_3_reserve_only_every_row + future_qty_table1 - future_qty_table2_受注引当 - future_qty_table2_仮押え, format_cell_purple_right)

    def _product_domain(self, product_template_ids, product_variant_ids):
        if product_template_ids:
            return [('product_tmpl_id', 'in', product_template_ids)]
        return [('product_id', 'in', product_variant_ids)]

    def _move_domain(self, product_template_ids, product_variant_ids, wh_location_ids):
        move_domain = self._product_domain(product_template_ids, product_variant_ids)
        move_domain += [('product_uom_qty', '!=', 0)]
        out_domain = move_domain + [
            '&',
            ('location_id', 'in', wh_location_ids),
            ('location_dest_id', 'not in', wh_location_ids),
        ]
        in_domain = move_domain + [
            '&',
            ('location_id', 'not in', wh_location_ids),
            ('location_dest_id', 'in', wh_location_ids),
        ]
        return in_domain, out_domain

    def _move_draft_domain(self, product_template_ids, product_variant_ids, wh_location_ids):
        in_domain, out_domain = self._move_domain(product_template_ids, product_variant_ids, wh_location_ids)
        in_domain += [('state', '=', 'draft')]
        out_domain += [('state', '=', 'draft')]
        return in_domain, out_domain

    def _move_confirmed_domain(self, product_template_ids, product_variant_ids, wh_location_ids):
        in_domain, out_domain = self._move_domain(product_template_ids, product_variant_ids, wh_location_ids)
        out_domain += [('state', 'not in', ['draft', 'cancel', 'done'])]
        in_domain += [('state', 'not in', ['draft', 'cancel', 'done'])]
        return in_domain, out_domain

    def _compute_draft_quantity_count(self, product_template_ids, product_variant_ids, wh_location_ids):
        in_domain, out_domain = self._move_draft_domain(product_template_ids, product_variant_ids, wh_location_ids)
        incoming_moves = self.env['stock.move'].read_group(in_domain, ['product_qty:sum'], 'product_id')
        outgoing_moves = self.env['stock.move'].read_group(out_domain, ['product_qty:sum'], 'product_id')
        in_sum = sum(move['product_qty'] for move in incoming_moves)
        out_sum = sum(move['product_qty'] for move in outgoing_moves)
        return {
            'draft_picking_qty': {
                'in': in_sum,
                'out': out_sum
            },
            'qty': {
                'in': in_sum,
                'out': out_sum
            }
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'data': data,
            'doc_ids': docids,
            'doc_model': 'product.product',
            'docs': self._get_report_data(product_variant_ids=docids),
        }

    def _get_report_data(self, product_template_ids=False, product_variant_ids=False):
        # assert product_template_ids or product_variant_ids
        res = {}

        # Get the warehouse we're working on as well as its locations.
        if self.env.context.get('warehouse'):
            warehouse = self.env['stock.warehouse'].browse(self.env.context['warehouse'])
        else:
            warehouse = self.env['stock.warehouse'].search([
                ('company_id', '=', self.env.company.id)
            ], limit=1)
            self.env.context = dict(self.env.context, warehouse=warehouse.id)
        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read([('id', 'child_of', warehouse.view_location_id.id)],['id'],)]
        res['active_warehouse'] = warehouse.display_name

        # Get the products we're working, fill the rendering context with some of their attributes.
        if product_template_ids:
            product_templates = self.env['product.template'].browse(product_template_ids)
            res['product_templates'] = product_templates
            res['product_variants'] = product_templates.product_variant_ids
            res['multiple_product'] = len(product_templates.product_variant_ids) > 1
            res['uom'] = product_templates[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_templates.mapped('qty_available'))
            res['virtual_available'] = sum(product_templates.mapped('virtual_available'))
        elif product_variant_ids:
            product_variants = self.env['product.product'].browse(product_variant_ids)
            res['product_templates'] = False
            res['product_variants'] = product_variants
            res['multiple_product'] = len(product_variants) > 1
            res['uom'] = product_variants[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_variants.mapped('qty_available'))
            res['virtual_available'] = sum(product_variants.mapped('virtual_available'))
        res.update(self._compute_draft_quantity_count(product_template_ids, product_variant_ids, wh_location_ids))

        res['lines'] = self._get_report_lines(product_template_ids, product_variant_ids, wh_location_ids)
        return res

    def _prepare_report_line(self, quantity, move_out=None, move_in=None, replenishment_filled=True, product=False, reservation=False):
        timezone = self._context.get('tz')
        product = product or (move_out.product_id if move_out else move_in.product_id)
        is_late = move_out.date < move_in.date if (move_out and move_in) else False
        return {
            'document_in': move_in._get_source_document() if move_in else False,
            'document_out': move_out._get_source_document() if move_out else False,
            'product': {
                'id': product.id,
                'display_name': product.display_name
            },
            'replenishment_filled': replenishment_filled,
            'uom_id': product.uom_id,
            'receipt_date': format_datetime(self.env, move_in.date, timezone, dt_format=False) if move_in else False,
            'delivery_date': format_datetime(self.env, move_out.date, timezone, dt_format=False) if move_out else False,
            'is_late': is_late,
            'quantity': float_round(quantity, precision_rounding=product.uom_id.rounding),
            'move_out': move_out,
            'move_in': move_in,
            'reservation': reservation,
        }

    def _get_report_lines(self, product_template_ids, product_variant_ids, wh_location_ids):
        def _rollup_move_dests(move, seen):
            for dst in move.move_dest_ids:
                if dst.id not in seen:
                    seen.add(dst.id)
                    _rollup_move_dests(dst, seen)
            return seen

        def _reconcile_out_with_ins(lines, out, ins, demand, only_matching_move_dest=True):
            index_to_remove = []
            for index, in_ in enumerate(ins):

                if float_is_zero(in_['qty'], precision_rounding=out.product_id.uom_id.rounding):
                    continue


                if only_matching_move_dest and in_['move_dests'] and out.id not in in_['move_dests']:
                    continue

                taken_from_in = min(demand, in_['qty'])
                demand -= taken_from_in
                lines.append(self._prepare_report_line(taken_from_in, move_in=in_['move'], move_out=out))
                in_['qty'] -= taken_from_in


                if in_['qty'] <= 0:
                    index_to_remove.append(index)
                if float_is_zero(demand, precision_rounding=out.product_id.uom_id.rounding):
                    break


            for index in index_to_remove[::-1]:
                ins.pop(index)
            return demand

        in_domain, out_domain = self._move_confirmed_domain(
            product_template_ids, product_variant_ids, wh_location_ids
        )
        outs = self.env['stock.move'].search(out_domain, order='priority desc, date, id')
        outs_per_product = defaultdict(lambda: [])
        outs_reservation = {}
        for out in outs:
            outs_per_product[out.product_id.id].append(out)
            outs_reservation[out.id] = out._get_orig_reserved_availability()
        ins = self.env['stock.move'].search(in_domain, order='priority desc, date, id')
        ins_per_product = defaultdict(lambda: [])
        for in_ in ins:
            ins_per_product[in_.product_id.id].append({
                'qty': in_.product_qty,
                'move': in_,
                'move_dests': _rollup_move_dests(in_, set())
            })
        currents = {c['id']: c['qty_available'] for c in outs.product_id.read(['qty_available'])}

        lines = []
        for product in (ins | outs).product_id:
            for out in outs_per_product[product.id]:
                reserved_availability = outs_reservation[out.id]
                if float_is_zero(reserved_availability, precision_rounding=product.uom_id.rounding):
                    continue
                current = currents[out.product_id.id]
                reserved = out.product_uom._compute_quantity(reserved_availability, product.uom_id)
                currents[product.id] -= reserved
                lines.append(self._prepare_report_line(reserved, move_out=out, reservation=True))

            unreconciled_outs = []
            for out in outs_per_product[product.id]:
                reserved_availability = outs_reservation[out.id]
                # Reconcile with the current stock.
                current = currents[out.product_id.id]
                reserved = 0.0
                if not float_is_zero(reserved_availability, precision_rounding=product.uom_id.rounding):
                    reserved = out.product_uom._compute_quantity(reserved_availability, product.uom_id)
                demand = out.product_qty - reserved
                taken_from_stock = min(demand, current)
                if not float_is_zero(taken_from_stock, precision_rounding=product.uom_id.rounding):
                    currents[product.id] -= taken_from_stock
                    demand -= taken_from_stock
                    lines.append(self._prepare_report_line(taken_from_stock, move_out=out))
                # Reconcile with the ins.
                if not float_is_zero(demand, precision_rounding=product.uom_id.rounding):
                    demand = _reconcile_out_with_ins(lines, out, ins_per_product[out.product_id.id], demand, only_matching_move_dest=True)
                if not float_is_zero(demand, precision_rounding=product.uom_id.rounding):
                    unreconciled_outs.append((demand, out))
            if unreconciled_outs:
                for (demand, out) in unreconciled_outs:
                    # Another pass, in case there are some ins linked to a dest move but that still have some quantity available
                    demand = _reconcile_out_with_ins(lines, out, ins_per_product[product.id], demand, only_matching_move_dest=False)
                    if not float_is_zero(demand, precision_rounding=product.uom_id.rounding):
                        # Not reconciled
                        lines.append(self._prepare_report_line(demand, move_out=out, replenishment_filled=False))
            # Unused remaining stock.
            free_stock = currents.get(product.id, 0)
            if not float_is_zero(free_stock, precision_rounding=product.uom_id.rounding):
                lines.append(self._prepare_report_line(free_stock, product=product))
            # In moves not used.
            for in_ in ins_per_product[product.id]:
                if float_is_zero(in_['qty'], precision_rounding=product.uom_id.rounding):
                    continue
                lines.append(self._prepare_report_line(in_['qty'], move_in=in_['move']))
        return lines

    @api.model
    def get_filter_state(self):
        res = {}
        res['warehouses'] = self.env['stock.warehouse'].search_read(fields=['id', 'name', 'code'])
        res['active_warehouse'] = self.env.context.get('warehouse', False)
        if not res['active_warehouse']:
            company_id = self.env.context.get('allowed_company_ids')[0]
            res['active_warehouse'] = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).id
        return res
