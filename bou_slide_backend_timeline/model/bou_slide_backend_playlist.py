# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

class BouPlaylist(models.Model):
    _name = 'bou.playlist'
    _description = 'Playlist'
    
    active = fields.Boolean(string="Active", default=True)
    name = fields.Char('Name', size=77, required=True)
    user_id = fields.Many2one('res.users', 'Owner User', required=True)
    follower_line_ids = fields.One2many('bou.playlist.follower.line', 'playlist_id', 'Followers')
    channel_id = fields.Many2one('slide.channel', 'Owner Channel')
    type = fields.Selection(
        [
            ('album', 'Album'),
            ('playlist', 'Playlist'),
            ('save', 'Save'),
            ('like', 'Like'),
            ('endorsed', 'Endorsed'),
            ('discover', 'Discover'),
        ], string="Type", required=True)
    sequence = fields.Integer(default=10, help='Display order')
    bou_playlist_line_ids = fields.One2many('bou.playlist.line', 'playlist_id', 'Playlist Line')
    description = fields.Text('Description')
    
#end of BouPlayList()

class BouPlaylistLine(models.Model):
    _name = 'bou.playlist.line'
    _description = 'Playlist Line'
    
    sequence = fields.Integer(default=10, help='Display order')
    playlist_id = fields.Many2one('bou.playlist', 'Playlist')
    content_id = fields.Many2one('slide.slide', 'Content')
    
#end of BouPlayListLine()