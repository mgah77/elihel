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
    lyd = fields.Boolean(string="L y D", help="Limpieza y Desinfeccion")
    sai = fields.Boolean(string="S I", help="Sanitizado Interior")
    vuf = fields.Boolean(string="V F", help="Vuelta Falsa")
    crm = fields.Boolean(string="CRM", help="Contenedores Redes Materiales")
    rfr = fields.Boolean(string="Rfr", help="Reefer")
    eee = fields.Boolean(string="EEE", help="Estanque ensilaje y equipos")
    rox = fields.Boolean(string="R O", help="Rack Oxigeno")
    pcr = fields.Boolean(string="Pcr", help="Portacrios")
    rag = fields.Boolean(string="R A", help="Rack Agua")
    bin = fields.Boolean(string="B C", help="Bins Completos")
    bmm = fields.Boolean(string="B M", help="Bins Mort/Mat/Viv")
    lob = fields.Boolean(string="L B", help="Lonas de baño")
    ibc = fields.Boolean(string="IBC", help="IBC")
    ist = fields.Boolean(string="Iso", help="Isotanques")
    stk = fields.Boolean(string="stk", help="Stk Combustible")
    moc = fields.Boolean(string="M C", help="Motocompresor")
    cbu = fields.Boolean(string="C B", help="Compresor Buceo")
    pdo = fields.Boolean(string="PD", help="Pasillo Doble")
    pdt = fields.Boolean(string="PDT", help="Pasillo Doble T")
    psi = fields.Boolean(string="PS", help="Pasillo Simple")
    pst = fields.Boolean(string="PT", help="Pasillo T")
    crp = fields.Boolean(string="CP", help="Cruceta Pasillos")
    exm = fields.Boolean(string="Ex M", help="Extracion Mort")
    flg = fields.Boolean(string="Fl G", help="Flot. Grandes")
    flc = fields.Boolean(string="Fl C", help="Flot. Chicos")
    byp = fields.Boolean(string="B. Pl", help="Boyas Plast.")
    bym = fields.Boolean(string="B. Me.", help="Boyas Metalicas")
    bot = fields.Boolean(string="Bote", help="Bote")
    rpe = fields.Boolean(string="R Pe", help="Rejas Perimetrales")
    pls = fields.Boolean(string="Pla", help="Plansas")
    con = fields.Boolean(string="C M", help="Conos Mortex")
    tah = fields.Boolean(string="T H", help="Tambores Hidrocarb.")
    rol = fields.Boolean(string="R C", help="Rollos Cabos")
    plu = fields.Boolean(string="C Plu", help="Cajas Plumavit")
    mat = fields.Boolean(string="Mat R", help="Mat. Ret.")
    ens = fields.Boolean(string="Ens", help="Ensilaje")

    obs = fields.Char('Observaciones')
    serie = fields.Char('Serie')

class Elihel_Nave(models.Model):
    _name = 'elihel.nave.rel'
    _description = 'elihel naves rel'

    name = fields.Char('Nave', default='Nuevo', index=True)   
    es_camion = fields.Boolean(string="Camion")
    matricula  = fields.Char(string="Matricula", size=6)
    precio = fields.Integer(string = "valor", default=0)
