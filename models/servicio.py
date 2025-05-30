from odoo import models, fields, api

class Servicio(models.Model):
    _name = 'elihel.servicio'
    _description = 'Servicio'
    _rec_name = 'tipo_servicio'  # Define el campo 'tipo_servicio' como el nombre predeterminado

    # Lista de tipos de servicios
    TIPO_SERVICIO_SELECTION = [
        ('des', 'Desinfección'),
        ('rfr', 'Reffer'),
        ('eee', 'Estanque ensilaje y equipos'),
        ('pdo', 'Pasillo Doble'),
        ('pdt', 'Pasillo Doble T'),
        ('psi', 'Pasillo simple'),
        ('pst', 'Pasillo T'),
        ('pls', 'Plansas'),
        ('con', 'Conos Mortex'),
        ('tah', 'Tambores Hidrocarburos'),
        ('rol', 'Rollo Cabos'),
        ('plu', 'Cajas Plumavit'),
        ('cad', 'Paño Cadenas'),
        ('crp', 'Cruceta Pasillos'),
        ('exm', 'Extrator Mort'),
        ('flg', 'Flotadores Grandes'),
        ('flc', 'Flotadores Chicos'),
        ('bym', 'Boyas Metalicas'),
        ('byp', 'Boyas Plasticas'),
        ('bot', 'Bote'),
        ('bic', 'Bins Completo'),
        ('bmm', 'Bins Cosecha/Mort'),
        ('lob', 'Lona Balo Peces'),
        ('mat', 'Mat Retorno'),
        ('moc', 'Motocompresor'),
        ('rox', 'Rack Oxigeno'),
        ('pcr', 'Portacrios'),
        ('rag', 'Rack Agua'),
        ('ibc', 'IBC'),
        ('stk', 'Estanque Combustible'),
        ('ens', 'Ensilaje'),
        ('ist', 'Isotanque'),
        ('cbu', 'Compresor Buceo'),
        ('rpe', 'Rejas Perimetrales'),
        ('crm', 'Contenedores'),   
    ]

    tipo_servicio = fields.Selection(
        TIPO_SERVICIO_SELECTION,
        string='Tipo de Servicio',
        required=True
    )  # Tipo de servicio

    cantidad = fields.Integer(string='Cantidad', required=True)  # Cantidad del servicio
    camion_id = fields.Many2one('elihel.camion', string='Camión', ondelete='cascade')  # Relación con el camión

    # Nuevo campo para precio unitario (calculado)
    precio_unitario = fields.Integer(
        string='Precio Unitario',
        compute='_compute_precio_unitario',
        store=True
    )

    def _compute_precio_unitario(self):
        precio_model = self.env['elihel.precio.servicio']
        for servicio in self:
            # Obtenemos el lugar del barco asociado al camión
            lugar = servicio.camion_id.barco_id.lugar if servicio.camion_id and servicio.camion_id.barco_id else False
            if lugar:
                precio = precio_model.search([
                    ('tipo_servicio', '=', servicio.tipo_servicio),
                    ('lugar', '=', lugar)
                ], limit=1)
                servicio.precio_unitario = precio.precio if precio else 0
            else:
                servicio.precio_unitario = 0


class PrecioServicio(models.Model):
    _name = 'elihel.precio.servicio'
    _description = 'Precios de Servicios'
    _rec_name = 'tipo_servicio'

    tipo_servicio = fields.Selection(
        selection=lambda self: self.env['elihel.servicio']._fields['tipo_servicio'].selection,
        string='Tipo de Servicio',
        required=True
    )
    
    lugar = fields.Selection([
        ('pue', 'Puerto Montt'),
        ('cco', 'Chacabuco'),
    ], string='Lugar', required=True)
    
    precio = fields.Integer(
        string='Precio',
        required=True,
        default=0
    )

    dato = fields.Char(
        string='Descripción',
        compute='_compute_dato',
        store=True
    )

    _sql_constraints = [
        ('precio_servicio_lugar_uniq', 'unique(tipo_servicio, lugar)', 'Ya existe un precio para este servicio en este lugar!'),
    ]

    @api.depends('tipo_servicio')
    def _compute_dato(self):
        for record in self:
            # Obtenemos la lista de selección del modelo Servicio
            servicio_model = self.env['elihel.servicio']
            selection_list = servicio_model._fields['tipo_servicio'].selection
            # Convertimos a diccionario
            selection_dict = dict(selection_list)
            # Asignamos la descripción correspondiente al código
            record.dato = selection_dict.get(record.tipo_servicio, '')