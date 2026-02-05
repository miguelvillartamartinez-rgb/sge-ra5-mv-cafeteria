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

    ocupada = fields.Boolean(string="Ocupada", compute="_compute_ocupada", store=True)

    @api.depends("activa")
    def _compute_ocupada(self):
        # lo calculamos buscando pedidos abiertos por mesa
        Pedido = self.env["cafe.pedido"]
        for mesa in self:
            if not mesa.activa:
                mesa.ocupada = False
                continue
            mesa.ocupada = bool(Pedido.search_count([
                ("mesa_id", "=", mesa.id),
                ("estado", "=", "abierto"),
            ]))
