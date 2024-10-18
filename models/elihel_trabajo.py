from odoo import models, fields , api , _

class Elihel_Trabajos(models.Model):

    _name = 'elihel.main'
    _description = 'Elihel Ingreso'

    name = fields.Char(string="Nro ", readonly=True, default='Nuevo', copy=False)

    fecha = fields.Date('Fecha', default=fields.Date.context_today)
    cliente = fields.Many2one('res.partner',string='Cliente')
    obs = fields.Html('Observaciones')
    main_line = fields.One2many(comodel_name = 'elihel.datos',inverse_name = 'main_line_id', string = 'Lineas OT',copy=True)
    lugar = fields.Selection([
        ('pmo','Puerto Montt'),       
        ('cco','Chacabuco')
        ],string='Lugar')
    state = fields.Selection([
        ('borr','Borrador'),       
        ('cert','Certificado'),
        ('fact','Facturado')
        ],string='Status',default='borr')

class Elihel_Detalle(models.Model):
    _name = 'elihel.datos'
    _description = 'Elihel detalle'

    main_line_id = fields.Many2one('elihel.main', string='lineas main', required=True, ondelete='cascade', index=True, copy=False)
  
    nave = fields.Many2one('elihel.nave.rel', string='Nave / Camion', domain="[('es_camion', '=', False)]", store=True)
    lyd = fields.Integer(string="L y D", help="Limpieza y Desinfeccion")
    sai = fields.Integer(string="S Int", help="Sanitizado Interior")
    vuf = fields.Integer(string="V F", help="Vuelta Falsa")
    crm = fields.Integer(string="C.R.M.", help="Contenedores Redes Materiales")
    rfr = fields.Integer(string="Reefer", help="Reefer")
    eee = fields.Integer(string="E.E.E.", help="Estanque ensilaje y equipos")
    rox = fields.Integer(string="Rack O", help="Rack Oxigeno")
    pcr = fields.Integer(string="Portacr", help="Portacrios")
    rag = fields.Integer(string="Rack Ag", help="Rack Agua")
    bic = fields.Integer(string="Bin Co", help="Bins Completos")
    bmm = fields.Integer(string="Bin Mo", help="Bins Mort/Mat/Viv")
    lob = fields.Integer(string="Lona B", help="Lonas baño peces")
    ibc = fields.Integer(string="IBC", help="IBC")
    ist = fields.Integer(string="Isot", help="Isotanques")
    stk = fields.Integer(string="stk", help="Estanque Combustible")
    moc = fields.Integer(string="Motocom", help="Motocompresor")
    cbu = fields.Integer(string="Compr B", help="Compresor Buceo")
    pdo = fields.Integer(string="P Dob", help="Pasillo Doble")
    pdt = fields.Integer(string="P Dob T", help="Pasillo Doble T")
    psi = fields.Integer(string="P Simp", help="Pasillo Simple")
    pst = fields.Integer(string="P T", help="Pasillo T")
    crp = fields.Integer(string="Cruc P", help="Cruceta Pasillos")
    exm = fields.Integer(string="Ext Mor", help="Extractor Mort")
    flg = fields.Integer(string="Flot. G", help="Flot. Grandes")
    flc = fields.Integer(string="Flot. C", help="Flot. Chicos")
    byp = fields.Integer(string="Boya Pl", help="Boyas Plasticas")
    bym = fields.Integer(string="Boya Me", help="Boyas Metalicas")
    bot = fields.Integer(string="Bote", help="Bote")
    rpe = fields.Integer(string="Reja Pe", help="Rejas Perimetrales")
    pls = fields.Integer(string="Plansa", help="Plansas")
    con = fields.Integer(string="Cono Mo", help="Conos Mortex")
    tah = fields.Integer(string="Tam Hid", help="Tambores Hidrocarb.")
    rol = fields.Integer(string="R Cabos", help="Rollos Cabos")
    plu = fields.Integer(string="Caja Pl", help="Cajas Plumavit")
    cad = fields.Integer(string="Paño Cd", help="Paño Cadenas")
    mat = fields.Integer(string="Mat R", help="Mat. Retorno")
    ens = fields.Integer(string="Ensil.", help="Ensilaje")

    obs = fields.Char('Observaciones')
    serie = fields.Char('Serie')

class Elihel_Nave(models.Model):
    _name = 'elihel.nave.rel'
    _description = 'elihel naves rel'

    name = fields.Char('Nave', default='Nuevo', index=True)   
    es_camion = fields.Boolean(string="Camion", default=False)
    matricula  = fields.Char(string="Matricula", size=6)
    precio = fields.Integer(string = "valor", default=0)

class Elihel_ServiciosNavePMO(models.Model):
    _name = 'elihel.serv_pmo.rel'
    _description = 'elihel servicios rel'

    name = fields.Char('Servicio', index=True)   
    precio = fields.Integer(string = "valor")

class Elihel_ServiciosNaveCCO(models.Model):
    _name = 'elihel.serv_cco.rel'
    _description = 'elihel servicios rel'

    name = fields.Char('Servicio', index=True)   
    precio = fields.Integer(string = "valor")

