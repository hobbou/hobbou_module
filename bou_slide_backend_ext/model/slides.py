# -*- coding: utf-8 -*-

import openerp
import base64
from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
from openerp.tools import config
from openerp.exceptions import ValidationError
from openerp.addons.bou_slide_backend_ext.tinytag import TinyTagException, TinyTag, ID3, Ogg, Wave, Flac
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import metadata
from openerp.addons.bou_slide_backend_ext.hachoir_parser.guess import createParser
from datetime import timedelta


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
    _description = "Hobbou Slides Category"
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
    # content
    slide_type = fields.Selection(selection_add=[
        ('story', 'Story'),
        ('image', 'Image'),
        ('audio', 'Audio')]
        )

    
    file = fields.Binary(string='File', attachment=True, track_visibility='on_change')    
    filename = fields.Char('Filename', track_visibility='on_change')
    mime_type = fields.Char('Mime-type', readonly=True, compute='_get_mime_type')

    def _get_mime_type(self):
        if self.filename.lower().endswith('mp3'):
            self.mime_type = 'mpeg'
        elif self.filename.lower().endswith('wav'):
            self.mime_type = 'wav'
        elif self.filename.lower().endswith('ogg'):
            self.mime_type = 'ogg'
        else:
            self.mime_type = None

    def _get_embed_code(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        for record in self:
            if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
                record.embed_code = '<iframe src="%s/slides/embed/%s?page=1" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (base_url, record.id, 315, 420)
            elif record.slide_type == 'video':
                # if video is on youtube/google
                if record.document_id:
                    if not record.mime_type:
                        # embed youtube video
                        record.embed_code = '<iframe src="//www.youtube.com/embed/%s?theme=light" allowFullScreen="true" frameborder="0"></iframe>' % (record.document_id)
                    else:
                        # embed google doc video
                        record.embed_code = '<embed src="https://video.google.com/get_player?ps=docs&partnerid=30&docid=%s" type="application/x-shockwave-flash"></embed>' % (record.document_id)
                else:
                    record.embed_code = '<video controls><source src="data:video/%s;base64,%s" ></video>' % (self.mime_type, self.file)
            elif record.slide_type == 'audio':
                record.embed_code = '<audio controls src="data:audio/%s;base64,%s" />' % (self.mime_type, self.file)
            else:
                record.embed_code = False
    @api.onchange('channel_id')
    def _onchange_bou_channel(self):
        self.tag_ids = self.channel_id.bou_slide_section_ids

    @api.constrains('name')
    def _check_bou_name(self):
        for slide_id in self:
            if slide_id.name:              
                if len(slide_id.name) <= 7:
                    raise ValidationError(_('Have a longer title will not hurt bro..'))

    @api.constrains('file','filename')
    def _check_file(self):

        allowed_audio = ('.wav', '.mp3', '.m4a')
        allowed_video = ('.mp4', '.mov', '.mpeg4', '.avi', '.wmv', '.flv')

        #writing to temp file
        file_ext = self.filename[-4:].lower()
        if self.filename.lower().endswith(('.jpeg','.webp','.tiff','.docx','.pptx')):
                file_ext = self.filename[-5:].lower()
        if self.filename.lower().endswith('.mpeg4'):
                file_ext = self.filename[-6:].lower()
                
        print file_ext,"file is found"
        with open(config['data_dir']+"\\temp"+file_ext, "wb") as fh:
            fh.write(self.file.decode('base64'))

        if file_ext in allowed_audio:
            self.slide_type = 'audio'

            tag = TinyTag.get(config['data_dir']+"\\temp"+file_ext)
            print "This track is by",tag.artist
            print"It is",tag.duration,"seconds long"
            
            duration = tag.duration
            if duration > 437:
                raise ValidationError("Audio duration is too long. Expected below 7 minutes and 17 seconds")
        elif file_ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.tif', '.tiff'):
            self.slide_type = 'image'
        elif  file_ext in ('.pdf', '.txt', '.doc', '.docx', '.odt'):
            self.slide_type = 'story'
        elif  file_ext in allowed_video:
            self.slide_type = 'video'

            parser = createParser(config['data_dir']+"\\temp"+file_ext)
            metalist = metadata.extractMetadata(parser)
            duration = metalist.get('duration').total_seconds()
            print "duration :",duration

            if duration > 437:
                raise ValidationError(_("Video duration is too long. Expected below 7 minutes and 17 seconds"))

        elif  file_ext in ('.ppt', '.pptx', '.odp'):
            self.slide_type = 'presentation'
        else:
            raise ValidationError(_("Format is not valid."))
    
#end of Slide()

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    bou_channel_ids = fields.One2many('slide.channel', 'bou_user_owner_id', 'Channel List')
    bou_member_in_channel_ids = fields.Many2many('slide.channel', 'bou_channel_user_rel', 'channel_id', 'user_id', 'Member in Channel')
    
#end of ResUsers()