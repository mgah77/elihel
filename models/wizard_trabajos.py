import base64
import xlwt
from io import BytesIO
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
    html_resultados = fields.Html(string='Resultados', readonly=True, default="")


    def exportar_a_excel(self):
        # Obtener los datos filtrados
        ultimo_dia_mes = calendar.monthrange(self.anno, int(self.mes))[1]
        trabajos = self.env['elihel.barco'].search([
            ('lugar', '=', self.lugar),
            ('fecha_llegada', '>=', f'{self.anno}-{self.mes}-01'),
            ('fecha_llegada', '<=', f'{self.anno}-{self.mes}-{ultimo_dia_mes}'),
        ])

        # Obtener las descripciones de los servicios
        servicio_model = self.env['elihel.servicio']
        tipo_servicio_selection = dict(servicio_model._fields['tipo_servicio'].selection)

        # Crear un libro de Excel y una hoja
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Trabajos')

        # Definir los encabezados fijos
        headers_fijos = [
            'Certificado', 'Barco', 'Matrícula', 'Fecha', 'Camiones'
        ]

        # Obtener todos los servicios únicos con sus descripciones
        servicios_unicos = set()
        for trabajo in trabajos:
            for camion in trabajo.camion_ids:
                for servicio in camion.servicio_ids:
                    descripcion_servicio = tipo_servicio_selection.get(servicio.tipo_servicio, servicio.tipo_servicio)
                    servicios_unicos.add(descripcion_servicio)

        # Convertir el conjunto de servicios únicos a una lista ordenada
        servicios_unicos = sorted(list(servicios_unicos))

        # Escribir los encabezados fijos
        for col, header in enumerate(headers_fijos):
            sheet.write(0, col, header)

        # Escribir los encabezados de servicios
        for col, servicio in enumerate(servicios_unicos, start=len(headers_fijos)):
            sheet.write(0, col, servicio)

        # Escribir los datos
        row = 1
        for trabajo in trabajos:
            primera_fila_trabajo = True  # Bandera para la primera fila del trabajo
            for camion in trabajo.camion_ids:
                # Formatear la fecha en formato dd-mmm-YY
                fecha_formateada = trabajo.fecha_llegada.strftime('%d-%b-%y')

                # Escribir los datos fijos solo en la primera fila del trabajo
                if primera_fila_trabajo:
                    sheet.write(row, 0, trabajo.numero_certificado)
                    sheet.write(row, 1, trabajo.nombre)
                    sheet.write(row, 2, trabajo.matricula)
                    sheet.write(row, 3, fecha_formateada)
                    primera_fila_trabajo = False
                else:
                    # Dejar vacías las celdas de Certificado, Barco, Matrícula y Fecha
                    sheet.write(row, 0, "")
                    sheet.write(row, 1, "")
                    sheet.write(row, 2, "")
                    sheet.write(row, 3, "")

                # Escribir los datos del camión
                sheet.write(row, 4, camion.matricula)

                # Contar los servicios por tipo para este camión
                servicios_camion = {}
                for servicio in camion.servicio_ids:
                    descripcion_servicio = tipo_servicio_selection.get(servicio.tipo_servicio, servicio.tipo_servicio)
                    if descripcion_servicio in servicios_camion:
                        servicios_camion[descripcion_servicio] += servicio.cantidad
                    else:
                        servicios_camion[descripcion_servicio] = servicio.cantidad

                # Escribir la cantidad de servicios por tipo
                for col, servicio in enumerate(servicios_unicos, start=len(headers_fijos)):
                    cantidad = servicios_camion.get(servicio, 0)
                    sheet.write(row, col, cantidad)

                row += 1

        # Guardar el archivo en un objeto BytesIO
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Codificar el archivo en base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Crear un registro de ir.attachment para descargar el archivo
        attachment = self.env['ir.attachment'].create({
            'name': f"Informe_Trabajos_{self.lugar}_{self.mes}_{self.anno}.xls",
            'datas': excel_file,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
        })

        # Devolver una acción para descargar el archivo
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{attachment.id}?download=true",
            'target': 'self',
        }

    @api.onchange('lugar', 'mes', 'anno')
    def _onchange_filtrar_trabajos(self):
        # Reiniciar el contenido HTML correctamente
        html_content = ""
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
                                    <th style="padding-left:10px">Barco</th>
                                    <th style="padding-left:10px">Matrícula</th>
                                    <th style="padding-left:10px">Fecha</th>
                                    <th style="padding-left:10px">Camiones</th>
                                    <th style="padding-left:10px">Cantidad de Servicios</th>
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
                                    <td style="padding-left:10px">{trabajo.nombre}</td>
                                    <td style="padding-left:10px">{trabajo.matricula}</td>
                                    <td style="padding-left:10px">{trabajo.fecha_llegada}</td>
                                    <td style="padding-left:10px">{camion.matricula}</td>
                                    <td style="padding-left:10px">{cantidad_servicios} servicio{'s' if cantidad_servicios != 1 else ''}</td>
                                </tr>
                            """
                            primera_fila = False
                        else:
                            html_content += f"""
                                <tr>
                                    <td></td>
                                    <td style="padding-left:10px"></td>
                                    <td style="padding-left:10px"></td>
                                    <td style="padding-left:10px"></td>
                                    <td style="padding-left:10px">{camion.matricula}</td>
                                    <td style="padding-left:10px">{cantidad_servicios} servicio{'s' if cantidad_servicios != 1 else ''}</td>
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