# -*- coding: utf-8 -*-
{
    'name': "change_attachment_file_send_email",

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
    'depends': ['base', 'account', 'sale', 'purchase', 'custom_report_rtw','mail'],

    # always loaded
    'data': [
        'views/attachment_sale.xml',
        'views/attachment_po.xml',
        'views/attachment_invoice.xml'
    ],
}