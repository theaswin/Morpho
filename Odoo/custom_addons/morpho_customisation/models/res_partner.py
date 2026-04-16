from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    organisation_ids = fields.Many2many('org.organisation', string='Organisations', default=lambda self: self.env.user.organisation_ids.ids)
    date_of_joining = fields.Date(string='Date of Joining', default=fields.Date.context_today)
    monthly_fee = fields.Float(string='Monthly Fee')
    additional_cost = fields.Float(string='Additional Cost')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)

    @api.depends('monthly_fee', 'additional_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.monthly_fee + record.additional_cost

class ResUsers(models.Model):
    _inherit = 'res.users'

    organisation_ids = fields.Many2many('org.organisation', related='partner_id.organisation_ids', readonly=False, string='Organisations', default=lambda self: self.env.user.organisation_ids.ids)
