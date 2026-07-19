{
    'name': "Bakery Manager",

    'summary': "Module to manage your bakery",

    'description': """
You can use this module to sell your baked goods and recieve orders from customers.
    """,

    'author': "Yara Ramy",
    'website': "https://www.linkedin.com/in/yara-ramy",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/cart_wizard.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/bakery_item_views.xml',
        'views/bakery_order_views.xml',
        'views/cart_views.xml',
        'views/checkout_views.xml',
        'views/profile_views.xml',
        'views/bakery_info_views.xml',
        'views/menus.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

