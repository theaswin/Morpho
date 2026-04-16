{
    'name': 'Hostel Management',
    'version': '1.0',
    'category': 'Industry',
    'summary': 'Manage hostels, rooms, and beds',
    'description': """
Hostel Management System
========================
- Manage Organizations
- Manage Rooms and Beds
- Multi-tenant data separation
    """,
    'depends': ['base', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/organisation_views.xml',
        'views/room_views.xml',
        'views/bed_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
