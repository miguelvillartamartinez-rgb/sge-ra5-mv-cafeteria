from odoo import models, fields

class CafePedido(models.Model):
    _name = "cafe.pedido"
    _description = "Pedido"

    name = fields.Char(string="Referencia", required=True)
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    mesa_id = fields.Many2one("cafe.mesa", string="Mesa", required=True)
    estado = fields.Selection(
        [("abierto", "Abierto"), ("cobrado", "Cobrado"), ("cancelado", "Cancelado")],
        string="Estado",
        default="abierto",
        required=True,
    )

    linea_ids = fields.One2many("cafe.pedido.linea", "pedido_id", string="Líneas")

