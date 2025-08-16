# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# TODO: Correct the import
from datetime import datetime
import odoo
from odoo import models, fields, api, _
from odoo import http
from odoo.http import request
from requests import Response
import requests
import xmlrpc
import logging
import json
import pytz
import sys
import io
import os
import re
import base64
from odoo.addons.web.controllers.session import Session
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class KitchenAPI(http.Controller):

    def authenticate_token(self):
        IrHttp = request.env['ir.http'].sudo()
        IrHttp._auth_method_outlook()

    @http.route('/token/authenticate', type='json', auth="none", methods=['POST'], csrf=False, save_session=False, cors="*")
    def get_token(self, **post):
        params = post.copy()
        username = params['username']
        password = params['password']
        credential = {'login': username, 'password': password, 'type': 'password'}
        user_id = request.session.authenticate(request.db,credential)
        user_id = user_id.get('uid')
        if not user_id:
            return json.dumps({"error": "Invalid Username or Password."})
        env = request.env(user=request.env.user.browse(user_id))
        t= env['res.users.apikeys.description'].check_access_make_key()
        token = request.env['res.users.apikeys']._generate(
            None,
            username,
            datetime.now() + timedelta(hours=24)

        )
        payload = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'token': token
        }
        res_user = request.env['res.users'].sudo().search([('id','=',user_id)])
        if res_user.has_group('zb_kitchen_display.group_kitchen_user'):
            user_type = 'full'
        elif res_user.has_group('zb_kitchen_display.group_customer_user'):
            user_type = 'readonly'
        else:
            user_type = 'None'
        return {
            "user_type":user_type,
            "user_id":user_id,
            "data": payload,
            "responsedetail": {
            "messages": "UserValidated",
            "messagestype": 1,
            "responsecode": 200
            }
        }
    
    @http.route('/token/delete', type='json', auth="none", methods=['POST'], csrf=False, save_session=False, cors="*")
    def revoke_token(self, **post):
        username = post.get('username')
        password = post.get('password')
        credential = {'login': username, 'password': password, 'type': 'password'}
        user_id = request.session.authenticate(request.db,credential)
        user_id = user_id.get('uid')
        if not user_id:
            return {
                "error": "Invalid credentials",
                "responsecode": 401
            }
        # Find all active keys for the user and deactivate them
        keys = request.env['res.users.apikeys'].sudo().search([
            ('user_id', '=', user_id),
        ])
        if not keys:
            return {
                "message": "No active API key found for this user.",
                "responsecode": 404
            }
        keys.sudo().unlink()  # deactivate
        return {
            "message": "API key(s) deactivated successfully.",
            "responsecode": 200
        }
