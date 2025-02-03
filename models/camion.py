from odoo import models, fields

class Camion(models.Model):
    _name = 'elihel.camion'
    _description = 'Camión'

    matricula = fields.Char(string='Matrícula', required=True)  # Matrícula del camión
    barco_id = fields.Many2one('elihel.barco', string='Barco', ondelete='cascade')  # Relación con el barco
    servicio_ids = fields.One2many('elihel.servicio', 'camion_id', string='Servicios')  # Servicios asociados