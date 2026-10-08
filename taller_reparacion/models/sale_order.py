from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    taller_reparacion_ids = fields.Many2many(
        "taller.reparacion",
        "taller_reparacion_sale_order_rel",
        "sale_order_id",
        "reparacion_id",
        string="Órdenes de trabajo",
        copy=False,
    )
