from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CafePedido(models.Model):
    _name = "cafe.pedido"
    _description = "Pedido"
    _order = "fecha desc, id desc"

    name = fields.Char(
        string="Referencia",
        required=True,
        default="New",
        copy=False,
        readonly=True
    )
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    mesa_id = fields.Many2one("cafe.mesa", string="Mesa", required=True)

    estado = fields.Selection(
        [("abierto", "Abierto"), ("cobrado", "Cobrado"), ("cancelado", "Cancelado")],
        string="Estado",
        default="abierto",
        required=True,
        tracking=True,
    )

    linea_ids = fields.One2many("cafe.pedido.linea", "pedido_id", string="Líneas")
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    # -------------------------
    # CREATE / COMPUTES
    # -------------------------
    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("cafe.pedido") or "New"

        pedido = super().create(vals)

        # Recalcular ocupación de la mesa (si tu mesa tiene 'ocupada' y _compute_ocupada)
        if pedido.mesa_id:
            pedido.mesa_id._compute_ocupada()

        return pedido

    @api.depends("linea_ids.subtotal")
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(pedido.linea_ids.mapped("subtotal"))

    # -------------------------
    # BUTTONS
    # -------------------------
    def action_cobrar(self):
        for pedido in self:
            if pedido.estado != "abierto":
                raise UserError(_("Solo puedes cobrar pedidos en estado Abierto."))
            pedido.estado = "cobrado"

        # Recalcular ocupación mesas implicadas
        self.mapped("mesa_id")._compute_ocupada()

    def action_cancelar(self):
        for pedido in self:
            if pedido.estado == "cobrado":
                raise UserError(_("No puedes cancelar un pedido ya cobrado."))
            pedido.estado = "cancelado"

        # Recalcular ocupación mesas implicadas
        self.mapped("mesa_id")._compute_ocupada()

    # -------------------------
    # WRITE / UNLINK (bloqueos)
    # -------------------------
    def write(self, vals):
        only_estado = set(vals.keys()) <= {"estado"}

        mesas_antes = self.mapped("mesa_id")

        for pedido in self:
            if pedido.estado != "abierto" and not only_estado:
                raise UserError(_("No puedes modificar un pedido que no esté en estado Abierto."))

        res = super().write(vals)

        mesas_despues = self.mapped("mesa_id")
        (mesas_antes | mesas_despues).filtered(lambda m: m)._compute_ocupada()

        return res

    def unlink(self):
        mesas = self.mapped("mesa_id")

        for pedido in self:
            if pedido.estado != "abierto":
                raise UserError(_("No puedes borrar un pedido que no esté en estado Abierto."))

        res = super().unlink()

        mesas.filtered(lambda m: m)._compute_ocupada()
        return res

    # -------------------------
    # CONSTRAINTS
    # -------------------------
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



