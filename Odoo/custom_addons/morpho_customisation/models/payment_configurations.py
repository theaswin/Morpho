from odoo import fields,models,_,api

class PaymentConfigurations(models.Model):
    _name = 'pay.conf'
    _description = "Payment Configurations"
    _rec_name="payment_provider_id"

    payment_provider_id = fields.Many2one('pay.providers',string="Payment Provider")
    organisation_id = fields.Many2one('client.organisation',string="Organisation")
    key_id = fields.Char(string="Key ID")
    key_secret = fields.Char(string="Key Secret")

    # api
    conf_api_1 = fields.Char(string="API 1")
    conf_api_2 = fields.Char(string="API 2")
    conf_api_3 = fields.Char(string="API 3")
    conf_api_4 = fields.Char(string="API 4")