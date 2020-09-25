# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': "ClickIt Custom Reports",
    'description': """
        ClickIt COMP 4882 Custom Reports
    """,

    'version': '0.1',
    'depends': ['base','web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/custom_reports_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': True
}