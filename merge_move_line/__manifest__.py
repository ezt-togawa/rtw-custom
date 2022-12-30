# -*- coding: utf-8 -*-

{
    'name': "Marge Move Line",
    'author': "My Company",
    'category': 'stock',
    'summary': """Marge Move Line""",
    'website': 'http://www.yourcompany.com',
    'description': """
""",
    'version': '14.0.0.0',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/merge_move_line_wizard_view.xml',
        'views/templates.xml',
    ],
}
