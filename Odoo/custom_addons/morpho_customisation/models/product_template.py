from odoo import fields,models,_,api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    org_id = fields.Many2one('res.partner',string="Organisation",default=lambda self: self.env.user.organisation_id)
