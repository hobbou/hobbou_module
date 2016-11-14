# -*- coding: utf-8 -*-

import odoo
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class Slide(models.Model): 
    _inherit = 'slide.slide'   
                    
    fal_comment_ids = fields.One2many('bou.comment', 'content_id', 'Content Commentaires')
    
#end of Slide()
