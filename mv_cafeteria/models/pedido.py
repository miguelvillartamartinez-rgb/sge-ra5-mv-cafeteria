from odoo import models, fields, api

class CafePedido(models.Model):
    _name = "cafe.pedido"
    _description = "Pedido"

    name = fields.Char(string="Referencia", required=True, default="New")
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    mesa_id = fields.Many2one("cafe.mesa", string="Mesa", required=True)

    estado = fields.Selection(
        [("abierto", "Abierto"), ("cobrado", "Cobrado"), ("cancelado", "Cancelado")],
        string="Estado",
        default="abierto",
        required=True,
    )

    linea_ids = fields.One2many("cafe.pedido.linea", "pedido_id", string="Líneas")

    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends("linea_ids.subtotal")
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(pedido.linea_ids.mapped("subtotal"))
