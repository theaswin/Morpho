from odoo import models, fields

class HostelBed(models.Model):
    _name = 'hostel.bed'
    _description = 'Hostel Bed'
    _rec_name = 'partner_id'

    room_id = fields.Many2one('hostel.room', string='Room', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Resident')
    partner_street = fields.Char(related='partner_id.street', string='Street')
    partner_city = fields.Char(related='partner_id.city', string='City')
    partner_image = fields.Binary(related='partner_id.image_128', string='Resident Image')
    organisation_id = fields.Many2one('org.organisation', related='room_id.organisation_id', store=True, string='Organisation')
