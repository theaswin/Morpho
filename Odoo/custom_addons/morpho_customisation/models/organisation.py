from odoo import models, fields, api

class Organisation(models.Model):
    _name = 'org.organisation'
    _description = 'Hostel Organisation'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    logo = fields.Binary(string='Logo')
    vat = fields.Char(string='VAT')
    location = fields.Char(string='Location')
    mobile = fields.Char(string='Mobile')
    owner_id = fields.Many2one('res.partner', string='Owner')
    room_ids = fields.One2many('hostel.room', 'organisation_id', string='Rooms')
    partner_ids = fields.Many2many('res.partner', string='Partners')

    total_rooms = fields.Integer(string='Total Rooms', compute='_compute_stats', store=True)
    total_beds = fields.Integer(string='Total Beds', compute='_compute_stats', store=True)
    occupied_count = fields.Integer(string='Occupied', compute='_compute_stats', store=True)
    vacant_count = fields.Integer(string='Vacant', compute='_compute_stats', store=True)
    default_message = fields.Text(string='Default Message')

    @api.depends('room_ids', 'room_ids.bed_ids', 'room_ids.bed_ids.partner_id')
    def _compute_stats(self):
        for org in self:
            rooms = org.room_ids
            beds = rooms.mapped('bed_ids')
            occupied = beds.filtered(lambda b: b.partner_id)
            org.total_rooms = len(rooms)
            org.total_beds = len(beds)
            org.occupied_count = len(occupied)
            org.vacant_count = len(beds) - len(occupied)
