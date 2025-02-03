from odoo import models, fields

class Servicio(models.Model):
    _name = 'elihel.servicio'
    _description = 'Servicio'

    # Campo Selection para el tipo de servicio
    tipo_servicio = fields.Selection([
        ('desinfeccion', 'Desinfección'),
        ('reffers', 'Reffers'),
        ('bins', 'Bins'),
    ], string='Tipo de Servicio', required=True)

    cantidad = fields.Integer(string='Cantidad', required=True)  # Cantidad del servicio
    camion_id = fields.Many2one('elihel.camion', string='Camión', ondelete='cascade')  # Relación con el camión