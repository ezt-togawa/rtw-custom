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
    'depends': ['base', 'excel_import_export', 'sale_management', 'sale','sale_sourced_by_line','product','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/proforma.xml',
        'report/report.xml',
        'report_quotation/actions.xml',
        'report_quotation/templates.xml',
        'report_list_price_quotation/actions.xml',
        'report_list_price_quotation/templates.xml',
        'report_unit_price_quotation/actions.xml',
        'report_unit_price_quotation/templates.xml',
        'report_invoice/actions.xml',
        'report_invoice/templates.xml',
        
        'report_purchase_order/actions.xml',
        'report_purchase_order/templates.xml',
        'report_purchase_order_sheet/actions.xml',
        'report_purchase_order_sheet/templates.xml',
        'report_purchase_order_for_part/actions.xml',
        'report_purchase_order_for_part/templates.xml',
        'report_delivery_request_form/actions.xml',
        'report_delivery_request_form/templates.xml',
        'report_ship_order/actions.xml',
        'report_ship_order/templates.xml',

        'views/views.xml',
        'views/product_spec.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
