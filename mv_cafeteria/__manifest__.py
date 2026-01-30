# -*- coding: utf-8 -*-
{
    "name": "Cafetería",
    "version": "1.0",
    "summary": "Gestión básica de una cafetería",
    "category": "Services",
    "author": "Miguel",
    "depends": ["base"],
"data": [
    "security/ir.model.access.csv",
    "views/producto_views.xml",
    "views/mesa_views.xml",
    "views/alergeno_views.xml",
    "views/pedido_views.xml",
    "views/menu.xml",
],
"demo": [
    "data/demo.xml",
],
    "installable": True,
    "application": True,
}
