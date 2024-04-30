# -*- coding: utf-8 -*-
{
    'name': "rtw_excel_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'excel_import_export', 'sale_management', 'sale','sale_sourced_by_line','product','purchase','stock_move_container','stock_move_pallet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/proforma.xml',
        'report/report.xml',
        # 'report_quotation/actions.xml',
        # 'report_quotation/templates.xml',
        # 'report_quotation_oversea/actions.xml',
        # 'report_quotation_oversea/templates.xml',
        # 'report_list_price_quotation/actions.xml',
        # 'report_list_price_quotation/templates.xml',
        # 'report_unit_price_quotation/actions.xml',
        # 'report_unit_price_quotation/templates.xml',
        # 'report_invoice/actions.xml',
        # 'report_invoice/templates.xml',
        # 'report_invoice_sale_order/actions.xml',
        # 'report_invoice_sale_order/templates.xml',

        # 'report_purchase_order/actions.xml',
        # 'report_purchase_order/templates.xml',

        'report_purchase_order_sheet/actions.xml',
        'report_purchase_order_sheet/templates.xml',
        'report_inspection_order_form/actions.xml',
        'report_inspection_order_form/templates.xml',

        # 'report_purchase_order_for_part/actions.xml',
        # 'report_purchase_order_for_part/templates.xml',
        'report_delivery_request_form/actions.xml',
        'report_delivery_request_form/templates.xml',
        'report_ship_order/actions.xml',
        'report_ship_order/templates.xml',

        'views/views.xml',
        'views/product_spec.xml',
        'views/work_progress_slip_list.xml',
        'views/product_label_sticker.xml',
        'views/inventory_import_list.xml',
        'views/inspection_check_sheet.xml',
        'views/stock_status_list.xml',
        'views/shipping_list.xml',
        'views/invoice_sticker.xml',
        'views/scheduled_payment_list.xml',
        'views/scheduled_arrival_list.xml',
        'views/supplied_material_detail.xml',
        'views/stock_move_pallet.xml',
        'views/report_quotation.xml',
        'views/report_quotation_oversea.xml',
        'views/list_price_quotation.xml',
        'views/unit_price_quotation.xml',
        'views/purchase_order.xml',
        'views/purchase_order2.xml',
        'views/invoice_sale_order.xml',
        'views/invoice_account_move.xml',
        'views/purchase_order_for_part.xml',

        # 'report_stock_move_pallet/actions.xml',
        # 'report_stock_move_pallet/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
