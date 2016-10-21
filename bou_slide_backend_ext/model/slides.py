# -*- coding: utf-8 -*-

import openerp
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp.exceptions import ValidationError

class Channel(models.Model):
    _inherit = 'slide.channel'
    
    name = fields.Char(size=77)            
    active = fields.Boolean(string="Active", default=True)
    bou_slide_category_id = fields.Many2one('bou.slide.category', string="Category", required=True, help="Specify the category of channel, and section to have default value on each slide on this channel.")
    bou_slide_section_ids = fields.Many2many('slide.tag', 'bou_channel_section_rel', 'channel_id', 'section_id', 'Sections', required=True, domain="[('bou_category_ids', '=', bou_slide_category_id)]", help="Specify the category of channel, and section to have default value on each slide on this channel.")
    bou_user_owner_id = fields.Many2one('res.users', 'Owner', required=True)
    bou_team_member_ids = fields.Many2many('res.users', 'bou_channel_user_rel', 'user_id', 'channel_id', 'Team Member')
    
    @api.constrains('name')
    def _check_bou_name(self):
        for channel_id in self:
            if channel_id.name:
                channel_exist = self.search([('name', '=ilike', channel_id.name)])
                if len(channel_exist.ids) != 1:
                    raise ValidationError(_('Too late bro, this channel is already taken..'))                    
                if len(channel_id.name) < 3:
                    raise ValidationError(_('You must have a longer name bro..'))

    _sql_constraints = [
        ('bou_channel_unique', 'UNIQUE(name)', 'Channel must be unique!'),
    ]
    
#end of Channel()

class BouSlideCategory(models.Model):
#we create a new class of category because the current class not fit our requirement
    _name = 'bou.slide.category'
    _description = "HowBou Slides Category"
    _order = "sequence, id"
    
    active = fields.Boolean(string="Active", default=True)
    name = fields.Char('Name', translate=True, required=True)
    description = fields.Text('Description', translate=True)
    sequence = fields.Integer(default=10, help='Display order')
    channel_ids = fields.One2many(
        'slide.channel', 'bou_slide_category_id', string="List of Channel")    
    slide_ids = fields.One2many(
        'slide.slide', 'bou_slide_category_id', string="List of Slide")
    
    slide_tag_ids = fields.Many2many('slide.tag', 'bou_tag_category_rel', 'category_id', 'tag_id', 'List of Tag')

    _sql_constraints = [
        ('bou_slide_category_unique', 'UNIQUE(name)', 'Category must be unique!'),
    ]

    @api.constrains('name')
    def _check_category_unique_insesitive(self):
        for category_id in self:
            if category_id.name:
                category_exist = self.search([('name', '=ilike', category_id.name)])
                if len(category_exist) != 1:
                    raise ValidationError(_('Category must be unique!'))
    
#end of BouCategory()

class Category(models.Model):
    _inherit = 'slide.category'

#end of Category()

class SlideTag(models.Model):
    _inherit = 'slide.tag'
    _order = "sequence, id"
    
    active = fields.Boolean(string="Active", default=True)
    description = fields.Text('Description', translate=True)
    sequence = fields.Integer(default=10, help='Display order')
    bou_category_ids = fields.Many2many('bou.slide.category', 'bou_tag_category_rel',  'tag_id', 'category_id', 'List of Category')
    bou_channel_ids = fields.Many2many('slide.channel', 'bou_channel_section_rel',  'section_id', 'channel_id', 'List of Channel')
    bou_slide_ids = fields.Many2many(
        'slide.slide', 'rel_slide_tag', 'slide_id', 'tag_id', string='Slides')
    bou_tag_highlight = fields.Boolean('Highlight')

    @api.constrains('name')
    def _check_tag_unique_insesitive(self):
        for tag_id in self:
            if tag_id.name:
                tag_exist = self.search([('name', '=ilike', tag_id.name)])
                if len(tag_exist) != 1:
                    raise ValidationError(_('Tag must be unique!'))
    
#end of SlideTag()

class Slide(models.Model): 
    _inherit = 'slide.slide'   
                    
    name = fields.Char(size=77)
    active = fields.Boolean(string="Active", default=True)
    bou_slide_category_id = fields.Many2one(related='channel_id.bou_slide_category_id', comodel_name='bou.slide.category', string="Category", store=True, readonly=True)
    tag_ids = fields.Many2many(string="Sections", domain="[('bou_category_ids', '=', bou_slide_category_id)]", required=True)

    @api.onchange('channel_id')
    def _onchange_bou_channel(self):
        self.tag_ids = self.channel_id.bou_slide_section_ids

    @api.constrains('name')
    def _check_bou_name(self):
        for slide_id in self:
            if slide_id.name:              
                if len(slide_id.name) <= 7:
                    raise ValidationError(_('Have a longer title will not hurt bro..'))
    
#end of Slide()

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    bou_channel_ids = fields.One2many('slide.channel', 'bou_user_owner_id', 'Channel List')
    bou_member_in_channel_ids = fields.Many2many('slide.channel', 'bou_channel_user_rel', 'channel_id', 'user_id', 'Member in Channel')
    
#end of ResUsers()