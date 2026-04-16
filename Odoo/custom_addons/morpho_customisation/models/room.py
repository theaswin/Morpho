from odoo import models, fields

class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _rec_name = 'room_number'

    room_number = fields.Char(string='Room Number', required=True)
    organisation_id = fields.Many2one('org.organisation', string='Organisation', required=True, ondelete='cascade')
    bed_ids = fields.One2many('hostel.bed', 'room_id', string='Beds')
