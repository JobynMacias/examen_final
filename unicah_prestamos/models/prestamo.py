from odoo import api, fields, models
from odoo.exceptions import ValidationError

class UnicahPrestamo(models.Model):
    _name = "unicah.prestamo"
    _description = "Préstamo de equipo universitario"
    _order = "fecha_inicio desc, id desc"

    name = fields.Char(string="Referencia", required=True)
    partner_id = fields.Many2one("res.partner", string="Solicitante", required=True, ondelete="restrict")
    equipo_id = fields.Many2one("product.product", string="Equipo", required=True, ondelete="restrict")
    fecha_inicio = fields.Date(string="Fecha de préstamo", required=True, default=fields.Date.context_today)
    fecha_fin = fields.Date(string="Fecha prevista de devolución", required=True)
    dias = fields.Integer(string="Días de préstamo", compute="_compute_dias", store=True)
    state = fields.Selection([("borrador", "Borrador"), ("prestado", "Prestado"), ("devuelto", "Devuelto")], string="Estado", default="borrador", required=True)
    notas = fields.Text(string="Observaciones")

    @api.depends("fecha_inicio", "fecha_fin")
    def _compute_dias(self):
        for loan in self:
            loan.dias = (loan.fecha_fin - loan.fecha_inicio).days + 1 if loan.fecha_inicio and loan.fecha_fin else 0

    @api.constrains("fecha_inicio", "fecha_fin", "equipo_id", "state")
    def _check_prestamo(self):
        for loan in self:
            if loan.fecha_fin < loan.fecha_inicio:
                raise ValidationError("La devolución no puede ser anterior al préstamo.")
            if loan.state == "prestado" and self.search_count([("id", "!=", loan.id), ("equipo_id", "=", loan.equipo_id.id), ("state", "=", "prestado"), ("fecha_inicio", "<=", loan.fecha_fin), ("fecha_fin", ">=", loan.fecha_inicio)]):
                raise ValidationError("El equipo ya tiene un préstamo activo en esas fechas.")

    def action_prestar(self):
        self.write({"state": "prestado"})

    def action_devolver(self):
        self.write({"state": "devuelto"})
