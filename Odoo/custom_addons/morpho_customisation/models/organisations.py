from odoo import fields, models, _

class Organisation(models.Model):
    _name = 'client.organisation'
    _description = 'Organisation'
    _rec_name = 'name'

    name = fields.Char(string="Organisation")
    image_1920 = fields.Image(string="Logo / Image", max_width=1920, max_height=1920)
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
