from odoo import fields,models,_,api

class PaymentProviders(models.Model):
    _name = 'pay.providers'
    _description = "Payment Providers"

    image =fields.Binary(string="Image")
    name=fields.Char(string="Name")
    availability =fields.Boolean(string="Availability")

    def action_view_credentials(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.conf',
            'name':"Credentials",
            'view_mode': 'list,form',
            'domain': [('organisation_id', '=', self.id)],
            'context': {'default_organisation_id': self.id},
            'context': {
                'create': False,
                'edit': False,
                'delete': False,
            },

        }

    def action_view_logs(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.logs',
            'name':"Logs",
            'view_mode': 'list,form',
            'domain': [('organisation_id', '=', self.id)],
            'context': {'default_organisation_id': self.id},
        }



    