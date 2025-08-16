from odoo import fields,models,_,api
from lxml import etree

class MorphoWeb(models.Model):
    _name = 'morpho.backend'
    _description = "Morpho Backend"

    # Morpho Fields
    name = fields.Char(string="Name")
    website = fields.Char(string="URL")
    organisation_id = fields.Many2one('client.organisation',string="Organisation",default=lambda self: self.env.user.organisation_id)
    status = fields.Selection([('draft','Draft'),('in_progress','In Progress'),
                               ('archived','Archived'),('live','Live')],default='draft')
    is_generated = fields.Boolean(string="Website Generated")
    
    # Banner Section
    header_image = fields.Binary(string="Banner Image")
    header_align = fields.Selection([('full','Full'),('top','Top'),
                                    ('left','Left'),('right','Right')],string="Banner Type")
    head_content = fields.Text(string="Banner Content")
    head_content_align = fields.Selection([('full','Full'),('top','Top'),
                                    ('left','Left'),('right','Right')],string="Banner Align")
    head_html = fields.Html(string="Head Html")
    
    # Footer Section

    f_image = fields.Binary(string="Footer Image")
    f_html1 = fields.Html(string="Content 1")
    f_html2 = fields.Html(string="Content 2")
    f_html3 = fields.Html(string="Content 3")
    
    general_sections_ids = fields.One2many('morpho.general.sections','morpho_backend_id',string="Sections")
    def create_refresh(self):
        pass

    def action_set_live(self):
        for rec in self:
            rec.status = 'live'

    def action_set_inprogress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_set_archived(self):
        for rec in self:
            rec.status = 'archived'
    
    def action_view_all_sections(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'morpho.general.sections',
            'name': "Sections",
            'view_mode': 'list',
            'view_id': self.env.ref('morpho_customisation.view_morpho_general_sections_list').id,
            'domain': [('morpho_backend_id', '=', self.id)],
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
            },
        }





class MorphoGeneralSections(models.Model):
    _name='morpho.general.sections'
    _description = "General Sections"

    morpho_backend_id = fields.Many2one('morpho.backend',string="Backend")

    sequence = fields.Integer(string="Sequence")
    section_id = fields.Many2one('section.sections',string="Type")
    title = fields.Char(string="Title")
    description = fields.Text(string="Descriptions")
    design = fields.Html(string="Design")
    image_ids = fields.Many2many('ir.attachment','image_sec_rel','img_sec_id','attach_id',string="Images")
    color = fields.Char(string="Color")
    
