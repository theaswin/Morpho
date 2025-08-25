from odoo import fields,models,_,api

class Sections(models.Model):
    _name = 'section.sections'
    _description = "Sections"

    organisation_id = fields.Many2one('res.partner',string="Organisation")
    name = fields.Char(string="Name")
    code = fields.Html(string="Code")