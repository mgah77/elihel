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
                    .informe table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }
                    .informe th, .informe td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    .informe th {
                        background-color: #f2f2f2;
                    }
                    .informe ul {
                        list-style-type: none;
                        padding: 0;
                        margin: 0;
                    }
                    .informe ul li {
                        margin: 5px 0;
                    }
                </style>
                <div class="informe">
                    <h2>Informe de Trabajos</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Certificado</th>
                                <th>Barco</th>
                                <th>Matrícula</th>
                                <th>Fecha</th>
                                <th>Camiones</th>
                                <th>Servicios</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            for trabajo in trabajos:
                # Contador para saber cuántas filas se han generado para este trabajo
                filas_generadas = 0

                # Obtener el número total de servicios en todos los camiones del trabajo
                total_servicios = sum(len(camion.servicio_ids) for camion in trabajo.camion_ids)

                # Generar la primera fila del trabajo con la información común
                html_content += f"""
                    <tr>
                        <td rowspan="{total_servicios}">{trabajo.numero_certificado}</td>
                        <td rowspan="{total_servicios}">{trabajo.nombre}</td>
                        <td rowspan="{total_servicios}">{trabajo.matricula}</td>
                        <td rowspan="{total_servicios}">{trabajo.fecha_llegada}</td>
                """

                # Iterar sobre los camiones del trabajo
                for camion in trabajo.camion_ids:
                    # Iterar sobre los servicios del camión
                    for i, servicio in enumerate(camion.servicio_ids):
                        # Obtener la descripción del servicio desde el campo selection
                        descripcion_servicio = tipo_servicio_selection.get(servicio.tipo_servicio, servicio.tipo_servicio)

                        # Si es la primera fila del trabajo, mostrar el primer camión
                        if filas_generadas == 0:
                            html_content += f"""
                                <td>{camion.nombre}</td>
                                <td>{descripcion_servicio} ({servicio.cantidad})</td>
                                </tr>
                            """
                        else:
                            # Si no es la primera fila, solo mostrar el servicio
                            html_content += f"""
                                <tr>
                                    <td></td> <!-- Columna de camión vacía -->
                                    <td>{descripcion_servicio} ({servicio.cantidad})</td>
                                </tr>
                            """
                        filas_generadas += 1

            html_content += "</tbody>"
                    </table>
                </div>
            
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