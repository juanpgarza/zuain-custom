##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    price_with_tax = fields.Monetary(
        string="Precio Final",
        compute='_compute_price',
        help='Price for product specified on the context',
    )

    # Estoy sobre-escribiendo el método de adhoc
    def _compute_price(self):
        self = self.sudo()
        active_id = model = False
        if 'pricelist_product_id' in self._context:
            active_id = self._context.get('pricelist_product_id')
            model = 'product.product'
        elif 'pricelist_template_id' in self._context:
            active_id = self._context.get('pricelist_template_id')
            model = 'product.template'
        else:
            self.price = 0.0

        if active_id and model:
            for rec in self:
                rec.price = self.env[model].browse(active_id).with_context(pricelist=rec.id)._get_contextual_price()
                product = self.env[model].browse(active_id)
                porc_iva = 1 + product.taxes_id.amount / 100
                rec.price_with_tax = rec.price * porc_iva
                