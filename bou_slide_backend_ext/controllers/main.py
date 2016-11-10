# -*- coding: utf-8 -*-
import werkzeug
import json
from openerp.http import request
from openerp import http
import json

class website_hobbou(http.Controller):

    # get slide content, order by newest, most liked, etc.
    @http.route(['/slide','/slide/order/<string:order>','/slide/tag/<string:tag>',
        '/slide/tag/<string:tag>/order/<string:order>','/slide/category/<string:category>',
        '/slide/category/<string:category>/order/<string:order>','/slide/type/<string:bou_type>',
        '/slide/type/<string:bou_type>/order/<string:order>'], type='http', auth='public', website=True)
    def get_slide(self, order=False,tag=False,category=False,bou_type=False):
        domain = []
        if bou_type:
            domain.append(('slide_type','=',bou_type))
        if tag:
            tag_obj = request.env['slide.tag'].search([('name','=',tag)])
            tag_ids = []
            for tag_id in tag_obj:
                tag_ids.append(tag_id.id)
            domain.append(('tag_ids','in',tag_ids))
        if category:
            category_obj = request.env['slide.category'].search([('name','=',category)])
            category_ids = []
            for category_id in category_obj:
                category_ids.append(category_id.id)
            domain.append(('category_id','in',category_ids))

        if order == 'likes':#most like
            slides = request.env['slide.slide'].search(domain,order='likes desc')
        elif order == 'views': #most view
            slides = request.env['slide.slide'].search(domain,order='total_views desc')
        else:#newest
            slides = request.env['slide.slide'].search(domain,order='create_date desc')
        # print "slides :",slides
        slide_list = []
        if not len(slides):
            slide_list.append({
            'err' : 1,
            'error' : 'record not found'
            })
        for slide in slides:
            # tags = []
            # for tag in slide.tag_ids:
            #     tags.append(tag.name)
            a_slide = {
            'type' : slide.slide_type,
            'tag' : [tag.name for tag in slide.tag_ids],
            'category' : slide.bou_slide_category_id.name,
            'name' : slide.name,
            'channel' : slide.channel_id.name,
            'published' : slide.create_date,
            'likes' :slide.likes,
            'views' : slide.total_views
            }
            slide_list.append(a_slide)
        return json.dumps(slide_list)

    # get suscribed content
    @http.route('/subscribed', type='http', auth='public', website=True)
    def get_subscribed_content(self):
        bou_chan_subs_lines = request.env['bou.channel.subscribed.line'].search([('user_id','=',request.env.user.id)])
        subs = []
        channels = []

        slides = []
        if not len(bou_chan_subs_lines):
            item = {
            'err' : 1,
            'error' : 'record not found'
            }
            channels.append(item)

        for bou_chan_subs_line in bou_chan_subs_lines:
            slide_obj = request.env['slide.slide'].search([('channel_id','=',bou_chan_subs_line.channel_id.id)])
            for slide in slide_obj:
                a_slide = {
                'name' : slide.name,
                'published' : slide.create_date,
                'likes' :slide.likes,
                'dislikes' : slide.dislikes
                }
                slides.append(a_slide)
            a_channel = {
            'channel_id' : bou_chan_subs_line.channel_id.id,
            'channel_name' : bou_chan_subs_line.channel_id.name,
            'slides' : slides[:]
            }
            channels.append(a_channel)
            del slides[:]
        return json.dumps(channels)

#end of website_hobbou()