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
         'views/menu.xml',
         'views/elihel_trabajo.xml',
         'data/servicios_data.xml',
         
],


'depends': ['base' , 'contacts' , 'stock' , 'product'],
'installable': True,
'application': True,
}
