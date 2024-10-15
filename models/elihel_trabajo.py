from odoo import models, fields , api , _

class Elihel_Trabajos(models.Model):

    _name = 'elihel.main'
    _description = 'Elihel Ingreso'

    name = fields.Char(string="Nro ", readonly=True, default='Nuevo', copy=False)

    fecha = fields.Date('Fecha', default=fields.Date.context_today)
    cliente = fields.Many2one('res.partner',string='Cliente',domain="[('type', '!=', 'private'), ('is_company', '=', True), ('type','=','contact')]")
    obs = fields.Html('Observaciones')
    main_line = fields.One2many(comodel_name = 'elihel.datos',inverse_name = 'main_line_id', string = 'Lineas OT',copy=True)
    
    state = fields.Selection([
        ('borr','Borrador'),       
        ('cert','Certificado'),
        ('fact','Facturado')
        ],string='Status',default='borr')

class Elihel_Detalle(models.Model):
    _name = 'elihel.datos'
    _description = 'Elihel detalle'

    main_line_id = fields.Many2one('elihel.main', string='lineas main', required=True, ondelete='cascade', index=True, copy=False)
  
    nave = fields.Many2one('elihel.nave.rel', string='Nave / Camion', domain="[('dueno', '=', main_line_id.cliente)]", store=True)
    obs = fields.Char('Observaciones')
    serie = fields.Char('Serie')

class Elihel_Nave(models.Model):
    _name = 'elihel.nave.rel'
    _description = 'elihel naves rel'

    nave = fields.Char('Nave', default='Nuevo', index=True)
    dueno = fields.Many2one('res.partner', string='Dueño',domain="[('type', '!=', 'private'), ('is_company', '=', True), ('type','=','contact')]")
    es_camion = fields.Boolean(string="Camion")
    matricula  = fields.Char(string="Matricula", size=6)
    precio = fields.Integer(string = "valor", default=0)
