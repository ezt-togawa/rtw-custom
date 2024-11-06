from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo.exceptions import UserError, ValidationError

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
class stock_move_container(models.Model):
    _inherit = 'stock.move.container'
    current_print = fields.Char(compute="_compute_current_print")
    
    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')

class shipping_instruction(models.AbstractModel):
    _name = 'report.rtw_excel_report.shipping_instruction_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("SHIPPING INSTRUCTION")
        font_name_hgp = 'HGPｺﾞｼｯｸM'
        stock_move_container = lines[0]
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        current_date = day + "/" + month + "/" + year
        # ADD LOGO
        image_logo = get_module_resource(
            'rtw_excel_report', 'img', 'ritzwell.png')
        img = PILImage.open(image_logo)
        img = img.convert('RGB')
        img = img.resize((200, 60))
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(2)

        # SET WIDTH FOR COLUMN
        sheet.set_column("A:A", width=20, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("B:B", width=55, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("C:C", width=20, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("D:D", width=20, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("E:E", width=25, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("F:F", width=30, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("G:G", width=30, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("H:H", width=15, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("I:I", width=15, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("J:J", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("K:K", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("L:L", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("M:M", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("N:N", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("O:O", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("P:P", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("Q:Q", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("R:R", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("S:S", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("T:T", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("U:U", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("V:V", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("W:W", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("X:X", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))
        sheet.set_column("Y:Y", None, cell_format=workbook.add_format(
            {'font_name': font_name_hgp}))

        sheet.insert_image(0, 0, "logo", {'image_data': img_io})

        sheet.write(0, 4, "SHIPPING INSTRUCTION", workbook.add_format(
            {'bold': True, 'font_size': 16, 'valign': 'top', 'font_name': font_name_hgp}))

        sheet.write(5, 0, 'DATE', workbook.add_format(
            {'bold': True, 'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 1,  current_date, workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 2,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 3,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 4,  'INVOICE NO.', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 5,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 6,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 7,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'font_name': font_name_hgp}))
        sheet.write(5, 8,  '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'top': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(6, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 1, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 2, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 3, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 4, 'PO NO.', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 5, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 6, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 7, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(6, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(7, 0, 'SHIPPER/EXPORTER', workbook.add_format(
            {'bold': True, 'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(7, 4, 'CONSIGNEE', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(7, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(8, 4, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.write(8, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(9, 0, 'Ritzwell & Co.', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.write(9, 4, 'LIGNE e/o FDS', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.write(9, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(10, 4, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.write(10, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(11, 1, 11, 3, '5-2-9 ITAZUKE HAKATA-KU', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(11, 4, 11, 8, 'NIEUWBRUGSTRAAT ,71', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(12, 1, 12, 3, 'FUKUOKA 812-0888 JAPAN', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(12, 4, 12, 8, 'B1830 MACHELEN BELGIUM', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(13, 1, 13, 3, 'TEL:  +81-92-584-2240', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(13, 4, 13, 8, 'TEL:    +32 2 720 9231', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(14, 1, 14, 3, 'FAX:  +81-92-584-2241', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(14, 4, 14, 8, 'FAX:', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(15, 1, 15, 3, 'VAT NO. NL 826346315B01', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(15, 4, 15, 8, 'VAT NO.', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.write(15, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bottom': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(16, 0, 16, 1, 'PLACE OF LOADING', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(16, 2, 16, 3, 'SCHIPOL-RIJK, NETHERLAND	', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(16, 4, 16, 8, 'IMPORTER/BUYER - IF OTHER THAN CONSIGNEE', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(17, 0, 17, 1, 'PLACE OF DELIVERY', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(17, 2, 17, 3, 'MACHELEN, BELGIUM', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(17, 4, 17, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(18, 0, 18, 1, 'COUNTRY OF ORIGIN', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(18, 2, 18, 3, 'JAPAN', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(18, 4, 18, 8, 'LIGNE', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'bold': True, 'font_name': font_name_hgp}))

        sheet.merge_range(19, 0, 19, 3, 'DELIVERY DATE & REQUESTS', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(19, 4, 19, 8, '14, GALERIE DU ROI', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(20, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(20, 1, 20, 3, 'Openings hours:', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bg_color': 'yellow', 'color': 'red', 'font_name': font_name_hgp}))
        sheet.merge_range(20, 4, 20, 8, 'BRUXELLES, BELGIUM 1000', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(21, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(21, 1, 21, 3, 'Wednesday 7:30 - 12:00, 13:00 - 16:30', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bg_color': 'yellow', 'color': 'red', 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(21, 4, 21, 8, 'TEL:           +32 2 511 6030', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(22, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(22, 1, 22, 3, 'Thursday 7:30 - 12:00, 13:00 - 16:30', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bg_color': 'yellow', 'color': 'red', 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(22, 4, 22, 8, 'FAX:', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'font_name': font_name_hgp}))

        sheet.write(23, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(23, 1, 23, 3, 'Friday 7:00 - 9:00', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'bg_color': 'yellow', 'color': 'red', 'bold': True, 'bottom': 2, 'font_name': font_name_hgp}))
        sheet.merge_range(23, 4, 23, 8, 'VAT NO.   BE 0401824775', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'bottom': 2, 'font_name': font_name_hgp}))

        sheet.merge_range(24, 0, 32, 0, 'NOTE', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(24, 1, 32, 8, stock_move_container.note_eng if stock_move_container.note_eng else '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'align': 'left', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'font_name': font_name_hgp}))

        sheet.write(33, 0, 'TOTAL AMOUNT', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(33, 1, 33, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'bold': True, 'font_name': font_name_hgp}))

        sheet.write(34, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(34, 1, 34, 8, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'bold': True, 'font_name': font_name_hgp}))

        sheet.write(35, 0, '', workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'left': 2, 'bottom': 2,  'bold': True, 'font_name': font_name_hgp}))
        sheet.merge_range(35, 1, 35, 8, stock_move_container.pallet_count, workbook.add_format(
            {'font_size': 13, 'valign': 'top', 'right': 2, 'bottom': 2, 'bold': True, 'font_name': font_name_hgp}))

        sheet.merge_range(36, 0, 38, 0, 'No.', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 1, 38, 1, 'ARTICLE', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 2, 38, 2, 'HS CODE', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 3, 38, 3, 'DIMENSIONS     [WxDxH mm]', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 4, 38, 4, 'QTY', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 5, 38, 5, 'GOODS CODE', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 6, 38, 6, 'LOT&SER', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
        sheet.merge_range(36, 7, 38, 8, 'LOCATION	', workbook.add_format(
            {'font_size': 13, 'valign': 'vcenter', 'left': 2, 'right': 2, 'bottom': 2, 'bold': True, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))

        start = 39
        if stock_move_container.pallet_ids:
            for index, pallet in enumerate(stock_move_container.pallet_ids):
                stock_move_lines = pallet.move_ids
                if stock_move_lines:
                    sheet.write(start, 1, f'[{pallet.name}]', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, }))
                    sheet.merge_range(start, 0, start+len(stock_move_lines), 0, index+1, workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'bottom': 2, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
                    sheet.write(start, 2, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 3, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 4, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 5, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 6, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.merge_range(start, 7, start, 8, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                else:
                    sheet.write(start, 0, index+1, workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'left': 2, 'right': 2, 'bottom': 2, 'align': 'center', 'text_wrap': True, 'font_name': font_name_hgp}))
                    sheet.write(start, 1, f'[{pallet.name}]', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'bottom': 2, 'text_wrap': True, }))
                    sheet.write(start, 2, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 3, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 4, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 5, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 6, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.merge_range(start, 7, start, 8, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                start += 1
                for i, line in enumerate(stock_move_lines):
                    product_name_and_attribute = line.product_id.name + '\n'
                    product_template_attribute_values = line.product_id.product_template_attribute_value_ids

                    for index, attr in enumerate(product_template_attribute_values):
                        product_name_and_attribute += '    ' + attr.display_name + '\n'

                    product_name_and_attribute += '    W' + \
                        str(line.product_id.width) + ' x' + ' D' + str(line.product_id.depth) + \
                        ' x' + ' H' + str(line.product_id.height) + ' mm'
                    sheet.write(start, 1, product_name_and_attribute, workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 2, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 3, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 4, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 5, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.write(start, 6, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    sheet.merge_range(start, 7, start, 8, '', workbook.add_format(
                        {'font_size': 13, 'valign': 'top', 'text_wrap': True, 'bottom': 2, 'right': 2, 'top': 2, 'left': 2, 'font_name': font_name_hgp}))
                    start += 1
