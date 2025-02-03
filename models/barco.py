from odoo import models, fields

class Barco(models.Model):
    _name = 'elihel.barco'
    _description = 'Barco'

    name = fields.Char(string='Matrícula', required=True)  # Matrícula del barco
    valor = fields.Float(string='Valor')  # Valor asociado al barco
    fecha_llegada = fields.Datetime(string='Fecha de Llegada', default=fields.Datetime.now)  # Fecha de llegada
    camion_ids = fields.One2many('elihel.camion', 'barco_id', string='Camiones')  # Camiones asociados al barco