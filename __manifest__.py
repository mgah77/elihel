# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{ 'name': 'Elihel',
'summary': "Trabajos",
'author': "Mauricio Gah",
'license': "AGPL-3",
'application': "True",
'version': "2.0",
'data': ['security/groups.xml',
         'security/ir.model.access.csv',
         'data/sequences.xml',                   
         'views/barco_info_views.xml',
         'views/barco_views.xml',
         'views/camion_views.xml',
         'views/servicio_views.xml',
        
],


'depends': ['base' , 'contacts' , 'stock' , 'product'],
'installable': True,
'application': True,
}
