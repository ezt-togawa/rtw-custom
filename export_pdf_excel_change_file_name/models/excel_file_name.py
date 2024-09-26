from odoo import models , _
from datetime import datetime
from pytz import timezone  

class ExcelFileNameCus(models.AbstractModel):
    _inherit = "report.report_xlsx.abstract"

    def create_xlsx_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)

        if len(objs) > 1:  # only export list
            def _update_report_file(reports, current_time):
                for report in reports:
                    report.write({"report_file": f"{report.name}_{current_time}"})
            user_tz = self.env.user.tz or "Asia/Tokyo" or "UTC"
            local_tz = timezone(user_tz)
            current_time = datetime.now(local_tz).strftime("%Y-%m-%dT%H%M%S")
            if objs._name == "purchase.order":
                pos = self.env.ref("rtw_excel_report.purchase_order_component").with_context({"lang": self.env.user.lang})
                _update_report_file(pos, current_time)
            elif objs._name == "stock.picking":
                picking_xml_ids = ["picking_scheduled_arrival_list", "picking_scheduled_shipment_list", "picking_scheduled_supply_list"]
                pickings = [self.env.ref(f"rtw_excel_report.{pid}").with_context({"lang": self.env.user.lang}) for pid in picking_xml_ids]
                _update_report_file(pickings, current_time)
            elif objs._name == "mrp.production":
                mrp_xml_ids = ["mrp_product_label_seal", "mrp_purchase_order_inspection", "mrp_purchase_order", "mrp_wip_product_list"]
                mrps = [self.env.ref(f"rtw_excel_report.{mid}").with_context({"lang": self.env.user.lang}) for mid in mrp_xml_ids]
                _update_report_file(mrps, current_time)

        return super(ExcelFileNameCus, self).create_xlsx_report(docids, data)
    