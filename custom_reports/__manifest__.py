# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': "ClickIt Custom Reports",
    'description': """
        ClickIt COMP 4882 Custom Reports
    """,

    'version': '0.1',
    'depends': ['base','hr', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/employee_performance_views.xml',
        'views/custom_reports_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True
}