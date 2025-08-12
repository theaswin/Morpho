from odoo import fields,models,_,api

class PaymentProviders(models.Model):
    _name = 'pay.providers'
    _description = "Payment Providers"

    name=fields.Char(string="Name")
    availability =fields.Boolean(string="Availability")

    