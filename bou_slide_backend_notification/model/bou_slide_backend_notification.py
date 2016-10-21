# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

class BouUserNotification(models.Model):
    _name = 'bou.user.notification'
    _description = 'User Notification'
    _order = 'create_date'
    
    user_id = fields.Many2one('res.users', 'Owner User', required=True)
    active = fields.Boolean(string="Active", default=True)
    channel_id = fields.Many2one('slide.channel', 'Channel', required=True)   
    notification_type = fields.Selection(
        [
            ('subcribe', 'Subcribe'),
            ('endorse', 'Endorse'),
            ('like', 'Like'),
            ('playlist', 'Playlist'),
            ('comment', 'Comment'),
            ('event', 'Event'),
            ('news', 'News'),
            ('update', 'Update'),
            ('follow', 'Follow'),
            ('discover', 'Discover'),
        ], string="Notification Type", required=True)
    content_id = fields.Many2one('slide.slide', 'Content')
    sender_id = fields.Many2one('res.users', 'Sender', required=True)
    description = fields.Text('Description', required=True)
    read = fields.Boolean('Read')
    
#end of BouUserNotification()

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    fal_notification_ids = fields.One2many('bou.user.notification', 'user_id', 'Notification')
    
#end of ResUsers()