from odoo import fields,models,_,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    organisation_id = fields.Many2one('client.organisation',string="Organisation",default=lambda self: self.env.user.organisation_id)