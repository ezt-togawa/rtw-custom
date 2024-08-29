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
        # sale
        'report/sale_quotation.xml',
        'report/sale_quotation_oversea.xml',
        'report/sale_list_price_quotation.xml',
        'report/sale_unit_price.xml',
        'report/sale_order_form.xml',
        'report/sale_list_order_form.xml',
        'report/sale_product_spec.xml',
        'report/sale_delivery_order.xml',
        'report/sale_invoice.xml',
        
        # delivery
        'report/picking_delivery_order.xml',
        'report/picking_shipping_order.xml',
        
        # invoice
        'report/account_invoice.xml',
        
        # purchase order
        'report/purchase_order_component.xml',
        
        # mrp
        'report/mrp_purchase_order.xml',
        'report/mrp_purchase_order_inspection.xml',
        
        #general
        'report/external_layout.xml',
        'report/internal_layout.xml',
        'report/header_footer.xml',
        'views/views.xml',
        'views/templates.xml',
        "views/res_company_view.xml",
        
        'report/purchase.xml',
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