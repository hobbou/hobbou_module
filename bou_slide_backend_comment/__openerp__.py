# -*- coding: utf-8 -*-
{
    "name": "HowBou Slide Backend Comment",
    "version": "1.0",
    'author': 'HowBou',
    "description": """
    Comment backend for the content.
    """,
    "depends" : ['bou_slide_backend_timeline'],
    'init_xml': [],
    'data': [
        'security/ir.model.access.csv',
        'views/bou_slides_backend_view.xml',
    ],
    'css': [],
    'js' : [],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: