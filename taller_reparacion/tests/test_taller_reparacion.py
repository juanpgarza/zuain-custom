from psycopg2 import IntegrityError

from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestTallerReparacion(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cliente = cls.env["res.partner"].create({"name": "Cliente Taller"})
        cls.otro_cliente = cls.env["res.partner"].create({"name": "Otro Cliente"})
        cls.vehiculo = cls.env["taller.vehiculo"].create(
            {"patente": "ab 123 cd", "partner_id": cls.cliente.id}
        )

    def _crear_reparacion(self):
        return self.env["taller.reparacion"].create(
            {"partner_id": self.cliente.id, "vehiculo_id": self.vehiculo.id}
        )

    def test_patente_normalizada_y_unica(self):
        self.assertEqual(self.vehiculo.patente, "AB123CD")
        self.assertEqual(
            self.env["taller.vehiculo"].name_search("ab 123")[0][0], self.vehiculo.id
        )
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["taller.vehiculo"].create({"patente": "AB123CD"})

    def test_autonumeracion(self):
        r1 = self._crear_reparacion()
        r2 = self._crear_reparacion()
        self.assertTrue(r1.name.startswith("OT/"))
        self.assertNotEqual(r1.name, r2.name)
        self.assertEqual(self.vehiculo.reparacion_count, 2)

    def test_vincular_pedido_nuevo(self):
        reparacion = self._crear_reparacion()
        wizard = self.env["taller.reparacion.vincular.venta"].create(
            {"reparacion_id": reparacion.id, "modo": "nuevo"}
        )
        action = wizard.action_confirmar()
        pedido = self.env["sale.order"].browse(action["res_id"])
        self.assertEqual(pedido.partner_id, self.cliente)
        self.assertEqual(pedido.origin, reparacion.name)
        self.assertEqual(reparacion.sale_order_ids, pedido)
        self.assertEqual(pedido.taller_reparacion_ids, reparacion)
        self.assertEqual(pedido.taller_reparacion_count, 1)
        accion = pedido.action_ver_taller_reparaciones()
        self.assertEqual(accion["res_id"], reparacion.id)

    def test_vincular_pedidos_existentes(self):
        reparacion = self._crear_reparacion()
        pedidos = self.env["sale.order"].create(
            [{"partner_id": self.cliente.id}, {"partner_id": self.cliente.id}]
        )
        ajeno = self.env["sale.order"].create({"partner_id": self.otro_cliente.id})
        wizard = self.env["taller.reparacion.vincular.venta"].create(
            {
                "reparacion_id": reparacion.id,
                "modo": "existente",
                "sale_order_ids": [(6, 0, pedidos.ids)],
            }
        )
        # El dominio solo ofrece pedidos del mismo cliente
        ofrecidos = self.env["sale.order"].search(
            [("partner_id", "child_of", self.cliente.id)]
        )
        self.assertNotIn(ajeno, ofrecidos)
        wizard.action_confirmar()
        self.assertEqual(reparacion.sale_order_ids, pedidos)
        self.assertEqual(reparacion.sale_order_count, 2)

    def test_reporte_orden_trabajo(self):
        reparacion = self._crear_reparacion()
        reparacion.notas_reparacion = "<p>Cambio de pastillas de freno</p>"
        html = self.env["ir.actions.report"]._render_qweb_html(
            "taller_reparacion.report_taller_reparacion", reparacion.ids
        )[0].decode()
        self.assertIn(reparacion.name, html)
        self.assertIn("AB123CD", html)
        self.assertIn("Cliente Taller", html)
        self.assertIn("Cambio de pastillas de freno", html)
        self.assertIn("Firma del cliente", html)
