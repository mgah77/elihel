from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Camion(models.Model):
    _name = 'elihel.camion'
    _description = 'Camión'

    matricula = fields.Char(string='Matrícula del Camión', required=True, size=6)  # Matrícula del camión (6 caracteres)
    barco_id = fields.Many2one('elihel.barco', string='Barco', ondelete='cascade')  # Relación con el barco
    servicio_ids = fields.One2many('elihel.servicio', 'camion_id', string='Servicios')  # Servicios asociados

    @api.constrains('matricula')
    def _check_matricula(self):
        for record in self:
            if len(record.matricula) != 6:
                raise ValidationError("La matrícula debe tener exactamente 6 caracteres.")
            # Convertir a mayúsculas
            record.matricula = record.matricula.upper()