# -*- coding: utf-8 -*-
{
    'name': "custom_report_rtw",

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
    'depends': ['base', 'sale', 'account', 'product_spec_rtw',
                'rtw_mrp_custom', 'rtw_product_attribute_value_images','excel_import_export'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # quotation
        'report/report_quotation.xml',
        'report/report_quotation_oversea.xml',
        'report/report_list_price_quotation.xml',
        'report/report_unit_price.xml',
        'report/purchase_order.xml',
        'report/purchase_order_fixed_price.xml',
        'report/report_product_spec.xml',
        'report/report_delivery_order_sale.xml',
        
        # delivery
        'report/report_delivery_order.xml',
        'report/report_shipping_order.xml',
        
        # invoice
        'report/report_invoice.xml',
        'report/report_invoice_sale_order.xml',
        
        # purchase order
        'report/purchase_order_sheet_for_part.xml',
        
        # mrp
        'report/purchase_order_sheet.xml',
        'report/inspection_order_form.xml',
        
        #general
        'report/external_layout.xml',
        'report/internal_layout.xml',
        'report/header_footer.xml',
        'views/views.xml',
        'views/templates.xml',
        "views/res_company_view.xml",
        
        'report/purchase.xml',
        'report/spec_list.xml',
        'report/mrp.xml',
        'report/invoice.xml',
        
        # 'report/stock_picking.xml',
        # "views/sale_views.xml",
        # "views/assets.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}