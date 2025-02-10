from odoo import models, fields, api
from datetime import datetime

class WizardTrabajos(models.TransientModel):
    _name = 'elihel.wizard_trabajos'
    _description = 'Wizard para filtrar trabajos por lugar, mes y año'

    lugar = fields.Selection([
        ('pue', 'Puerto Montt'),
        ('cco', 'Chacabuco'),
    ], string='Lugar', required=True)  # Lugar de trabajo

    mes = fields.Selection([
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ], string='Mes', required=True)  # Mes del trabajo

    anno = fields.Integer(
        string='Año',
        default=lambda self: datetime.now().year,  # Año actual por defecto
        required=True,
    )  # Año del trabajo

    resultado_ids = fields.One2many(
        'elihel.wizard_trabajos.resultado',  # Modelo relacionado
        'wizard_id',  # Campo Many2one en el modelo relacionado
        string='Resultados',  # Etiqueta del campo
    )  # Lista de resultados

    @api.onchange('lugar', 'mes', 'anno')
    def _onchange_lugar_mes_anno(self):
        # Limpiar resultados anteriores
        self.resultado_ids = [(5, 0, 0)]  # Eliminar todos los registros existentes

        # Verificar si se han seleccionado lugar, mes y año
        if self.lugar and self.mes and self.anno:
            # Obtener la fecha actual
            fecha_actual = datetime.now()
            anno_actual = fecha_actual.year
            mes_actual = fecha_actual.month

            # Verificar que el año no sea futuro
            if self.anno > anno_actual:
                return {
                    'warning': {
                        'title': 'Año inválido',
                        'message': 'No se puede seleccionar un año futuro.',
                    }
                }

            # Verificar que el mes no sea futuro dentro del año actual
            if self.anno == anno_actual and int(self.mes) > mes_actual:
                return {
                    'warning': {
                        'title': 'Mes inválido',
                        'message': 'No se puede seleccionar un mes futuro dentro del año actual.',
                    }
                }

            # Filtrar los trabajos por lugar, mes y año
            trabajos = self.env['elihel.barco'].search([
                ('lugar', '=', self.lugar),
                ('fecha_llegada', '>=', f'{self.anno}-{self.mes}-01'),
                ('fecha_llegada', '<=', f'{self.anno}-{self.mes}-31'),
            ])

            # Crear registros en el modelo transitorio para mostrar los resultados
            for trabajo in trabajos:
                for camion in trabajo.camion_ids:
                    servicios = ", ".join([
                        f"{servicio.tipo_servicio} ({servicio.cantidad})"
                        for servicio in camion.servicio_ids
                    ])
                    self.resultado_ids = [(0, 0, {
                        'numero_certificado': trabajo.numero_certificado,
                        'fecha_llegada': trabajo.fecha_llegada,
                        'matricula_camion': camion.matricula,
                        'servicios': servicios,
                    })]

class WizardTrabajosResultado(models.TransientModel):
    _name = 'elihel.wizard_trabajos.resultado'
    _description = 'Resultados del Wizard de Trabajos'

    wizard_id = fields.Many2one(
        'elihel.wizard_trabajos',  # Modelo relacionado
        string='Wizard',  # Etiqueta del campo
    )  # Relación con el wizard

    numero_certificado = fields.Char(string='Número de Certificado')  # Número de certificado
    fecha_llegada = fields.Date(string='Fecha de Llegada')  # Fecha de llegada
    matricula_camion = fields.Char(string='Matrícula del Camión')  # Matrícula del camión
    servicios = fields.Text(string='Servicios')  # Lista de servicios