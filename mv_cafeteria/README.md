# Módulo Cafetería – Odoo 17

Módulo desarrollado para la gestión básica de una cafetería dentro de Odoo 17.  
Permite administrar mesas, productos, alérgenos y pedidos con sus líneas, incluyendo control de estados, cálculos automáticos y vistas visuales tipo kanban.

---

##  Autor
**Miguel Villarta Martínez**
Proyecto del módulo SGE – DAM

---

## Funcionalidades principales

###  Mesas
- Gestión de mesas por ubicación y capacidad.
- Control de mesas activas/inactivas.
- Cálculo automático de mesa ocupada según pedidos abiertos.

### Productos
- Gestión de productos por tipo: bebida, comida y postre.
- Imagen del producto en la ficha.
- Relación con alérgenos (many2many).
- Vista kanban visual con fotografía.

###  Alérgenos
- Registro de alérgenos con código identificativo.
- Integración con productos y líneas de pedido.
- Visualización mediante etiquetas (tags).

###  Pedidos
- Creación automática de referencia mediante secuencia.
- Estados: **abierto, cobrado, cancelado**.
- Botones de acción:
  - Cobrar pedido
  - Cancelar pedido
- Restricciones:
  - Solo un pedido abierto por mesa.
  - No se puede modificar un pedido no abierto.
- Cálculo automático del total.

###  Líneas de pedido
- Selección de producto con precio automático.
- Cálculo de subtotal.
- Visualización de alérgenos del producto.
- Validación de cantidad > 0.

---

## Modelos implementados

- `cafe.mesa`
- `cafe.producto`
- `cafe.alergeno`
- `cafe.pedido`
- `cafe.pedido.linea`

### Relaciones

- Pedido → Líneas (One2many)
- Línea → Producto (Many2one)
- Producto ↔ Alérgenos (Many2many)

---

##  Vistas

- Tree y Form para todos los modelos.
- Kanban para:
  - Productos (con imagen)
  - Alérgenos
- Notebook en pedidos.
- Statusbar para estado del pedido.
- Search views con:
  - Filtros por estado, tipo, alérgeno.
  - Agrupaciones por mesa y estado.

---

## Seguridad

Permisos configurados mediante:

security/ir.model.access.csv

- Usuarios: lectura y edición básica.
- Administradores: control total.

## Datos de demostración

Incluye datos demo:

- Mesas interiores y terraza.
- Productos con precios.
- Alérgenos comunes.
- Pedidos con líneas de ejemplo.

Archivo:

data/demo.xml

## Instalación

1. Copiar el módulo en:

addons/

2. Reiniciar Odoo.

3. Activar modo desarrollador y:
- Actualizar lista de aplicaciones  
- Instalar módulo Cafetería

## Estructura del módulo

mv_cafeteria/
├── models/
├── views/
├── security/
├── data/
├── static/description/icon.png
└── __manifest__.py

## Requisitos cumplidos

- Icono personalizado del módulo.  
- Modelos con relaciones.  
- Vistas kanban y formulario con imagen.  
- Datos demo.  
- Búsquedas y filtros.  
- Lógica de negocio y validaciones.

## Mejoras futuras

- Botón “Abrir pedido” desde mesa.
- Informe ticket PDF.
- Integración con TPV.


