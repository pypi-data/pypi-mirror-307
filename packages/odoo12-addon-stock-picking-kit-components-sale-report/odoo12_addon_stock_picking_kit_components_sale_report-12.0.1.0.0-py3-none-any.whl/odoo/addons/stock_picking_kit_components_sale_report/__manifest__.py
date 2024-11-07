# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking Kit Components Sale Report',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'summary': 'Shows the main product and kit components in the stock picking reports.',
    'author': 'Sygel',
    'website': 'https://www.sygel.es',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock',
        'mrp'
    ],
    'data': [
        'views/report_picking.xml',
        'views/report_delivery_document.xml'
    ],
    'installable': True,
}
