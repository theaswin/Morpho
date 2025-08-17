from odoo import fields,models,_,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    org_id = fields.Many2one('client.organisation',string="Organisation",default=lambda self: self.env.user.organisation_id)
