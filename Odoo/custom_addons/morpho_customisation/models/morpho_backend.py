from odoo import fields,models,_,api

class MorphoWeb(models.Model):
    _name = 'morpho.backend'
    _description = "Morpho Backend"

    name = fields.Char(string="Name")
    website = fields.Char(string="URL")
    organisation_id = fields.Many2one('client.organisation',string="Organisation")

    # Banner Section
    header_image = fields.Binary(string="Banner Image")
    header_align = fields.Selection([('full','Full'),('top','Top'),
                                    ('left','Left'),('right','Right')],string="Banner Type")
    head_content = fields.Text(string="Banner Content")
    head_content_align = fields.Selection([('full','Full'),('top','Top'),
                                    ('left','Left'),('right','Right')],string="Banner Type")
    head_html = fields.Html(string="Head Html")
    
    # Footer Section

    f_image = fields.Binary(string="Footer Image")
    f_html1 = fields.Html(string="Content 1")
    f_html2 = fields.Html(string="Content 2")
    f_html3 = fields.Html(string="Content 3")
    
    sections_ids = fields.One2many('morpho.sections','morpho_backend_id',string="Sections")


class Sections(models.Model):
    _name='morpho.sections'

    morpho_backend_id = fields.Many2one('morpho.backend',string="Backend")