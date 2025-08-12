from odoo import fields,models,_,api

class MorphoWeb(models.Model):
    _name = 'morpho.backend'
    _description = "Morpho Backend"

    # Morpho Fields
    name = fields.Char(string="Name")
    website = fields.Char(string="URL")
    organisation_id = fields.Many2one('client.organisation',string="Organisation",default=lambda self: self.env.user.organisation_id)
    status = fields.Selection([('draft','Draft'),('in_progress','In Progress'),
                               ('archived','Archived'),('live','Live')])
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
    image_sections_ids = fields.One2many('image.sections','morpho_backend_id',string="Sections")


    def test(self):
        print("executing======================")
        print("Colum Type === ",self.env )


class NormalSections(models.Model):
    _name='morpho.sections'

    morpho_backend_id = fields.Many2one('morpho.backend',string="Backend")

    title = fields.Char(string="Title")
    image = fields.Binary(string="Image")
    text = fields.Text(string="Text")
    color = fields.Char(string="Color")


class ImageSections(models.Model):
    _name='image.sections'

    morpho_backend_id = fields.Many2one('morpho.backend',string="Backend")

    title = fields.Char(string="Title")
    image_ids = fields.Many2many('ir.attachment','image_sec_rel','img_sec_id','attach_id',string="Images")
    color = fields.Char(string="Color")
