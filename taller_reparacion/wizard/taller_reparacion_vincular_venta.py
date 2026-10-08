from odoo import fields, models


class TallerReparacionVincularVenta(models.TransientModel):
    _name = "taller.reparacion.vincular.venta"
    _description = "Vincular orden de trabajo con pedidos de venta"

    reparacion_id = fields.Many2one("taller.reparacion", required=True)
    partner_id = fields.Many2one(related="reparacion_id.partner_id")
    modo = fields.Selection(
        [
            ("nuevo", "Crear un pedido de venta nuevo"),
            ("existente", "Vincular pedidos existentes del cliente"),
        ],
        required=True,
        default="nuevo",
    )
    sale_order_ids = fields.Many2many(
        "sale.order",
        string="Pedidos del cliente",
        domain="[('partner_id', 'child_of', partner_id), "
        "('state', '!=', 'cancel'), ('id', 'not in', ya_vinculados_ids)]",
    )
    ya_vinculados_ids = fields.Many2many(
        related="reparacion_id.sale_order_ids", string="Ya vinculados"
    )

    def action_confirmar(self):
        self.ensure_one()
        reparacion = self.reparacion_id
        if self.modo == "nuevo":
            pedido = self.env["sale.order"].create(
                {
                    "partner_id": reparacion.partner_id.id,
                    "origin": reparacion.name,
                    "company_id": reparacion.company_id.id,
                }
            )
            reparacion.sale_order_ids = [fields.Command.link(pedido.id)]
            return {
                "type": "ir.actions.act_window",
                "res_model": "sale.order",
                "res_id": pedido.id,
                "view_mode": "form",
                "target": "current",
            }
        reparacion.sale_order_ids = [
            fields.Command.link(so.id) for so in self.sale_order_ids
        ]
        return {"type": "ir.actions.act_window_close"}
