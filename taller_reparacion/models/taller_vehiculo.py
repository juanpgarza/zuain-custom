from odoo import api, fields, models


class TallerVehiculo(models.Model):
    _name = "taller.vehiculo"
    _description = "Vehículo"
    _rec_name = "patente"
    _order = "patente"

    patente = fields.Char(required=True, index=True)
    marca = fields.Char()
    modelo = fields.Char()
    anio = fields.Integer(string="Año")
    partner_id = fields.Many2one("res.partner", string="Propietario")
    reparacion_ids = fields.One2many(
        "taller.reparacion", "vehiculo_id", string="Reparaciones"
    )
    reparacion_count = fields.Integer(compute="_compute_reparacion_count")

    _sql_constraints = [
        ("patente_uniq", "unique(patente)", "Ya existe un vehículo con esa patente."),
    ]

    @api.depends("reparacion_ids")
    def _compute_reparacion_count(self):
        for rec in self:
            rec.reparacion_count = len(rec.reparacion_ids)

    @api.model
    def _normalizar_patente(self, patente):
        # "ab 123 cd" -> "AB123CD"
        return "".join(patente.split()).upper() if patente else patente

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("patente"):
                vals["patente"] = self._normalizar_patente(vals["patente"])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("patente"):
            vals["patente"] = self._normalizar_patente(vals["patente"])
        return super().write(vals)

    @api.model
    def _search_display_name(self, operator, value):
        # Permite buscar "ab 123" y encontrar "AB123CD"
        if isinstance(value, str):
            value = self._normalizar_patente(value)
        return super()._search_display_name(operator, value)

    def action_ver_reparaciones(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "taller_reparacion.action_taller_reparacion"
        )
        action["domain"] = [("vehiculo_id", "=", self.id)]
        action["context"] = {
            "default_vehiculo_id": self.id,
            "default_partner_id": self.partner_id.id,
        }
        return action
