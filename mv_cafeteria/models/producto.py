from odoo import models, fields

class CafeProducto(models.Model):
    _name = "cafe.producto"
    _description = "Producto de cafetería"

    name = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio", required=True)
    descripcion = fields.Text(string="Descripción")
    tipo = fields.Selection(
        [("bebida", "Bebida"), ("comida", "Comida"), ("postre", "Postre")],
        string="Tipo",
        default="bebida",
        required=True,
    )
    activo = fields.Boolean(string="Activo", default=True)

    # Requisito: imagen en un formulario
    image_1920 = fields.Image(string="Imagen")
    alergeno_ids = fields.Many2many("cafe.alergeno", string="Alérgenos")

