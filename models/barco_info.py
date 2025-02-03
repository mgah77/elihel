from odoo import models, fields

class BarcoInfo(models.Model):
    _name = 'elihel.barco_info'
    _description = 'Información del Barco'

    nombre = fields.Char(string='Nombre del Barco', required=True)  # Nombre del barco
    matricula = fields.Char(string='Matrícula del Barco', required=True)  # Matrícula del barco
    valor = fields.Float(string='Valor del Barco', required=True)  # Valor del barco