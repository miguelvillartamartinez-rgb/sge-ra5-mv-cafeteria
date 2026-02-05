from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import _


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

        pedido = super().create(vals)

        pedido.mesa_id._compute_ocupada()

        return pedido


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

        # Guardamos mesas antes del cambio
        mesas_antes = self.mapped("mesa_id")

        for pedido in self:
            if pedido.estado != "abierto" and not only_estado:
                raise UserError("No puedes modificar un pedido que no esté en estado Abierto.")

        res = super().write(vals)

        # Mesas después del cambio
        mesas_despues = self.mapped("mesa_id")

        # Recalcular ocupación de mesas implicadas
        (mesas_antes | mesas_despues)._compute_ocupada()

        return res

    def unlink(self):
        mesas = self.mapped("mesa_id")

        for pedido in self:
            if pedido.estado != "abierto":
                raise UserError("No puedes borrar un pedido que no esté en estado Abierto.")

        res = super().unlink()

        # Recalcular ocupación de las mesas afectadas
        mesas._compute_ocupada()

        return res

    
    @api.constrains("mesa_id", "estado")
    def _check_un_pedido_abierto_por_mesa(self):
        for pedido in self:
            if pedido.estado != "abierto" or not pedido.mesa_id:
                continue
            otros = self.search_count([
                ("id", "!=", pedido.id),
                ("mesa_id", "=", pedido.mesa_id.id),
                ("estado", "=", "abierto"),
            ])
            if otros:
                raise ValidationError(_("Ya existe un pedido abierto para esta mesa."))

    @api.constrains("mesa_id", "estado")
    def _check_mesa_libre(self):
        for pedido in self:
            if pedido.estado != "abierto" or not pedido.mesa_id:
                continue
            otros = self.search_count([
                ("id", "!=", pedido.id),
                ("mesa_id", "=", pedido.mesa_id.id),
                ("estado", "=", "abierto"),
            ])
            if otros:
                raise ValidationError(_("Esa mesa ya tiene un pedido abierto."))
            
    def _recalcular_mesas_ocupadas(self, mesas):
        mesas = mesas.filtered(lambda m: m)  # por si hay None
        if mesas:
            mesas._compute_ocupada()



