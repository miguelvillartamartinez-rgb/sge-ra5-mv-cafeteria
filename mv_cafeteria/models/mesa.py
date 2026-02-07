from odoo import models, fields, api

class CafeMesa(models.Model):
    _name = "cafe.mesa"
    _description = "Mesa de cafetería"

    name = fields.Char(string="Mesa", required=True)
    capacidad = fields.Integer(string="Capacidad", default=2)

    ubicacion = fields.Selection(
        [("interior", "Interior"), ("terraza", "Terraza")],
        string="Ubicación",
        default="interior",
        required=True,
    )

    activa = fields.Boolean(string="Activa", default=True)

    # 👇 ESTE CAMPO FALTABA
    ocupada = fields.Boolean(
        string="Ocupada",
        compute="_compute_ocupada",
        store=True
    )

    @api.depends("activa")
    def _compute_ocupada(self):
        for mesa in self:
            pedidos = self.env["cafe.pedido"].search([
                ("mesa_id", "=", mesa.id),
                ("estado", "=", "abierto")
            ])
            mesa.ocupada = bool(pedidos)
