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
        # Reiniciar el contenido HTML correctamente
        self.html_resultados = ""

        if self.lugar and self.mes and self.anno:
            ultimo_dia_mes = calendar.monthrange(self.anno, int(self.mes))[1]

            trabajos = self.env['elihel.barco'].search([
                ('lugar', '=', self.lugar),
                ('fecha_llegada', '>=', f'{self.anno}-{self.mes}-01'),
                ('fecha_llegada', '<=', f'{self.anno}-{self.mes}-{ultimo_dia_mes}'),
            ])

            if trabajos:  # Solo agregar el título si hay datos
                html_content = """                   
                    <div class="clearfix">
                    <div>
                        <h2>Informe de Trabajos</h2>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 10px">
                            <thead>
                                <tr>
                                    <th>Certificado</th>
                                    <th style="padding-left:20px">Barco</th>
                                    <th style="padding-left:20px">Matrícula</th>
                                    <th style="padding-left:20px">Fecha</th>
                                    <th style="padding-left:20px">Camiones</th>
                                    <th style="padding-left:20px">Cantidad de Servicios</th>
                                </tr>
                            </thead>
                            <tbody>
                """
                for trabajo in trabajos:
                    primera_fila = True
                    for camion in trabajo.camion_ids:
                        cantidad_servicios = len(camion.servicio_ids)
                        if primera_fila:
                            html_content += f"""
                                <tr>
                                    <td>{trabajo.numero_certificado}</td>
                                    <td style="padding-left:20px">{trabajo.nombre}</td>
                                    <td style="padding-left:20px">{trabajo.matricula}</td>
                                    <td style="padding-left:20px">{trabajo.fecha_llegada}</td>
                                    <td style="padding-left:20px">{camion.matricula}</td>
                                    <td style="padding-left:20px">{cantidad_servicios} servicio{'s' if cantidad_servicios != 1 else ''}</td>
                                </tr>
                            """
                            primera_fila = False
                        else:
                            html_content += f"""
                                <tr>
                                    <td></td>
                                    <td style="padding-left:20px"></td>
                                    <td style="padding-left:20px"></td>
                                    <td style="padding-left:20px"></td>
                                    <td style="padding-left:20px">{camion.matricula}</td>
                                    <td style="padding-left:20px">{cantidad_servicios} servicio{'s' if cantidad_servicios != 1 else ''}</td>
                                </tr>
                            """

                html_content += """
                            </tbody>
                        </table>
                    </div>
                    </div>
                """
                self.html_resultados = html_content
            else:
                self.html_resultados = "<p>No hay trabajos en este período.</p>"


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