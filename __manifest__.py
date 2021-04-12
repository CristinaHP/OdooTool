# -*- coding: utf-8 -*-
{
    'name': "nueva_herramienta",

    'summary': """
        Nueva herramienta de Cristina para Odoo""",

    'description': """
        Ésta es una nueva herramienta para Odoo, realizada por Cristina en el módulo de Sistemas de
        Gestión Empresarial
    """,

    'author': "Cristina",
    'website': "https://edu-examensge.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/nomina.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}