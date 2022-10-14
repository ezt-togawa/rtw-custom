# -*- coding: utf-8 -*-
{
    'name': "rtw_lettermgmt",

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
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_letter_view.xml',
        'views/letter_category_view.xml',
        'views/letter_type_view.xml',
        'views/letter_channel_view.xml',
        'views/letter_folder_view.xml',
        'views/letter_reassignment_view.xml',
        'data/letter_sequence.xml',
        'security/ir.model.access.csv',
        'security/lettermgmt_security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
