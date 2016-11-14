# -*- coding: utf-8 -*-

import odoo
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval
from odoo.tools.translate import _

class BouComment(models.Model):
    _name = 'bou.comment'
    _description = 'Comment'
    _order = 'create_date'
    
    active = fields.Boolean(string="Active", default=True)
    sender_id = fields.Many2one('res.users', 'Sender', required=True)
    content_id = fields.Many2one('slide.slide', 'Content')
    comment = fields.Text('Comment', required=True)
    comment_thread_id = fields.Many2one('bou.comment', 'Thread')
    comment_reply_ids = fields.One2many('bou.comment', 'comment_thread_id', 'Replies')
    channel_id = fields.Many2one('slide.channel', 'Channel', required=True)   
    comment_type = fields.Selection(
        [
            ('content_comment', 'Content Comment'),
            ('content_comment_reply', 'Content Comment Reply'),
            ('channel_comment', 'Channel Comment'),
            ('channel_comment_reply', 'Channel Comment Reply'),
        ], string="Comment Type", required=True)
        
#end of BouComment()

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    fal_comment_send_ids = fields.One2many('bou.comment', 'sender_id', 'Comment Sent')
    
#end of ResUsers()

class Channel(models.Model):
    _inherit = 'slide.channel'
    
    fal_comment_ids = fields.One2many('bou.comment', 'channel_id', 'Channel Commentaires')
    
#end of Channel()