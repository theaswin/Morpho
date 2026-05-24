from odoo import models, fields, api

class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _rec_name = 'room_number'

    room_number = fields.Char(string='Room Number', required=True)
    organisation_id = fields.Many2one('org.organisation', string='Organisation', required=True, ondelete='cascade')
    bed_ids = fields.One2many('hostel.bed', 'room_id', string='Beds')
    vacancy_count = fields.Integer(string='Vacancy', compute='_compute_vacancy')

    @api.depends('bed_ids.partner_id')
    def _compute_vacancy(self):
        for record in self:
            record.vacancy_count = len(record.bed_ids.filtered(lambda b: not b.partner_id))
