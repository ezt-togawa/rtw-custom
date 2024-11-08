# -*- coding: utf-8 -*-
{
    'name': "rtw_mrp_custom",

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
    'category': 'Manufacturing',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp','rtw_mrp_add_sol_date', 'sales_mo_sequence', 'sales_team',
                'sale_mrp', 'sale_order_crm_case', 'rtw_mrp_order_manage','mail','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'security/ir.model.access.csv',
        'views/revised_edition.xml',
        'views/mrp_production.xml',
        'views/mrp_workorder.xml',
        'views/mrp_stock_picking.xml',
        'views/mrp_ship_address.xml',
        'views/sale_to_mrp_list.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
