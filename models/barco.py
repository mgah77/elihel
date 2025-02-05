from odoo import models, fields

class Barco(models.Model):
    _name = 'elihel.barco'
    _description = 'Barco'
    _rec_name = 'nombre'  # Define el campo 'nombre' como el nombre predeterminado

    barco_info_id = fields.Many2one('elihel.barco_info', string='Información del Barco', required=True)  # Relación con BarcoInfo
    fecha_llegada = fields.Datetime(string='Fecha', default=fields.Datetime.now)  # Fecha
    camion_ids = fields.One2many('elihel.camion', 'barco_id', string='Camiones')  # Camiones asociados
    lugar = fields.Selection([
        ('pue', 'Puerto Montt'),
        ('cco', 'Chacabuco'),
    ], string='Lugar', required=True)  # Lugar de trabajo      

    # Campos relacionados (para mostrar en vistas)
    nombre = fields.Char(related='barco_info_id.nombre', string='Nombre', readonly=True)  # Nombre del barco
    matricula = fields.Char(related='barco_info_id.matricula', string='Matrícula', readonly=True)  # Matrícula del barco
    valor = fields.Float(related='barco_info_id.valor', string='Valor', readonly=True)  # Valor del barco