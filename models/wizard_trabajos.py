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
    html_resultados = fields.Html(string='Resultados', readonly=True)

    @api.onchange('lugar', 'mes', 'anno')
    def _onchange_filtrar_trabajos(self):
        self.html_resultados = ""

        if self.lugar and self.mes and self.anno:
            ultimo_dia_mes = calendar.monthrange(self.anno, int(self.mes))[1]

            trabajos = self.env['elihel.barco'].search([
                ('lugar', '=', self.lugar),
                ('fecha_llegada', '>=', f'{self.anno}-{self.mes}-01'),
                ('fecha_llegada', '<=', f'{self.anno}-{self.mes}-{ultimo_dia_mes}'),
            ])

            servicio_model = self.env['elihel.servicio']
            tipo_servicio_selection = dict(servicio_model._fields['tipo_servicio'].selection)

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
                primera_fila_trabajo = True
                for camion in trabajo.camion_ids:
                    for i, servicio in enumerate(camion.servicio_ids or [None]):
                        html_content += "<tr>"
                        if primera_fila_trabajo and i == 0:
                            html_content += f"""
                                <td rowspan="{sum(max(len(c.servicio_ids), 1) for c in trabajo.camion_ids)}">{trabajo.numero_certificado}</td>
                                <td rowspan="{sum(max(len(c.servicio_ids), 1) for c in trabajo.camion_ids)}">{trabajo.nombre}</td>
                                <td rowspan="{sum(max(len(c.servicio_ids), 1) for c in trabajo.camion_ids)}">{trabajo.matricula}</td>
                                <td rowspan="{sum(max(len(c.servicio_ids), 1) for c in trabajo.camion_ids)}">{trabajo.fecha_llegada}</td>
                            """
                            primera_fila_trabajo = False
                        if i == 0:
                            html_content += f"<td rowspan='{max(len(camion.servicio_ids), 1)}'>{camion.matricula}</td>"
                        if servicio:
                            descripcion_servicio = tipo_servicio_selection.get(servicio.tipo_servicio, servicio.tipo_servicio)
                            html_content += f"<td>{descripcion_servicio} ({servicio.cantidad})</td>"
                        else:
                            html_content += "<td></td>"
                        html_content += "</tr>"

            html_content += """
                        </tbody>
                    </table>
                </div>
            """
            self.html_resultados = html_content

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