from odoo import fields,models,_,api

class PaymentLogs(models.Model):
    _name = 'pay.logs'
    _description = "Payment Logs"

    name = fields.Char(string="Name")
    payment_provider_id = fields.Many2one('pay.providers',string="Payment Provider")
    request = fields.Text(string="Request")
    responses = fields.Text(string="Responses")
    code = fields.Integer(string="Code")