{
    'name': 'Morpho',
    'version': '18.0.0.0',
    'summary': 'Morpho is a modern, flexible, and intuitive Content '
    'Management System designed to help you create, manage, and publish '
    'content effortlessly. With a sleek interface and adaptable architecture, '
    'Morpho empowers creators, businesses, and developers to build dynamic digital '
    'experiences without limits.',
    'description': """Morpho takes inspiration from transformation and adaptability—just like 
    its namesake, the morpho butterfly. Built for speed, scalability, and simplicity, it offers 
    an elegant content editing experience, robust security, and powerful customization options. 
    Whether you’re running a personal blog, a business website, or a complex web application, 
    Morpho adapts to your vision. Its modular design allows developers to extend functionality 
    easily, while its clean, responsive interface ensures content creators can focus on storytelling, 
    not technical hurdles. With Morpho, your content isn’t just managed—it evolves.
    .
                """,
    'category':'Web',
    'icon': "/morpho_customisation/static/src/image/logo.png",    
    'author': 'Aswin Nath',
    'website': 'https://theaswin.github.io/personal_website/',
    'license': "LGPL-3",
    'depends': ['base','contacts','crm','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/morpho_backend_view.xml',
        'views/organisation_view.xml',
        'views/payment_providers_view.xml',
        'views/payment_configurations_view.xml',
        'views/sections_view.xml',
        'views/all_sections_list_view.xml',
        'views/res_partner_view.xml',
        'views/res_users_view.xml',
        'views/crm_view.xml',
        'views/menu_view.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
