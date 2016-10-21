# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp.exceptions import ValidationError


class Slide(models.Model): 
    _inherit = 'slide.slide'   
                    
    fal_comment_ids = fields.One2many('bou.comment', 'content_id', 'Content Commentaires')
    
#end of Slide()
