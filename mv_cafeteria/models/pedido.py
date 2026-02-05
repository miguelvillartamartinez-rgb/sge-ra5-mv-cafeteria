from odoo import models, fields, api
from odoo.exceptions import UserError

class CafePedido(models.Model):
    _name = "cafe.pedido"
    _description = "Pedido"

    name = fields.Char(string="Referencia", required=True, default="New", copy=False, readonly=True)
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

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("cafe.pedido") or "New"
        return super().create(vals)

    @api.depends("linea_ids.subtotal")
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(pedido.linea_ids.mapped("subtotal"))

    def action_cobrar(self):
        for pedido in self:
            if pedido.estado != "abierto":
                raise UserError("Solo puedes cobrar pedidos en estado Abierto.")
            pedido.estado = "cobrado"

    def action_cancelar(self):
        for pedido in self:
            if pedido.estado == "cobrado":
                raise UserError("No puedes cancelar un pedido ya cobrado.")
            pedido.estado = "cancelado"

    def write(self, vals):
        only_estado = set(vals.keys()) <= {"estado"}

        for pedido in self:
            if pedido.estado != "abierto" and not only_estado:
                raise UserError("No puedes modificar un pedido que no esté en estado Abierto.")
        return super().write(vals)
    
    def unlink(self):
        for pedido in self:
            if pedido.estado != "abierto":
                raise UserError("No puedes borrar un pedido que no esté en estado Abierto.")
        return super().unlink()

        


