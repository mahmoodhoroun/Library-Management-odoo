{
    'name': 'Library Management',
    'category': 'Library Management/Library Management',
    'description': "",
    'website': 'https://www.odoo.com/page/library_management',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_auther_views.xml',
        'views/library_reservations_views.xml',
        'views/res_partner_views.xml',
        'wizerd/update_book_price_wizard_views.xml',
        'views/views.xml',
        'views/library_menus.xml',
        'report/library_auther_report.xml',
        'report/report_library_book.xml',
        'data/ir_cron.xml',
     ],
    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}