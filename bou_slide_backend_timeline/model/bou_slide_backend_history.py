# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp.exceptions import ValidationError

class BouUserWatchHistory(models.Model):
    _name = 'bou.user.watch.history'
    _description = 'User watch history'

    user_id = fields.Many2one('res.users', 'User')
    content_id = fields.Many2one('slide.slide', 'Content')
    is_display = fields.Boolean('Is Display', default=True)
    
#end of BouUserWatchHistory()

class BouUserSearchHistory(models.Model):
    _name = 'bou.user.search.history'
    _description = 'User search history'

    user_id = fields.Many2one('res.users', 'User')
    name = fields.Char('Search Term', size=77)
    is_display = fields.Boolean('Is Display', default=True)
    
#end of BouUserSearchHistory()