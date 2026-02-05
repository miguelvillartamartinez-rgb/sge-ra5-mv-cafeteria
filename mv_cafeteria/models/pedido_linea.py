from odoo import models, fields, api

class CafePedidoLinea(models.Model):
    _name = "cafe.pedido.linea"
    _description = "Línea de pedido"

    pedido_id = fields.Many2one("cafe.pedido", string="Pedido", required=True, ondelete="cascade")
    producto_id = fields.Many2one("cafe.producto", string="Producto", required=True)

    cantidad = fields.Float(string="Cantidad", default=1.0, required=True)
    precio_unitario = fields.Float(string="Precio unitario", compute="_compute_precio_unitario", store=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends("producto_id")
    def _compute_precio_unitario(self):
        for line in self:
            if not line.producto_id:
                line.precio_unitario = 0.0
                continue
            # intenta varios nombres típicos sin romper
            line.precio_unitario = (
                getattr(line.producto_id, "precio", None)
                or getattr(line.producto_id, "pvp", None)
                or getattr(line.producto_id, "precio_venta", None)
                or 0.0
            )

    @api.depends("cantidad", "precio_unitario")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.cantidad or 0.0) * (line.precio_unitario or 0.0)
