from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CafePedidoLinea(models.Model):
    _name = "cafe.pedido.linea"
    _description = "Línea de pedido"
    _order = "id asc"

    pedido_id = fields.Many2one("cafe.pedido", string="Pedido", required=True, ondelete="cascade")
    producto_id = fields.Many2one("cafe.producto", string="Producto", required=True)

    cantidad = fields.Float(string="Cantidad", default=1.0, required=True)
    precio_unitario = fields.Float(string="Precio unitario", compute="_compute_precio_unitario", store=True, readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True, readonly=True)

    alergeno_ids = fields.Many2many(
        related="producto_id.alergeno_ids",
        string="Alérgenos",
        readonly=True
    )

    @api.depends("producto_id")
    def _compute_precio_unitario(self):
        for line in self:
            if not line.producto_id:
                line.precio_unitario = 0.0
                continue
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

    @api.constrains("cantidad")
    def _check_cantidad(self):
        for line in self:
            if line.cantidad <= 0:
                raise ValidationError(_("La cantidad debe ser mayor que 0."))
