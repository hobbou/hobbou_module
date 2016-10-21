# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = "res.users"
    
    bou_user_watch_history_line_ids = fields.One2many('bou.user.watch.history', 'user_id', 'Watch History')
    bou_user_search_history_line_ids = fields.One2many('bou.user.search.history', 'user_id', 'Search History')
    bou_user_playlist_line_ids = fields.One2many('bou.playlist', 'user_id', 'Playlist')
    bou_channel_subscribed_line_ids = fields.One2many('bou.channel.subscribed.line', 'user_id', 'Subscribeds')
    bou_album_follow_line_ids = fields.One2many('bou.playlist.follower.line', 'user_id', 'Follow Album')
    
    @api.one
    @api.constrains('bou_album_follow_line_ids')
    def _check_bou_album_follow_line_ids(self):
        temp = []
        for bou_album_follow_line_id in self.bou_album_follow_line_ids:
            if bou_album_follow_line_id.playlist_id.user_id.id == self.id:
                raise ValidationError(_('You cannot follow your own playlist bro..'))
            if  bou_album_follow_line_id.playlist_id.id not in temp:
                temp.append(bou_album_follow_line_id.playlist_id.id)
            else:
                raise ValidationError(_('You already followed the playlist bro..'))   
                
    
#end of ResUsers()

class Channel(models.Model):
    _inherit = 'slide.channel'
    
    bou_post_ids = fields.One2many('bou.channel.post', 'channel_id', 'Timeline')
    bou_playlist_ids = fields.One2many('bou.playlist', 'channel_id', 'Album')
    bou_channel_subscriber_line_ids = fields.One2many('bou.channel.subscribed.line', 'channel_id', 'Subscriber')

    def action_open_channel_timeline(self, cr, uid, ids, context=None):
        result = self.pool['ir.model.data'].xmlid_to_res_id(cr, uid, 'bou_slide_backend_timeline.action_open_channel_timeline_tree', raise_if_not_found=True)
        result = self.pool['ir.actions.act_window'].read(cr, uid, [result], context=context)[0]
        result['domain'] = "[('channel_id','in',[" + ','.join(map(str, ids)) + "])]"
        return result
        
#end of Channel()

class BouChannelSubscribedLine(models.Model):
    _name = "bou.channel.subscribed.line"
    _description = 'List of Subscriber'
    
    sequence = fields.Integer(default=10, help='Display order')
    user_id = fields.Many2one('res.users', 'Subscriber')
    channel_id = fields.Many2one('slide.channel', 'Channel')
        
#end of BouChannelSubscribedLine()

class BouPlaylistFollowerLine(models.Model):
    _name = "bou.playlist.follower.line"
    _description = 'List of Follower'
    
    sequence = fields.Integer(default=10, help='Display order')
    user_id = fields.Many2one('res.users', 'Follower')
    playlist_id = fields.Many2one('bou.playlist', 'Playlist')
    
#end of BouPlaylistFollowerLine()