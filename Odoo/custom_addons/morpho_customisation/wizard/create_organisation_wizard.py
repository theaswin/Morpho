from odoo import models, fields, api

class CreateOrganisationWizard(models.TransientModel):
    _name = 'create.organisation.wizard'
    _description = 'Create Organisation Wizard'

    # Organisation Details
    name = fields.Char(string='Organisation Name', required=True)
    vat = fields.Char(string='VAT')
    location = fields.Char(string='Location')
    mobile = fields.Char(string='Mobile')

    # Owner Details
    owner_name = fields.Char(string='Owner Name', required=True)
    owner_email = fields.Char(string='Owner Email', required=True)
    owner_phone = fields.Char(string='Owner Phone')


    def action_confirm(self):
        self.ensure_one()

        Users = self.env['res.users'].sudo()
        Organisation = self.env['org.organisation'].sudo()

        # Check existing user
        user = Users.search([('login', '=', self.owner_email)], limit=1)

        if not user:
            user = Users.create({
                'name': self.owner_name,
                'login': self.owner_email,
                'email': self.owner_email,
                'phone': self.owner_phone,
                'password': '123',
            })
        else:
            if self.owner_phone and not user.phone:
                user.write({
                    'phone': self.owner_phone
                })

        # Create organisation
        org = Organisation.create({
            'name': self.name,
            'vat': self.vat,
            'location': self.location,
            'mobile': self.mobile,
            'owner_id': user.partner_id.id,
        })

        # Link organisation to partner
        user.partner_id.sudo().write({
            'organisation_ids': [(4, org.id)]
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Organisation',
            'res_model': 'org.organisation',
            'res_id': org.id,
            'view_mode': 'form',
            'target': 'current',
        }