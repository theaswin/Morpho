from odoo import http
from odoo.http import request


class MorphoWeb(http.Controller):

    @http.route('/morpho/test_call', type='json', auth='public', methods=['POST'], csrf=False)
    def test_call(self, **kwargs):
        data = kwargs.get('testing'),
        return data

    @http.route('/morpho/fetch_hostels', type='json', auth='public', methods=['POST'], csrf=False)
    def fetch_hostels(self, **kwargs):
        print("Called hostels api =======================")
        output = []
        data =  request.env['org.organisation'].sudo().search([])
        for record in data:
            beds = record.room_ids.mapped('bed_ids')
            prices = [bed.price for bed in beds if bed.price is not None]
            rent_range = [min(prices), max(prices)] if prices else [0, 0]
            output.append({
                'id': record.id,
                'name': record.name,
                'logo': record.logo,
                'status':'testing',
                'ratings': 1.5,
                'desc':'A practical hostel block close to transport, labs, and evening dining.',
                'tags':['my test','jj','.5 review'],
                'vacant': record.vacant_count,
                'occupied': record.occupied_count,
                'rooms': record.total_rooms,
                'rent_range': rent_range
            })
        return output
    
    @http.route('/morpho/fetch_rooms', type='json', auth='public', methods=['POST'], csrf=False)
    def fetch_rooms(self, **kwargs):
        print("Called rooms api =======================")
        output = []
        params = kwargs.get('params') or kwargs
        hostel_id = params.get('hostel_id')
        if isinstance(hostel_id, (list, tuple)):
            hostel_id = hostel_id[0]

        if hostel_id:
            rooms = request.env['hostel.room'].sudo().search([('organisation_id', '=', hostel_id)])
            for room in rooms:
                output.append({
                    'id': room.id,
                    'room_number': room.room_number,
                    'vacancy': room.vacancy_count,
                    'beds': [{'id': bed.id, 'bed_number': getattr(bed, 'bed_number', None) or str(bed.id), 'price': bed.price, 'status': 'occupied' if bed.partner_id else 'vacant'} for bed in room.bed_ids]
                })

        return output

    @http.route('/morpho/fetch_beds', type='json', auth='public', methods=['POST'], csrf=False)
    def fetch_beds(self, **kwargs):
        print('Called Beds api =======================')
        output = []
        params = kwargs.get('params') or kwargs
        hostel_id = params.get('hostel_id')
        room_id = params.get('room_id')
        if isinstance(hostel_id, (list, tuple)):
            hostel_id = hostel_id[0]
        if isinstance(room_id, (list, tuple)):
            room_id = room_id[0]

        if hostel_id and room_id:
            beds = request.env['hostel.bed'].sudo().search([('organisation_id', '=', hostel_id),
                                                            ('room_id', '=', room_id)])
            for bed in beds:
                output.append({
                    'id': bed.id,
                    'room_id': bed.room_id.id,
                    'bed_number': getattr(bed, 'bed_number', None) or str(bed.id),
                    'status': 'occupied' if bed.partner_id else 'vacant',
                    'price': bed.price,
                    'enquiry_mobile': bed.organisation_id.mobile if bed.organisation_id else None,
                    'enquiry_message': bed.organisation_id.default_message if bed.organisation_id else None,
                })

        return output                       
