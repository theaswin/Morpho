from odoo import fields,models,_,api

class ResUsers(models.Model):
    _inherit = 'res.users'

    organisation_id = fields.Many2one('client.organisation',string="Organisation")