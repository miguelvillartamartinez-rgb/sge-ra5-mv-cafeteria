from odoo import models, fields

class CafePedidoLinea(models.Model):
    _name = "cafe.pedido.linea"
    _description = "Línea de pedido"

    pedido_id = fields.Many2one(
        "cafe.pedido",
        string="Pedido",
        required=True,
        ondelete="cascade",
    )
    producto_id = fields.Many2one("cafe.producto", string="Producto", required=True)
    cantidad = fields.Integer(string="Cantidad", default=1, required=True)

    precio_unitario = fields.Float(
        string="Precio unitario",
        related="producto_id.precio",
        store=True,
    )
