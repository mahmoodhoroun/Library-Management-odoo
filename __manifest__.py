{
    'name': 'Library Management',
    'category': 'Library Management/Library Management',
    'description': "",
    'website': 'https://www.odoo.com/page/library_management',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/library_book_views.xml',
        'views/library_auther_views.xml',
        'views/library_menus.xml',
        'report/library_auther_report.xml'
     ],
    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False
}