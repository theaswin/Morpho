from odoo import http
from odoo.http import request
import re

def format_url(raw_url):
    match = re.search(r'^.*?\.com', raw_url)
    if match:
        format_url = match.group()
        return format_url
    else:
        return "Invalid URL"

def extract_non_binary_data(model):
    datas = {}
    for rec in model:
        for field_name, field in rec._fields.items():
            if field.type != 'binary':
                value = getattr(rec, field_name)
                datas[field_name] = value
    return datas

def extract_binary_data(model):
    datas = {}
    for rec in model:
        for field_name, field in rec._fields.items():
            if field.type == 'binary':
                value = getattr(rec, field_name)
                datas[field_name] = value
    return datas

def whole_data(model):
    datas = {}
    for rec in model:
        for field_name, field in rec._fields.items():
            value = getattr(rec, field_name)
            datas[field_name] = value
    return datas

class webController(http.Controller):

    @http.route(['/get/web_data'], type='json', auth='public', methods=['GET'], csrf=False, cors="*")
    def get_non_binary_data(self, **kwargs):
        web_url = kwargs.get('web_url')        
        backend = request.env['morpho.backend'].search([
            ('website','=',format_url(web_url)),
            ('status','=','live')

        ])
        return extract_non_binary_data(backend)

    @http.route(['/get/web_images'], type='json', auth='public', methods=['GET'], csrf=False, cors="*")
    def get_binary_data(self, **kwargs):
        web_url = kwargs.get('web_url')
        datas = {}
        
        backend = request.env['morpho.backend'].search([
            ('website','=',format_url(web_url)),
            ('status','=','live')
        ])
        return extract_binary_data(backend)

    @http.route(['/get/sections'], type='json', auth='public', methods=['GET'], csrf=False, cors="*")
    def get_cms_web_data(self, **kwargs):
        web_url = kwargs.get('web_url')
        datas = []
        
        backend = request.env['morpho.backend'].sudo().search([
            ('website','=',format_url(web_url))
        ])
        for section in backend.general_sections_ids:
            datas.append(
                {
                    'sequence':section.sequence,
                    'section_id':section.section_id.id,
                    'section_name':section.section_id.name,
                    'section_organisation':section.section_id.organisation_id.name,
                    'section_code':section.section_id.code,
                    'section_title':section.title,
                    'section_description':section.description,
                    'section_design':section.design,
                    'section_image_ids':[img.datas for img in section.image_ids],
                    'section_color':section.color,
                })
        return datas