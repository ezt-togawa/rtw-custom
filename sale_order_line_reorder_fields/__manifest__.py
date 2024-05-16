# -*- coding: utf-8 -*-
{
    'name': "sale_order_line_reorder_fields",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Enzantrades",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'sale_sourced_by_line', 'stock' , 'sale' , 'sale_order_rtw' , 'product_spec_rtw', 'sale_order_line_planned_date' , 'sale_order_line_product_pack' ,
                'sale_order_line_outlook_stock','sale_order_line_delivery_confirmation','sale_order_line_warehouse','sale_line_bom_stock','sale_stock','product_configurator_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
