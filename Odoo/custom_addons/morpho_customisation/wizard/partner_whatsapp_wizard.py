from odoo import models, fields, api
import html

class PartnerWhatsappWizard(models.TransientModel):
    _name = 'partner.whatsapp.wizard'
    _description = 'WhatsApp Notification Wizard'

    partner_id = fields.Many2one('res.partner', string='Resident', required=True)
    mobile = fields.Char(string='Mobile Number', required=True)
    message = fields.Text(string='Message', required=True)

    @api.model
    def default_get(self, fields):
        res = super(PartnerWhatsappWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            partner = self.env['res.partner'].browse(active_id)
            res.update({
                'partner_id': partner.id,
                'mobile': partner.phone,
                'message': f"Hello {partner.name}, this is a reminder regarding your pending fees for {partner.organisation_ids[0].name if partner.organisation_ids else 'the hostel'}. Please settle the amount of {partner.total_cost} at your earliest convenience. Thank you!"
            })
        return res

    def action_send_whatsapp(self):
        self.ensure_one()
        if not self.mobile:
            raise models.ValidationError("Mobile number is required to send WhatsApp message.")
        
        # Clean mobile number: remove non-numeric characters except +
        mobile = ''.join(c for c in self.mobile if c.isdigit() or c == '+')
        if not mobile.startswith('+'):
            # Assume local number if no country code, might need adjustment based on region
            # For now, just use as is or prepend a default if known. 
            # I'll keep it simple and just use the cleaned number.
            pass
            
        message = self.message
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        url = f"https://web.whatsapp.com/send?phone={mobile}&text={encoded_message}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'whatsapp_web',
        }
