from odoo import models, fields

class CafeAlergeno(models.Model):
    _name = "cafe.alergeno"
    _description = "Alérgeno"

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código")
    descripcion = fields.Text(string="Descripción")

