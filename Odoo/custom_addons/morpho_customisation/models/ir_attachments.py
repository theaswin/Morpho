from odoo import fields,models,_,api

class IrAttachments(models.Model):
    _inherit = 'ir.attachment'

    organisation_id = fields.Many2one('res.partner',string="Organisation",default=lambda self: self.env.user.organisation_id)

