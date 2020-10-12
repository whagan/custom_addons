# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': "Custom Reports",
    'description': """
        ClickIt COMP 4882 Custom Reports
    """,

    'version': '0.1',
    'depends': ['base', 'hr', 'hr_attendance', 'mass_mailing', 'sale', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/employee_performance_reports_views.xml',
        'views/email_marketing_reports_views.xml',
        'views/custom_reports_views.xml',
    ],
    'demo': [
        'demo/email_marketing_demo.xml',
        'demo/custom_reports_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True
}