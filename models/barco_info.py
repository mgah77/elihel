from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BarcoInfo(models.Model):
    _name = 'elihel.barco_info'
    _description = 'Información del Barco'
    _rec_name = 'nombre'  # Define el campo 'nombre' como el nombre predeterminado

    nombre = fields.Char(string='Nombre del Barco', required=True)  # Nombre del barco
    matricula = fields.Char(string='Matrícula del Barco', required=True, size=6)  # Matrícula del barco (6 caracteres)
    valor = fields.Float(string='Valor del Barco', required=True)  # Valor del barco

    @api.constrains('matricula')
    def _check_matricula(self):
        for record in self:
            if record.matricula and len(record.matricula) != 6:
                raise ValidationError("La matrícula debe tener exactamente 6 caracteres.")

    @api.onchange('matricula')
    def _onchange_matricula(self):
        if self.matricula:
            self.matricula = self.matricula.upper()