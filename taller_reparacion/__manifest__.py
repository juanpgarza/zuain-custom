# Copyright 2026 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Taller - Registro de reparaciones",
    "summary": "Órdenes de trabajo de taller vinculadas a vehículos y pedidos de venta",
    "version": "18.0.1.2.0",
    "category": "Sales",
    "website": "https://github.com/juanpgarza/zuain-custom",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "wizard/taller_reparacion_vincular_venta_views.xml",
        "views/taller_vehiculo_views.xml",
        "views/taller_reparacion_views.xml",
        "views/sale_order_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
}
