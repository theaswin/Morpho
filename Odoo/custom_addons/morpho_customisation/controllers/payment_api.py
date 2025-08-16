from odoo import http
from odoo.http import request
import re
import razorpay


class webController(http.Controller):

    # Razorpay
    @http.route(['/get/generate_order_id/'], type='json', auth='public', methods=['POST'], csrf=False, cors="*")
    def get_rzp_order_id(self,**post):        
        conf = request.env['api.pay.conf'].search([('payment_mode','=','razor_pay')])
        
        YOUR_KEY_ID = conf.key_id
        YOUR_KEY_SECRET = conf.key_secret
        client = razorpay.Client(auth=(YOUR_KEY_ID, YOUR_KEY_SECRET))
        customer_date = post['customer_data']
        ticket_data = post['ticket_data']
        untaxed_amount = ticket_data.get('untax_amount',0)
        tax = ticket_data.get('tax',0)
        print(untaxed_amount,tax)
        if tax>0:
            amount_paisa = float(untaxed_amount)*100
            tax_amount = float(amount_paisa)*(tax/100)
            amount_total = amount_paisa + tax_amount

        else:
            amount_paisa = float(untaxed_amount)*100
            tax_amount = float(amount_paisa)*(18.0/100)
            amount_total = amount_paisa + tax_amount

        order_data = {
            "amount":  amount_total,  
            "currency": ticket_data.get('currency',"INR"),
            "receipt": ticket_data.get('receipt',None),  
            "payment_capture": 1,
            "payment_capture": ticket_data.get('payment_capture',False),
            "notes": {
                "customer_name": customer_date.get('customer_name',False),
                "customer_email": customer_date.get('customer_email',False),
                "customer_phone": customer_date.get('customer_phone',False),
                "customer_id": customer_date.get('customer_id',False)
            }
        }
        order = client.order.create(data=order_data)
        if order:
            
            log_calls(name="Get Order ID",status=200,data=post.copy(),response=order)
            log_cms_table(first_name=customer_date.get('firstname'),last_name=customer_date.get('lastname'),email = customer_date.get('email'),
                          mobile_number=customer_date.get('phone'),mode=customer_date.get('mode',False),
                          order_id = order["id"],amount=ticket_data.get('untax_amount'),ticket_count = ticket_data.get('ticket_count'),
                          website = customer_date.get('website'),flag=False,payload = post.copy())
            return {
                "code":200,
                "order_id":order["id"],
                "text":"Order Successfully Created In Razor Pay"
            } 
        else:
            log_calls(name="Get Order ID",status=404,data=post.copy(),response=order)
            log_cms_table(first_name=customer_date.get('firstname'),last_name=customer_date.get('lastname'),email = customer_date.get('email'),
                          mobile_number=customer_date.get('phone'),mode=customer_date.get('mode',False),order_id = order.get("id",False),amount=ticket_data.get('untax_amount'),ticket_count = ticket_data.get('ticket_count'),
                          website = customer_date.get('website'),payload = post.copy())

            return{
                "code":404,
                "order_id":'None',
                "text":"Order Failed Create In Razor Pay"

            }
