# -*- coding: utf-8 -*-
{
    "name": "Hobbou Slide Backend Extention",
    "version": "1.0",
    'author': 'Hobbou',
    "description": """
    Module to modify, extends, and improve the website_slide module.
    """,
    "depends" : ['website_slides'],
    'init_xml': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bou_slides_backend_ext_view.xml',
    ],
    'css': [],
    'js' : [],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: