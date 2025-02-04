from odoo import models, fields

class Servicio(models.Model):
    _name = 'elihel.servicio'
    _description = 'Servicio'
    _rec_name = 'tipo_servicio'  # Define el campo 'tipo_servicio' como el nombre predeterminado

    tipo_servicio = fields.Selection([
        ('desinfeccion', 'Desinfección'),
        ('reffers', 'Reffers'),
        ('bins', 'Bins'),
    ], string='Tipo de Servicio', required=True)  # Tipo de servicio
    cantidad = fields.Integer(string='Cantidad', required=True)  # Cantidad del servicio
    camion_id = fields.Many2one('elihel.camion', string='Camión', ondelete='cascade')  # Relación con el camión