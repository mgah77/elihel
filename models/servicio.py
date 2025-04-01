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