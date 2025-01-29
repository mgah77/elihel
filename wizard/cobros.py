from odoo import models, fields, api

class ElihelCobrosMesWizard(models.TransientModel):
    _name = 'elihel.cobros.mes.wizard'
    _description = 'Wizard para filtrar cobros por mes'

    mes = fields.Selection([
        ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'),
        ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'),
        ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ], string='Mes', required=True)
    
    cobros_ids = fields.Many2many('elihel.main', string='Registros del mes')
    
    @api.onchange('mes')
    def _onchange_mes(self):
        if self.mes:
            self.cobros_ids = self.env['elihel.main'].search([
                ('fecha', '>=', f'2024-{self.mes}-01'), ('fecha', '<=', f'2024-{self.mes}-31')
            ])
    
    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        mes_actual = fields.Date.today().strftime('%m')
        vals['mes'] = mes_actual
        vals['cobros_ids'] = [(6, 0, self.env['elihel.main'].search([
            ('fecha', '>=', f'2024-{mes_actual}-01'), ('fecha', '<=', f'2024-{mes_actual}-31')
        ]).ids)]
        return vals