from odoo import fields,models,_,api

class CRM(models.Model):
    _inherit = 'crm.lead'


    support_name = fields.Char(string="Support Name")
    support_title_id = fields.Many2one('res.partner.title',string="Support Title")
    support_job_position = fields.Char(string="Job Position")
    support_mobile = fields.Char(string="Support Mobile")