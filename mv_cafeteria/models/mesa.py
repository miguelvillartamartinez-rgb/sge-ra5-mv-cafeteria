from odoo import models, fields

class CafeMesa(models.Model):
    _name = "cafe.mesa"
    _description = "Mesa de cafetería"

    name = fields.Char(string="Mesa", required=True)  # Ej: M1, Terraza-2
    capacidad = fields.Integer(string="Capacidad", default=2)
    ubicacion = fields.Selection(
        [("interior", "Interior"), ("terraza", "Terraza")],
        string="Ubicación",
        default="interior",
        required=True,
    )
    activa = fields.Boolean(string="Activa", default=True)
