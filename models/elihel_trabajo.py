from odoo import models, fields , api , _

class Elihel_Trabajos(models.Model):

    _name = 'elihel.main'
    _description = 'Elihel Ingreso'

    name = fields.Char(string="Nro ", readonly=True, default='Nuevo', copy=False)

    fecha = fields.Date('Fecha', default=fields.Date.context_today)
    cliente = fields.Many2one('res.partner',string='Cliente')
    obs = fields.Html('Observaciones')
    nave = fields.Many2one('elihel.nave.rel', string='Embarcacion', store=True)
    camiones = fields.Boolean(string="Lleva camiones?", default=False)
    
    lugar = fields.Selection([
        ('pmo','Puerto Montt'),       
        ('cco','Chacabuco')
        ],string='Lugar')
    state = fields.Selection([
        ('borr','Borrador'),       
        ('cert','Certificado'),
        ('fact','Facturado')
        ],string='Status',default='borr')
    lyd = fields.Integer(string="Limp. y Desinfeccion", help="Limpieza y Desinfeccion")
    sai = fields.Integer(string="Sanitizado Interior", help="Sanitizado Interior")
    vuf = fields.Integer(string="Vuelta Falsa", help="Vuelta Falsa")
    crm = fields.Integer(string="Cont. Redes Materiales", help="Contenedores Redes Materiales")
    rfr = fields.Integer(string="Reefer", help="Reefer")
    eee = fields.Integer(string="Estanque ensil. y equip", help="Estanque ensilaje y equipos")
    rox = fields.Integer(string="Rack Oxigeno", help="Rack Oxigeno")
    pcr = fields.Integer(string="Portacrios", help="Portacrios")
    rag = fields.Integer(string="Rack Agua", help="Rack Agua")
    bic = fields.Integer(string="Bins Completos", help="Bins Completos")
    bmm = fields.Integer(string="Bins Mort/Mat/Viv", help="Bins Mort/Mat/Viv")
    lob = fields.Integer(string="Lonas baño peces", help="Lonas baño peces")
    ibc = fields.Integer(string="IBC", help="IBC")
    ist = fields.Integer(string="Isotanques", help="Isotanques")
    stk = fields.Integer(string="Estanque Combustible", help="Estanque Combustible")
    moc = fields.Integer(string="Motocompresor", help="Motocompresor")
    cbu = fields.Integer(string="Compresor Buceo", help="Compresor Buceo")
    pdo = fields.Integer(string="Pasillo Doble", help="Pasillo Doble")
    pdt = fields.Integer(string="Pasillo Doble T", help="Pasillo Doble T")
    psi = fields.Integer(string="Pasillo Simple", help="Pasillo Simple")
    pst = fields.Integer(string="Pasillo T", help="Pasillo T")
    crp = fields.Integer(string="Cruceta Pasillos", help="Cruceta Pasillos")
    exm = fields.Integer(string="Extractor Mort", help="Extractor Mort")
    flg = fields.Integer(string="Flot. Grandes", help="Flot. Grandes")
    flc = fields.Integer(string="Flot. Chicos", help="Flot. Chicos")
    byp = fields.Integer(string="Boyas Plasticas", help="Boyas Plasticas")
    bym = fields.Integer(string="Boyas Metalicas", help="Boyas Metalicas")
    bot = fields.Integer(string="Bote", help="Bote")
    rpe = fields.Integer(string="Rejas Perimetrales", help="Rejas Perimetrales")
    pls = fields.Integer(string="Plansas", help="Plansas")
    con = fields.Integer(string="Conos Mortex", help="Conos Mortex")
    tah = fields.Integer(string="Tambores Hidrocarb.", help="Tambores Hidrocarb.")
    rol = fields.Integer(string="Rollos Cabos", help="Rollos Cabos")
    plu = fields.Integer(string="Cajas Plumavit", help="Cajas Plumavit")
    cad = fields.Integer(string="Paño Cadenas", help="Paño Cadenas")
    mat = fields.Integer(string="Mat. Retorno", help="Mat. Retorno")
    ens = fields.Integer(string="Ensilaje", help="Ensilaje")



class Elihel_Nave(models.Model):
    _name = 'elihel.nave.rel'
    _description = 'elihel naves rel'

    name = fields.Char('Nave', default='Nuevo', index=True)   
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

