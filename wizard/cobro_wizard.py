from odoo import models, fields, api
from datetime import date

class EstadoWizard(models.TransientModel):
    _name = "wizard.cobro"
    _description = "Estado de pago de clientes"
    
    mes = fields.Selection([
        ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'),
        ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'),
        ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ], string='Mes', required=True)
    
    
    @api.depends('cliente')
    def _compute_cantidad_vencida(self):
        return

    def action_print_report(self):
        return

#   @api.depends('facturas_in')
#    def _compute_detalles_facturas_in(self):
#        for record in self:
#            detalles = ""
#            for factura in record.facturas_in:
#                detalles += (
#                    f"Factura: {factura.sii_document_number or 'N/A'}, "
#                    f"Vencimiento: {factura.invoice_date_due.strftime('%d-%b-%Y') if factura.invoice_date_due else 'Sin fecha'}, "
#                    f"Monto: ${factura.amount_residual_signed:,.0f}".replace(",", ".") + "\n"
#                )
#            record.detalles_facturas_in = detalles