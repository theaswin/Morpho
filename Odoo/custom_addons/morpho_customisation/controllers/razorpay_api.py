from odoo import http
from odoo.http import request
import re
import razorpay
import requests
from requests.auth import HTTPBasicAuth

def format_url(raw_url):
    match = re.search(r'^.*?\.com', raw_url)
    if match:
        format_url = match.group()
        return format_url
    else:
        return "Invalid URL"
    
class webController(http.Controller):

    # Razorpay
    @http.route(['/get/generate_order_id/'], type='json', auth='public', methods=['GET'], csrf=False, cors="*")
    def get_rzp_order_id(self,**post):
        web_url = post.get('web_url')
        backend = request.env['morpho.backend'].sudo().search([('website','=',format_url(web_url))])
        org_id = backend.organisation_id.id
        credentials = request.env['pay.conf'].sudo().search([
            ('id','=',org_id),('payment_provider_id.name','=','Razor Pay')
            ])
        
        YOUR_KEY_ID = credentials.key_id
        YOUR_KEY_SECRET = credentials.key_secret

        client = razorpay.Client(auth=(YOUR_KEY_ID, YOUR_KEY_SECRET))
        customer_data = post['customer_data']
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
                "customer_name": customer_data.get('customer_name',False),
                "customer_email": customer_data.get('customer_email',False),
                "customer_phone": customer_data.get('customer_phone',False),
                "customer_id": customer_data.get('customer_id',False)
            }
        }
        order = client.order.create(data=order_data)
        if order:
            return {
                "code":200,
                "order_id":order["id"],
                "text":"Order Successfully Created In Razor Pay"
            } 
        else:
            return{
                "code":404,
                "order_id":'None',
                "text":"Order Failed Create In Razor Pay"

            }

    @http.route(['/post/complete_payment/'], type='json', auth='public', methods=['POST'], csrf=False, cors="*")
    def verity_rzp_pay_id(self,**post):

        web_url = post.get('web_url')
        backend = request.env['morpho.backend'].sudo().search([('website','=',format_url(web_url))])
        org_id = backend.organisation_id.id
        credentials = request.env['pay.conf'].sudo().search([
            ('id','=',org_id),('payment_provider_id.name','=','Razor Pay')
            ])

        key_id = credentials.key_id
        key_secret = credentials.key_secret
        order_api = credentials.conf_api_1
        payment_api = credentials.conf_api_2

        
        

        razor_pay_id =  post.get('razorpay_payment_id',False) 
        razor_ord_id   = post.get('razorpay_order_id',False)
        razor_signature   = post.get('razorpay_signature',False)
        amount_paisa   = post.get('amount',False)

        order_api_url = f"{order_api}/{razor_ord_id}"
        order_response = requests.get(order_api_url, auth=HTTPBasicAuth(key_id, key_secret))
        order_datas = order_response.json()



        # signature verification
        client = razorpay.Client(auth=(key_id, key_secret))
        params_dict = {
            "razorpay_order_id": razor_ord_id,
            "razorpay_payment_id": razor_pay_id,
            "razorpay_signature": razor_signature
        }
        try:
            validation = client.utility.verify_payment_signature(params_dict)
            signature_status = 'valid'
            try:
                captured_payment = client.payment.capture(razor_pay_id, amount_paisa)
                print("Payment Captured:", captured_payment)
            except Exception as e:
                return("Error capturing payment:", str(e))
        except razorpay.errors.SignatureVerificationError:
            validation = False
            signature_status = 'invalid'

        payment_api_url = f"{payment_api}/{razor_pay_id}"
        payment_response = requests.get(payment_api_url, auth=HTTPBasicAuth(key_id, key_secret))
        payment_data = payment_response.json()

        if validation == True:
            return{
                "code":200,
                "note":f"Order ID [{razor_ord_id} , {order_datas.get('status')}] , Payment ID [{razor_pay_id} , {payment_data.get('status')}]",
                "signature_verification":validation
            }
        else: 
            return{
                "code":400,
                "note":f"Failed to Validate PaymentID {razor_pay_id},Order ID {razor_ord_id},Signature {razor_signature}",
                "signature_verification":validation
            }

