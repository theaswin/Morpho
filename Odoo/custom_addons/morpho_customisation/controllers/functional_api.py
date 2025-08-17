from odoo import http
from odoo.http import request
import requests
import re

def format_url(raw_url):
    match = re.search(r'^.*?\.com', raw_url)
    if match:
        format_url = match.group()
        return format_url
    else:
        return "Invalid URL"

def whole_data(model,org_id):
    output = []
    records = request.env[model].sudo().search([('org_id','=',org_id)])

    for rec in records:
        output.append({
            'logo':rec.image_1920,
            'name':rec.name,
            'type':rec.type,
            'category':rec.categ_id.name,
            'price':rec.list_price,

        })
    return output

class FunctionalController(http.Controller):

    @http.route(['/get/iterate_section/'], type='json', auth='public', methods=['GET'], csrf=False, cors="*")
    def get_rzp_order_id(self,**post):
        org_id = post.get('organisation_id')
        model = post.get('model')

        return whole_data(model=model,org_id = org_id)


