from odoo import fields, models, _

class Organisation(models.Model):
    _name = 'client.organisation'
    _description = 'Organisation'
    _rec_name = 'name'

    name = fields.Char(string="Organisation")
    image_1920 = fields.Image(string="Logo / Image", max_width=1920, max_height=1920)
    owner_id = fields.Many2one('res.partner',string="Owner")
    support_id = fields.Many2one('res.partner',string="Support")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    vat = fields.Char(string="Tax ID")
    company_type = fields.Selection([
        ('company', 'Company'),
        ('individual', 'Individual'),
    ], string="Company Type", default='company')
    
    description = fields.Text(string="Description / Notes")
    validity_till = fields.Datetime(string="Validity Till")
    status = fields.Selection([('in_progress','In Progress'),('active','Active'),('expiring','Expiring'),
                               ('expaired','Expired'),('cancelled','Cancelled')])
    


    def action_view_websites(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'morpho.backend',
            'name':"Websites",
            'view_mode': 'list,form',
            'domain': [('organisation_id', '=', self.id)],
            'context': {'default_organisation_id': self.id},
        }
    
    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.logs',
            'name':"Payments",
            'view_mode': 'list,form',
            'domain': [('organisation_id', '=', self.id)],
            'context': {'default_organisation_id': self.id},
        }


    def action_view_logs(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.logs',
            'name':"Payment Logs",
            'view_mode': 'list,form',
            'domain': [('organisation_id', '=', self.id)],
            'context': {'default_organisation_id': self.id},
        }

    def action_view_providers(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.providers',
            'name':"Payment Providers",
            'view_mode': 'kanban,form',
            'context': {},
        }