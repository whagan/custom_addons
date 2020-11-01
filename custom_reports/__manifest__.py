# -*- coding: utf-8 -*-
{
    'name': "Custom Reports",

    'summary': "Custom Reports",
    'description': """
        ClickIt COMP 4882 Custom Reports
    """,

    'version': '0.1',
    'depends': ['base', 'hr', 'hr_attendance', 'mass_mailing', 'product', 'point_of_sale', 'purchase', 'sale', 'sale_management', 'stock', 'web'],
    
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/sales_by_location_reports_views.xml',
        'views/employee_performance_reports_views.xml',
        'views/email_marketing_reports_views.xml',
        'views/contact_report_view.xml',
        'views/sales_statistics_reports_views.xml',
        'views/restock_report_view.xml',
        'views/custom_reports_views.xml',
    ],
    'demo': [
        'demo/employee_performance_demo.xml',
        'demo/email_marketing_demo.xml',
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/employee_performance_graph.xml',
        'static/src/xml/email_marketing_graph.xml',
        'static/src/xml/sales_statistics_graph.xml',
    ],
    
    
    'installable': True,
    'application': True,
    'auto_install': True
}