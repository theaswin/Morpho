from odoo import fields,models,_,api
from datetime import date, datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    organisation_id = fields.Many2one('res.partner',string="Organisation",default=lambda self: self.env.user.organisation_id)
    validity_till = fields.Date(string="Validity Till")
    valid_days = fields.Integer(string="Days",compute="_compute_validity",store=False)
    status = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], string="Current Status", default='active', compute="_compute_validity", store=False)
    owner_id = fields.Many2one('res.users',string="Owner")
    support_id = fields.Many2one('res.users',string="Associated User")
    organisation_id = fields.Many2one('res.partner',string="Organisation")

    @api.depends('validity_till')
    def _compute_validity(self):
        today = date.today()
        for rec in self:
            if rec.validity_till:
                # Handle datetime or date safely
                validity_date = (
                    rec.validity_till.date() if isinstance(rec.validity_till, datetime)
                    else rec.validity_till
                )

                # Always compute days difference
                days = (validity_date - today).days
                rec.valid_days = days

                if days > 15:
                    rec.status = 'active'
                elif 1 <= days <= 15:
                    rec.status = 'expiring'
                else:
                    rec.status = 'expired'
            else:
                rec.valid_days = 0
                rec.status = False
                


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