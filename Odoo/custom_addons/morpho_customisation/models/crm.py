from odoo import fields,models,_,api

from odoo.exceptions import UserError

class CRM(models.Model):
    _inherit = 'crm.lead'


    support_name = fields.Char(string="Support Name")
    support_title_id = fields.Many2one('res.partner.title',string="Support Title")
    support_job_position = fields.Char(string="Job Designation")
    support_mobile = fields.Char(string="Support Mobile")
    support_login = fields.Char(string="Email")
    owner_login = fields.Char(string="Email")
    done =fields.Boolean(string="Done")




    def action_initialise(self):
        """Initialise and create related users & partner"""
        company_model = 'res.partner'
        user_model = 'res.users'

        # Check mandatory fields
        if not self.partner_name:
            raise UserError("Please provide a Partner Name before initialization.")
        if not self.contact_name:
            raise UserError("Please provide a Contact Name before initialization.")
        if not self.support_name:
            raise UserError("Please provide a Support Contact Name before initialization.")

        cmp = self.env[company_model].sudo().create({
            'name': self.partner_name or "Unnamed Company",
            'street': self.street or False,
            'street2': self.street2 or False,
            'city': self.city or False,
            'state_id': self.state_id.id if self.state_id else False,
            'country_id':self.country_id.id,
            'zip': self.zip or False,
            'website': self.website or False,
            'is_company': True,
        })

        # Create Main Contact User
        self.env[user_model].sudo().create({
            'name': self.contact_name,
            'function': self.function or False,
            'title': self.title.id if self.title else False,
            'mobile': self.mobile or False,
            'login': self.owner_login,   # Must be unique
            'password':'111',
            'organisation_id':cmp.id
        })

        # Create Support Contact User
        self.env[user_model].sudo().create({
            'name': self.support_name,
            'function': self.support_job_position or False,
            'title': self.support_title_id.id if self.support_title_id else False,
            'mobile': self.support_mobile or False,
            'login': self.support_login,   # Must be unique
            'password':'111',
            'organisation_id':cmp.id
        })

        # Create Company Partner

        # Mark initialization complete
        self.done = True
