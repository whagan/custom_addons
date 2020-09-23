# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': "ClickIt Custom Reports",
    'description': """
        ClickIt COMP 4882 Custom Reports
    """,

    'version': '0.1',
    'depends': ['web'],
    'data': [
        "views/assets.xml",
        "views/custom_reports_view.xml"
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': True
}