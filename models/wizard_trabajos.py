from odoo import models, fields, api
from datetime import datetime
import calendar

class WizardTrabajos(models.TransientModel):
    _name = 'elihel.wizard_trabajos'
    _description = 'Wizard para filtrar trabajos por lugar, mes y año'

    lugar = fields.Selection([
        ('pue', 'Puerto Montt'),
        ('cco', 'Chacabuco'),
    ], string='Lugar', required=True)

    mes = fields.Selection([
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),
        ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),
        ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),
    ], string='Mes', required=True)

    anno = fields.Integer(string='Año', default=lambda self: datetime.now().year, required=True)

    html_resultados = fields.Html(string='Resultados', readonly=True)  # Campo para almacenar el informe en HTML

    @api.onchange('lugar', 'mes', 'anno')
    def _onchange_filtrar_trabajos(self):
        # Limpiar resultados anteriores
        self.html_resultados = ""

        # Verificar si se han seleccionado lugar, mes y año
        if self.lugar and self.mes and self.anno:
            # Obtener el último día del mes seleccionado
            ultimo_dia_mes = calendar.monthrange(self.anno, int(self.mes))[1]

            # Filtrar los trabajos por lugar, mes y año
            trabajos = self.env['elihel.barco'].search([
                ('lugar', '=', self.lugar),
                ('fecha_llegada', '>=', f'{self.anno}-{self.mes}-01'),
                ('fecha_llegada', '<=', f'{self.anno}-{self.mes}-{ultimo_dia_mes}'),
            ])

            # Obtener las descripciones de los servicios desde el modelo Servicio
            servicio_model = self.env['elihel.servicio']
            tipo_servicio_selection = dict(servicio_model._fields['tipo_servicio'].selection)

            # Generar el informe en HTML
            html_content = """
                <style>
                    .informe {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }
                    .informe h2 {
                        color: #333;
                    }
                    .informe .fila {
                        display: flex;
                        border-bottom: 1px solid #ddd;
                        padding: 8px 0;
                    }
                    .informe .columna {
                        flex: 1;
                        padding: 0 10px;
                    }
                    .informe .encabezado {
                        font-weight: bold;
                        background-color: #f2f2f2;
                        border-bottom: 2px solid #ddd;
                    }
                </style>
                <div class="informe">
                    <h2>Informe de Trabajos</h2>
                    <div class="row">
                        <div class="columna">Certificado</div>
                        <div class="columna">Barco</div>
                        <div class="columna">Matrícula</div>
                        <div class="columna">Fecha</div>
                        <div class="columna">Camiones</div>
                        <div class="columna">Servicios</div>
                    </div>
            """

            for trabajo in trabajos:
                # Generar filas para cada camión y sus servicios
                for i, camion in enumerate(trabajo.camion_ids):
                    # Obtener los servicios del camión
                    servicios_texto = ", ".join([
                        f"{tipo_servicio_selection.get(servicio.tipo_servicio, servicio.tipo_servicio)} ({servicio.cantidad})"
                        for servicio in camion.servicio_ids
                    ])

                    # Si es el primer camión, mostrar los datos del trabajo
                    if i == 0:
                        html_content += f"""
                            <div class="row">
                                <div class="columna">{trabajo.numero_certificado}</div>
                                <div class="columna">{trabajo.nombre}</div>
                                <div class="columna">{trabajo.matricula}</div>
                                <div class="columna">{trabajo.fecha_llegada}</div>
                                <div class="columna">{camion.matricula}</div>
                                <div class="columna">{servicios_texto}</div>
                            </div>
                        """
                    else:
                        # Para los camiones siguientes, dejar las primeras columnas vacías
                        html_content += f"""
                            <div class="row">
                                <div class="columna"></div>
                                <div class="columna"></div>
                                <div class="columna"></div>
                                <div class="columna"></div>
                                <div class="columna">{camion.matricula}</div>
                                <div class="columna">{servicios_texto}</div>
                            </div>
                        """

            html_content += """
                </div>
            """

            # Asignar el contenido HTML al campo
            self.html_resultados = html_content

class WizardTrabajosResultado(models.TransientModel):
    _name = 'elihel.wizard_trabajos.resultado'
    _description = 'Resultados del Wizard de Trabajos'

    wizard_id = fields.Many2one(
        'elihel.wizard_trabajos',  # Modelo relacionado
        string='Wizard',  # Etiqueta del campo
    )  # Relación con el wizard

    numero_certificado = fields.Char(string='Número de Certificado' )  # Número de certificado
    fecha_llegada = fields.Date(string='Fecha de Llegada')  # Fecha de llegada
    matricula_camion = fields.Char(string='Matrícula del Camión')  # Matrícula del camión
    servicios = fields.Text(string='Servicios')  # Lista de servicios