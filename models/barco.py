from odoo import models, fields

class Barco(models.Model):
    _name = 'elihel.barco'
    _description = 'Barco'

    barco_info_id = fields.Many2one('elihel.barco_info', string='Información del Barco', required=True)  # Relación con BarcoInfo
    fecha_llegada = fields.Datetime(string='Fecha de Llegada', default=fields.Datetime.now)  # Fecha de llegada
    camion_ids = fields.One2many('elihel.camion', 'barco_id', string='Camiones')  # Camiones asociados

    # Campos relacionados (para mostrar en vistas)
    nombre = fields.Char(related='barco_info_id.nombre', string='Nombre', readonly=True)  # Nombre del barco
    matricula = fields.Char(related='barco_info_id.matricula', string='Matrícula', readonly=True)  # Matrícula del barco
    valor = fields.Float(related='barco_info_id.valor', string='Valor', readonly=True)  # Valor del barco