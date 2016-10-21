# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

class BouChannelPost(models.Model):
    _name = 'bou.channel.post'
    _description = 'Channel Post'
    _rec_name = 'description'
    
    active = fields.Boolean(string="Active", default=True)
    channel_id = fields.Many2one('slide.channel', 'Channel', required=True)   
    post_type = fields.Selection(
        [
            ('pict', 'Picture'),
            ('vid', 'Video'),
            ('story', 'Story'), 
            ('sound', 'Sound'), 
            ('subcribed', 'Subcribed'),
            ('endorsed', 'Endorsed'),
            ('liked', 'Liked'),
            ('playlist', 'Playlist'),
        ], string="Post Type", required=True)
    content_id = fields.Many2one('slide.slide', 'Content')
    playlist_id = fields.Many2one('bou.playlist', 'Playlist')
    description = fields.Text('Description')
    
#end of BouChannelPost()