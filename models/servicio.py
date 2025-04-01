from odoo import models, fields

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
        return


class PrecioServicio(models.Model):
    _name = 'elihel.precio.servicio'
    _description = 'Precios de Servicios'

    tipo_servicio = fields.Selection(
        selection=lambda self: self.env['elihel.servicio']._fields['tipo_servicio'].selection,
        string='Tipo de Servicio',
        required=True,
        unique=True
    )
  
    precio = fields.Integer(
        string='Precio',
        required=True,
        default=0
    )

    descripcion = fields.Char(
        string='Descripción',
        compute='_compute_descripcion',
        store=True
    )
    
    @api.depends('tipo_servicio')
    def _compute_descripcion(self):
        return
    
    