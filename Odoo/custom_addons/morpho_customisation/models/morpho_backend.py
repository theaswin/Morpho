from odoo import fields,models,_,api

class MorphoWeb(models.Model):
    _name = 'morpho.backend'

    name = fields.Char(string="Name")
    website = fields.Char(string="URL")