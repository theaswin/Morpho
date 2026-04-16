from odoo import models, fields

class Organisation(models.Model):
    _name = 'org.organisation'
    _description = 'Hostel Organisation'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    vat = fields.Char(string='VAT')
    location = fields.Char(string='Location')
    mobile = fields.Char(string='Mobile')
    owner_id = fields.Many2one('res.partner', string='Owner')
    room_ids = fields.One2many('hostel.room', 'organisation_id', string='Rooms')
    partner_ids = fields.Many2many('res.partner', string='Partners')
