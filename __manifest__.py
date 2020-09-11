# -*- coding: utf-8 -*-
{
    'name': "reports",

    'summary': """
        ClickIt Reports module""",

    'description': """
        ClickIt Reports module for COMP 4882 capstone project
    """,

    'author': "ClickIt",
    'website': "http://www.clickit.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/reports.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
