from odoo import api, fields, models


class TallerReparacion(models.Model):
    _name = "taller.reparacion"
    _description = "Orden de trabajo de taller"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(
        string="Orden de trabajo",
        required=True,
        readonly=True,
        copy=False,
        default="Nuevo",
    )
    partner_id = fields.Many2one(
        "res.partner", string="Cliente", required=True, tracking=True
    )
    vehiculo_id = fields.Many2one(
        "taller.vehiculo", string="Patente", required=True, tracking=True
    )
    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_proceso", "En proceso"),
            ("terminado", "Terminado"),
            ("entregado", "Entregado"),
            ("cancelado", "Cancelado"),
        ],
        string="Estado",
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )
    fecha_ingreso = fields.Date(default=fields.Date.context_today)
    notas_reparacion = fields.Html(string="Notas de reparación")
    sale_order_ids = fields.Many2many(
        "sale.order",
        "taller_reparacion_sale_order_rel",
        "reparacion_id",
        "sale_order_id",
        string="Pedidos de venta",
        copy=False,
    )
    sale_order_count = fields.Integer(compute="_compute_sale_order_count")
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("taller.reparacion")
                    or "Nuevo"
                )
        return super().create(vals_list)

    @api.onchange("vehiculo_id")
    def _onchange_vehiculo_id(self):
        if self.vehiculo_id.partner_id and not self.partner_id:
            self.partner_id = self.vehiculo_id.partner_id

    def action_en_proceso(self):
        self.write({"state": "en_proceso"})

    def action_terminado(self):
        self.write({"state": "terminado"})

    def action_entregado(self):
        self.write({"state": "entregado"})

    def action_cancelar(self):
        self.write({"state": "cancelado"})

    def action_borrador(self):
        self.write({"state": "borrador"})

    def action_vincular_venta(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Vincular pedido de venta",
            "res_model": "taller.reparacion.vincular.venta",
            "view_mode": "form",
            "target": "new",
            "context": {"default_reparacion_id": self.id},
        }

    def action_ver_pedidos(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale.action_orders"
        )
        action["domain"] = [("id", "in", self.sale_order_ids.ids)]
        action["context"] = {"create": False}
        if len(self.sale_order_ids) == 1:
            action["views"] = [(False, "form")]
            action["res_id"] = self.sale_order_ids.id
        return action
