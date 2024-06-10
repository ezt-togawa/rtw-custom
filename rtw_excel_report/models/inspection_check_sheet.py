from odoo import models, _

class productSpec(models.AbstractModel):
    _name = 'report.rtw_excel_report.inspection_check_sheet_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        self = self.with_context(lang=self.env.user.lang)        
        # apply default font for workbook
        font_name = 'HGPｺﾞｼｯｸM'
        font_family = workbook.add_format({'font_name': font_name})

        format_head_title = workbook.add_format({'align': 'left','valign': 'vcenter','font_size':14,'bold':True,'font_name': font_name})
        format_cell_tick = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':18,'font_name': font_name})

        format_gray_center_size8= workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC','border':1,'font_size':8,'font_name': font_name})
        format_gray_center_size9= workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC','border':1,'font_size':9,'font_name': font_name})
        format_gray_center_size10= workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC','border':1,'font_size':10,'font_name': font_name})
        format_gray_center_size14= workbook.add_format({ 'align': 'center','valign': 'vcenter','bg_color': '#CCCCCC','border':1,'font_size':14,'font_name': font_name})

        format_white_center_size8 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':8,'font_name': font_name})
        format_white_center_size9 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':9,'font_name': font_name})
        format_white_center_size10 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':10,'font_name': font_name})
        format_white_center_size11 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':11,'font_name': font_name})
        format_white_center_size14 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':14,'font_name': font_name})
        format_white_center_size20 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':20,'font_name': font_name})
        format_white_left_size10 = workbook.add_format({'align': 'center','valign': 'vcenter','border':1,'font_size':10,'font_name': font_name})
        format_white_left_bold_size10 = workbook.add_format({'align': 'center','bold':True,'valign': 'vcenter','border':1,'font_size':10,'font_name': font_name})
        format_white_center_bold_size11 = workbook.add_format({'align': 'center','bold':True,'valign': 'vcenter','border':1,'font_size':11,'font_name': font_name})

        format_wrap_white_center_size8 = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_size':8,'font_name': font_name})
        format_wrap_white_center_size9 = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_size':9,'font_name': font_name})
        format_wrap_white_center_size9_verticle = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_size':9,'font_name': font_name, 'rotation': 90})
        format_wrap_white_center_size10 = workbook.add_format({'align': 'center','valign': 'vcenter','text_wrap':True, 'border': 1,'font_size':10,'font_name': font_name})

        for stock_picking in lines :
            stock_move_lines=self.env["stock.move.line"].search([("picking_id", "=", stock_picking.id)])
            if stock_move_lines:
                for index,line in enumerate(stock_move_lines) : 

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
                        
                    sheet_name = prod_code + prod_name + "_" + str(index)
                    sheet = workbook.add_worksheet(sheet_name)
                    sheet.set_column("I:I", width=14,cell_format=font_family)
                    sheet.set_column("J:J", width=3,cell_format=font_family)
                    sheet.set_column("K:K", width=4,cell_format=font_family)
                    sheet.set_column("M:M", width=12,cell_format=font_family)
                    sheet.set_column("A:Z", None,cell_format=font_family)

                    #table 1
                    sheet.merge_range(1,0,2,1, _("製造工場 "), format_gray_center_size10)
                    sheet.merge_range(3,0,4,1, _("受注番号 "), format_gray_center_size10)
                    sheet.merge_range(1,2,2,4, _("リッツウェル製造部 "), format_white_center_size11)
                    sheet.merge_range(3,2,4,4,stock_picking.name , format_white_center_size20)

                    #table 2
                    sheet.merge_range(1,6,2,7, _("工場責任者"), format_gray_center_size8)
                    sheet.merge_range(1,8,2,8, _("リッツウェル"), format_gray_center_size8)
                    sheet.merge_range(3,6,6,7, _("㊞"), format_white_center_size10)
                    sheet.merge_range(3,8,6,8, _("㊞"), format_white_center_size10)

                    #table 3
                    sheet.merge_range(8,0,9,1, _("確認"), format_gray_center_size10)
                    sheet.merge_range(8,2,9,4, _("製品名"), format_gray_center_size9)
                    sheet.merge_range(8,5,9,5, _("数"), format_gray_center_size9)
                    sheet.merge_range(8,6,9,7, _("仕様"), format_gray_center_size9)
                    sheet.merge_range(8,8,9,8, _("張地"), format_gray_center_size9)
                    sheet.merge_range(10,0,11,0, "□", format_cell_tick)
                    sheet.write(10,1, _("通常"), format_white_center_size8)
                    sheet.write(11,1, _("別注"), format_white_center_size8)

                    name_categ=""
                    p_type = ""
                    if line.move_id.p_type:
                        if line.move_id.p_type == "special":
                            p_type = _("別注")
                        elif line.move_id.p_type == "custom":
                            p_type = _("特注")
                    if line.product_id.product_tmpl_id.categ_id.name:
                        name_categ = str(line.product_id.product_tmpl_id.categ_id.name) + "\n" + p_type
                    sheet.merge_range(10,2,11,4, name_categ, format_wrap_white_center_size10)

                    sheet.merge_range(10,5,11,5, line.product_qty, format_white_center_size11)

                    prod_attrs=[]
                    attribute = line.product_id.product_template_attribute_value_ids
                    if attribute:
                        for attr in attribute:
                            prod_attrs.append(attr.attribute_id.name + ":" + attr.product_attribute_value_id.name)
                                        
                    if len(prod_attrs)==1:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap_white_center_size9)
                        sheet.merge_range(11,6,11,7, "" ,format_wrap_white_center_size9)
                        sheet.write(10,8, "", format_wrap_white_center_size9)
                        sheet.write(11,8, "", format_wrap_white_center_size9)                        
                    elif len(prod_attrs)==2:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap_white_center_size9)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap_white_center_size9)
                        sheet.write(10,8, "", format_wrap_white_center_size9)
                        sheet.write(11,8, "", format_wrap_white_center_size9)  
                    elif len(prod_attrs)==3:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap_white_center_size9)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap_white_center_size9)
                        sheet.write(10,8, prod_attrs[2], format_wrap_white_center_size9)
                        sheet.write(11,8, "", format_wrap_white_center_size9)
                    elif len(prod_attrs)>=4:
                        sheet.merge_range(10,6,10,7, prod_attrs[0], format_wrap_white_center_size9)
                        sheet.merge_range(11,6,11,7, prod_attrs[1] ,format_wrap_white_center_size9)
                        sheet.write(10,8, prod_attrs[2], format_wrap_white_center_size9)
                        sheet.write(11,8, prod_attrs[3] , format_wrap_white_center_size9)
                    else:
                        sheet.merge_range(10,6,10,7, "", format_wrap_white_center_size9)
                        sheet.merge_range(11,6,11,7, "" ,format_wrap_white_center_size9)
                        sheet.write(10,8, "", format_wrap_white_center_size9)
                        sheet.write(11,8, "", format_wrap_white_center_size9)

                    #table 4
                    sheet.merge_range(13,0,13,3, _("■最終検品時　作業確認表"), format_head_title)
                    sheet.merge_range(14,0,15,0, _("確認"), format_gray_center_size9)
                    sheet.merge_range(14,1,15,3, _("作業項目"), format_gray_center_size9)
                    sheet.merge_range(14,4,15,7, _("注意点"), format_gray_center_size9)
                    sheet.merge_range(16,0,17,0, "□", format_cell_tick)
                    sheet.merge_range(18,0,21,0, "□", format_cell_tick)
                    sheet.merge_range(22,0,23,0, "□", format_cell_tick)
                    sheet.merge_range(24,0,25,0, "□", format_cell_tick)
                    sheet.merge_range(26,0,27,0, "□", format_cell_tick)
                    sheet.merge_range(28,0,29,0, "", format_white_center_size10)
                    sheet.merge_range(16,1,17,3, _("取り付け・加工等"), format_white_left_size10)
                    sheet.merge_range(18,1,19,3, _("外観チェック"), format_white_left_bold_size10)
                    sheet.merge_range(20,1,21,3, _("直座り検査"), format_white_left_size10)
                    sheet.merge_range(22,1,23,3, _("脚部強度確認"), format_white_left_bold_size10)
                    sheet.merge_range(24,1,25,3, _("レベル・脚裏確認"), format_white_left_size10)
                    sheet.merge_range(26,1,27,3, _("検印シール"), format_white_left_size10)
                    sheet.merge_range(28,1,29,3, "", format_white_left_size10)
                    sheet.merge_range(16,4,17,7, _("脚切・プラパート・同梱物・その他"), format_white_center_size10)
                    sheet.merge_range(18,4,19,7, _("※右表にチェック"), format_white_center_size10)
                    sheet.merge_range(20,4,21,7, _("キシミ音"), format_white_center_size10)
                    sheet.merge_range(22,4,23,7, _("※脚部の強度確認を必ず実施して下さい"), format_white_center_size10)
                    sheet.merge_range(24,4,25,7, _("ガタツキ・脚裏の汚れを確認"), format_white_center_size10)
                    sheet.merge_range(26,4,27,7, _("貼り忘れ注意"), format_white_center_size10)
                    sheet.merge_range(28,4,29,7, "", format_white_center_size10)

                    #table 5
                    sheet.merge_range(31,0,31,3, _("■梱包時　作業確認表"), format_head_title)
                    sheet.merge_range(32,0,33,0, _("確認"), format_gray_center_size9)
                    sheet.merge_range(32,1,33,3, _("作業項目"), format_gray_center_size9)
                    sheet.merge_range(32,4,33,7, _("注意点"), format_gray_center_size9)
                    sheet.merge_range(34,0,36,0, "□", format_cell_tick)
                    sheet.merge_range(37,0,39,0, "□", format_cell_tick)
                    sheet.merge_range(40,0,42,0, "", format_white_center_size10)
                    sheet.merge_range(34,1,36,3, _("同梱物"), format_white_left_size10)
                    sheet.merge_range(37,1,39,3, _("梱包"), format_white_left_size10)
                    sheet.merge_range(40,1,42,3, "", format_white_left_size10)
                    sheet.merge_range(34,4,36,7, _("同梱物の確認"), format_white_center_size10)
                    sheet.merge_range(37,4,39,7, _("梱包仕様・製品梱包間違い"), format_white_center_size10)
                    sheet.merge_range(40,4,42,7, "", format_white_center_size10)

                    #table 6
                    sheet.merge_range(1,10,2,12, _("■不良箇所確認表"), format_head_title)
                    sheet.merge_range(3,10,4,12, "", format_gray_center_size9)
                    sheet.merge_range(3,13,4,15, _("張り後"), format_gray_center_size9)
                    sheet.merge_range(3,16,4,18, _("最終検品"), format_gray_center_size9)
                    sheet.merge_range(5,10,7,12, _("検品者"), format_white_center_size10)
                    sheet.merge_range(8,10,9,12, _("検品日"), format_white_center_size10)
                    sheet.merge_range(5,13,7,15, "武・長・福・中・今" + "\n" + "末    尾    本    村    任", format_wrap_white_center_size8)
                    sheet.merge_range(8,13,9,15, "/", format_white_center_bold_size11)
                    sheet.merge_range(5,16,7,18, "武・長・福・中・今" + "\n" + "末    尾    本    村    任", format_wrap_white_center_size8)
                    sheet.merge_range(8,16,9,18, "/", format_white_center_bold_size11)

                    #table 7
                    sheet.merge_range(11,10,12,12, _("不良項目"), format_gray_center_size9)
                    sheet.merge_range(11,14,12,15, _("不良箇所詳細"), format_gray_center_size9)
                    sheet.merge_range(11,13,12,13, _("確認"), format_gray_center_size9)
                    sheet.merge_range(11,16,12,16, _("確認"), format_gray_center_size9)
                    sheet.merge_range(11,17,12,18, _("不良箇所詳細"), format_gray_center_size9)

                    sheet.merge_range(13,10,27,10, _("木部"), format_wrap_white_center_size9_verticle )
                    sheet.merge_range(28,10,36,10, _("張り後"), format_wrap_white_center_size9_verticle )

                    sheet.merge_range(13,11,15,12, _("ワレ"), format_white_center_size10)
                    sheet.merge_range(16,11,18,12, _("キズ・へこみ"), format_white_center_size10)
                    sheet.merge_range(19,11,21,12, _("木目・節・白太"), format_white_center_size10)
                    sheet.merge_range(22,11,24,12, _("接合部スキマ・グラツキ"), format_white_center_size10)
                    sheet.merge_range(25,11,27,12, _("塗装不良・ムラ"), format_white_center_size10)
                    sheet.merge_range(28,11,30,12, _("張り仕上がり"), format_white_center_size10)
                    sheet.merge_range(31,11,33,12, _("張地不良（ベルト・ファスナー)"), format_white_center_size10)
                    sheet.merge_range(34,11,36,12, _("汚れ・銀ペン・接着剤"), format_white_center_size10)
                    sheet.merge_range(37,10,39,12, _("その他不良"), format_white_center_size9)

                    sheet.merge_range(13,13,15,13, "□", format_cell_tick)
                    sheet.merge_range(16,13,18,13, "□", format_cell_tick)
                    sheet.merge_range(19,13,21,13, "□", format_cell_tick)
                    sheet.merge_range(22,13,24,13, "□", format_cell_tick)
                    sheet.merge_range(25,13,27,13, "□", format_cell_tick)
                    sheet.merge_range(28,13,30,13, "□", format_cell_tick)
                    sheet.merge_range(31,13,33,13, "□", format_cell_tick)
                    sheet.merge_range(34,13,36,13, "□", format_cell_tick)
                    sheet.merge_range(37,13,39,13, "□", format_cell_tick)

                    sheet.merge_range(13,14,15,15, "", format_white_center_size11)
                    sheet.merge_range(16,14,18,15, "", format_white_center_size11)
                    sheet.merge_range(19,14,21,15, "", format_white_center_size11)
                    sheet.merge_range(22,14,24,15, "", format_white_center_size11)
                    sheet.merge_range(25,14,27,15, "", format_white_center_size11)
                    sheet.merge_range(28,14,30,15, "", format_white_center_size11)
                    sheet.merge_range(31,14,33,15, "", format_white_center_size11)
                    sheet.merge_range(34,14,36,15, "", format_white_center_size11)
                    sheet.merge_range(37,14,39,15, "", format_white_center_size11)

                    sheet.merge_range(13,16,15,16, "□", format_cell_tick)
                    sheet.merge_range(16,16,18,16, "□", format_cell_tick)
                    sheet.merge_range(19,16,21,16, "□", format_cell_tick)
                    sheet.merge_range(22,16,24,16, "□", format_cell_tick)
                    sheet.merge_range(25,16,27,16, "□", format_cell_tick)
                    sheet.merge_range(28,16,30,16, "□", format_cell_tick)
                    sheet.merge_range(31,16,33,16, "□", format_cell_tick)
                    sheet.merge_range(34,16,36,16, "□", format_cell_tick)
                    sheet.merge_range(37,16,39,16, "□", format_cell_tick)

                    sheet.merge_range(13,17,15,18, "", format_white_center_size11)
                    sheet.merge_range(16,17,18,18, "", format_white_center_size11)
                    sheet.merge_range(19,17,21,18, "", format_white_center_size11)
                    sheet.merge_range(22,17,24,18, "", format_white_center_size11)
                    sheet.merge_range(25,17,27,18, "", format_white_center_size11)
                    sheet.merge_range(28,17,30,18, "", format_white_center_size11)
                    sheet.merge_range(31,17,33,18, "", format_white_center_size11)
                    sheet.merge_range(34,17,36,18, "", format_white_center_size11)
                    sheet.merge_range(37,17,39,18, "", format_white_center_size11)

                    #table 8
                    sheet.merge_range(42,14,44,15, _("出荷日"), format_gray_center_size14)
                    if stock_picking.confirmed_shipping_date :
                        sheet.merge_range(42,16,44,18,str(stock_picking.confirmed_shipping_date).replace("-","/") , format_white_center_size14)
                    else:
                        sheet.merge_range(42,16,44,18," " , format_white_center_size14)
