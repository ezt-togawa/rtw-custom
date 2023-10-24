from odoo import models

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.inspection_check_sheet_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format = workbook.add_format({'align': 'center','valign': 'vcenter','border':1})
        format_tick = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'bold':True})
        format_size = workbook.add_format({'align': 'left','valign': 'vcenter','font_size':16,'bold':True})
        format_wrap = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1})
        format_table = workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC','border':1})
        
        for stock_picking in lines :
            stock_move_lines=self.env["stock.move.line"].search([("picking_id", "=", stock_picking.id)])
            if stock_move_lines:
                for line in stock_move_lines: 

                    prod_code=""
                    prod_name=""
                    if line.product_id.default_code:
                        prod_code= "[" + line.product_id.default_code +  "]" 
                    if line.product_id.product_tmpl_id.name:
                        prod_name=line.product_id.product_tmpl_id.name

                    prod_attrs=[]
                    attribute = line.product_id.product_template_attribute_value_ids
                    if attribute:
                        for attr in attribute:
                            prod_attrs.append(attr.attribute_id.name + ":" + attr.product_attribute_value_id.name)
                        
                    sheet_name = prod_code + prod_name
                    sheet = workbook.add_worksheet(sheet_name)
                    sheet.set_column("I:I", width=14)
                    sheet.set_column("J:J", width=3)
                    sheet.set_column("K:K", width=4)
                    sheet.set_column("M:M", width=12)

                    sheet.merge_range(1,0,2,1, "製造工場 ", format_table)
                    sheet.merge_range(3,0,4,1, "受注番号 ", format_table)
                    sheet.merge_range(1,2,2,4, "リッツウェル製造部 ", format)
                    sheet.merge_range(3,2,4,4,stock_picking.name , format)
                    sheet.merge_range(1,6,2,7, "工場責任者", format_table)
                    sheet.merge_range(1,8,2,8, "リッツウェル", format_table)
                    sheet.merge_range(3,6,6,7, "㊞", format)
                    sheet.merge_range(3,8,6,8, "㊞", format)
                    sheet.merge_range(8,0,9,1, "確認", format_table)
                    sheet.merge_range(8,2,9,4, "製品名", format_table)
                    sheet.merge_range(8,5,9,5, "数", format_table)

                    sheet.merge_range(8,6,9,7, "仕様", format_table)
                    sheet.merge_range(8,8,9,8, "張地", format_table)

                    sheet.merge_range(10,0,11,0, "□", format)
                    sheet.write(10,1, "通常", format)
                    sheet.write(11,1, "別注", format)

                    name_categ=""
                    p_type = ""
                    if line.move_id.p_type:
                        if line.move_id.p_type == "special":
                            p_type = "別注"
                        elif line.move_id.p_type == "custom":
                            p_type = "特注"
                    if line.product_id.product_tmpl_id.categ_id.name:
                        name_categ = str(line.product_id.product_tmpl_id.categ_id.name) + "\n" + p_type
                    sheet.merge_range(10,2,11,4, name_categ, format_wrap)

                    sheet.merge_range(10,5,11,5, line.product_qty, format)

                    prod_attrs=[]
                    attribute = line.product_id.product_template_attribute_value_ids
                    if attribute:
                        for attr in attribute:
                            prod_attrs.append(attr.attribute_id.name + ":" + attr.product_attribute_value_id.name)
                                        
                    if len(prod_attrs)==1:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap)
                        sheet.merge_range(11,6,11,7, "" ,format_wrap)
                        sheet.write(10,8, "", format_wrap)
                        sheet.write(11,8, "", format_wrap)                        
                    elif len(prod_attrs)==2:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap)
                        sheet.write(10,8, "", format_wrap)
                        sheet.write(11,8, "", format_wrap)  
                    elif len(prod_attrs)==3:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap)
                        sheet.write(10,8, prod_attrs[2], format_wrap)
                        sheet.write(11,8, "", format_wrap)
                    elif len(prod_attrs)>=4:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap)
                        sheet.write(10,8, prod_attrs[2], format_wrap)
                        sheet.write(11,8, prod_attrs[3] , format_wrap)
                    else:
                        sheet.merge_range(10,6,10,7, "", format_wrap)
                        sheet.merge_range(11,6,11,7, "" ,format_wrap)
                        sheet.write(10,8, "", format_wrap)
                        sheet.write(11,8, "", format_wrap)

                    sheet.merge_range(13,0,13,3, "■最終検品時　作業確認表", format_size)
                    sheet.merge_range(14,0,15,0, "確認", format_table)
                    sheet.merge_range(14,1,15,3, "作業項目", format_table)
                    sheet.merge_range(14,4,15,7, "注意点", format_table)
                    sheet.merge_range(16,0,17,0, "□", format_tick)
                    sheet.merge_range(18,0,21,0, "□", format_tick)
                    sheet.merge_range(22,0,23,0, "□", format_tick)
                    sheet.merge_range(24,0,25,0, "□", format_tick)
                    sheet.merge_range(26,0,27,0, "□", format_tick)
                    sheet.merge_range(28,0,29,0, "", format)
                    sheet.merge_range(16,1,17,3, "取り付け・加工等", format)
                    sheet.merge_range(18,1,19,3, "外観チェック", format)
                    sheet.merge_range(20,1,21,3, "直座り検査", format)
                    sheet.merge_range(22,1,23,3, "脚部強度確認", format)
                    sheet.merge_range(24,1,25,3, "レベル・脚裏確認", format)
                    sheet.merge_range(26,1,27,3, "検印シール", format)
                    sheet.merge_range(28,1,29,3, "", format)
                    sheet.merge_range(16,4,17,7, "脚切・プラパート・同梱物・その他", format)
                    sheet.merge_range(18,4,19,7, "※右表にチェック", format)
                    sheet.merge_range(20,4,21,7, "キシミ音", format)
                    sheet.merge_range(22,4,23,7, "※脚部の強度確認を必ず実施して下さい", format)
                    sheet.merge_range(24,4,25,7, "ガタツキ・脚裏の汚れを確認", format)
                    sheet.merge_range(26,4,27,7, "貼り忘れ注意", format)
                    sheet.merge_range(28,4,29,7, "", format)

                    sheet.merge_range(31,0,31,3, "■梱包時　作業確認表", format_size)
                    sheet.merge_range(32,0,33,0, "確認", format_table)
                    sheet.merge_range(34,0,36,0, "□", format)
                    sheet.merge_range(37,0,39,0, "□", format)
                    sheet.merge_range(40,0,42,0, "", format)
                    sheet.merge_range(32,1,33,3, "作業項目", format_table)
                    sheet.merge_range(34,1,36,3, "同梱物", format)
                    sheet.merge_range(37,1,39,3, "梱包", format)
                    sheet.merge_range(40,1,42,3, "", format)
                    sheet.merge_range(32,4,33,7, "注意点", format_table)
                    sheet.merge_range(34,4,36,7, "同梱物の確認", format)
                    sheet.merge_range(37,4,39,7, "梱包仕様・製品梱包間違い", format)
                    sheet.merge_range(40,4,42,7, "", format)

                    sheet.merge_range(1,10,2,12, "■不良箇所確認表", format_size)
                    sheet.merge_range(3,10,4,12, "", format_table)
                    sheet.merge_range(5,10,7,12, "検品者", format)
                    sheet.merge_range(8,10,9,12, "検品日", format)
                    sheet.merge_range(3,13,4,15, "張り後", format_table)
                    sheet.merge_range(5,13,7,15, "武・長・福・中・今"  + "\n" + "末    尾    本    村    任", format_wrap)
                    sheet.merge_range(8,13,9,15, "/", format)
                    sheet.merge_range(3,16,4,18, "最終検品", format_table)
                    sheet.merge_range(5,16,7,18, "武・長・福・中・今"  + "\n" + "末    尾    本    村    任", format_wrap)
                    sheet.merge_range(8,16,9,18, "/", format)

                    sheet.merge_range(11,10,12,12, "不良項目", format_table)
                    sheet.merge_range(13,10,27,10, "木"+ "\n" + "部", format_wrap)
                    sheet.merge_range(28,10,36,10, "張"+ "\n" + "り"+ "\n" + "後", format_wrap)
                    sheet.merge_range(13,11,15,12, "ワレ", format)
                    sheet.merge_range(16,11,18,12, "キズ・へこみ", format)
                    sheet.merge_range(19,11,21,12, "木目・節・白太", format)
                    sheet.merge_range(22,11,24,12, "接合部スキマ・グラツキ", format)
                    sheet.merge_range(25,11,27,12, "塗装不良・ムラ", format)
                    sheet.merge_range(28,11,30,12, "張り仕上がり", format)
                    sheet.merge_range(31,11,33,12, "張地不良（ベルト・ファスナー", format)
                    sheet.merge_range(34,11,36,12, "汚れ・銀ペン・接着剤", format)
                    sheet.merge_range(37,10,39,12, "その他不良", format)
                    sheet.merge_range(11,13,12,13, "確認", format_table)
                    sheet.merge_range(13,13,15,13, "□", format_tick)
                    sheet.merge_range(16,13,18,13, "□", format_tick)
                    sheet.merge_range(19,13,21,13, "□", format_tick)
                    sheet.merge_range(22,13,24,13, "□", format_tick)
                    sheet.merge_range(25,13,27,13, "□", format_tick)
                    sheet.merge_range(28,13,30,13, "□", format_tick)
                    sheet.merge_range(31,13,33,13, "□", format_tick)
                    sheet.merge_range(34,13,36,13, "□", format_tick)
                    sheet.merge_range(37,13,39,13, "□", format_tick)
                    sheet.merge_range(11,14,12,15, "不良箇所詳細", format_table)
                    sheet.merge_range(13,14,15,15, "", format)
                    sheet.merge_range(16,14,18,15, "", format)
                    sheet.merge_range(19,14,21,15, "", format)
                    sheet.merge_range(22,14,24,15, "", format)
                    sheet.merge_range(25,14,27,15, "", format)
                    sheet.merge_range(28,14,30,15, "", format)
                    sheet.merge_range(31,14,33,15, "", format)
                    sheet.merge_range(34,14,36,15, "", format)
                    sheet.merge_range(37,14,39,15, "", format)
                    sheet.merge_range(11,16,12,16, "確認", format_table)
                    sheet.merge_range(13,16,15,16, "□", format_tick)
                    sheet.merge_range(16,16,18,16, "□", format_tick)
                    sheet.merge_range(19,16,21,16, "□", format_tick)
                    sheet.merge_range(22,16,24,16, "□", format_tick)
                    sheet.merge_range(25,16,27,16, "□", format_tick)
                    sheet.merge_range(28,16,30,16, "□", format_tick)
                    sheet.merge_range(31,16,33,16, "□", format_tick)
                    sheet.merge_range(34,16,36,16, "□", format_tick)
                    sheet.merge_range(37,16,39,16, "□", format_tick)
                    sheet.merge_range(11,17,12,18, "不良箇所詳細", format_table)
                    sheet.merge_range(13,17,15,18, "", format)
                    sheet.merge_range(16,17,18,18, "", format)
                    sheet.merge_range(19,17,21,18, "", format)
                    sheet.merge_range(22,17,24,18, "", format)
                    sheet.merge_range(25,17,27,18, "", format)
                    sheet.merge_range(28,17,30,18, "", format)
                    sheet.merge_range(31,17,33,18, "", format)
                    sheet.merge_range(34,17,36,18, "", format)
                    sheet.merge_range(37,17,39,18, "", format)

                    sheet.merge_range(42,14,44,15, "出荷日", format_table)
                    if stock_picking.confirmed_shipping_date :
                        sheet.merge_range(42,16,44,18,str(stock_picking.confirmed_shipping_date).replace("-","/") , format)
                    else:
                        sheet.merge_range(42,16,44,18," " , format)
