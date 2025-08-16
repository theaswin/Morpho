from odoo import fields, models, _,api
from datetime import date, datetime
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
    validity_till = fields.Date(string="Validity Till")
    valid_days = fields.Integer(string="Days",compute="_compute_validity",store=False)
    status = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='active', compute="_compute_validity", store=False)

    @api.depends('validity_till')
    def _compute_validity(self):
        today = date.today()
        for rec in self:
            if rec.validity_till:
                validity_date = (
                    rec.validity_till.date() if isinstance(rec.validity_till, datetime)
                    else rec.validity_till
                )
                if not isinstance(validity_date, date):
                    validity_date = validity_date.date()

            days = (validity_date - today).days
            rec.valid_days = days
            if days > 15:
                rec.status = 'active'
            elif 1 <= days <= 15:
                rec.status = 'expiring'
            else:
                rec.status = 'expired'


    
    def action_cancel_org(self):
        for rec in self:
            rec.status = 'cancelled'

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