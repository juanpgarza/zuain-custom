from odoo import api, fields, models


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
    taller_reparacion_count = fields.Integer(
        compute="_compute_taller_reparacion_count"
    )

    @api.depends("taller_reparacion_ids")
    def _compute_taller_reparacion_count(self):
        for rec in self:
            rec.taller_reparacion_count = len(rec.taller_reparacion_ids)

    def action_ver_taller_reparaciones(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "taller_reparacion.action_taller_reparacion"
        )
        action["domain"] = [("id", "in", self.taller_reparacion_ids.ids)]
        action["context"] = {"create": False}
        if len(self.taller_reparacion_ids) == 1:
            action["views"] = [(False, "form")]
            action["res_id"] = self.taller_reparacion_ids.id
        return action
