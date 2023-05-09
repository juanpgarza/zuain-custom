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

    @api.depends_context('product_id', 'template_id')
    def _compute_price(self):
        super(ProductPricelist,self)._compute_price()
        product_id = self._context.get('product_id', False)
        template_id = self._context.get('template_id', False)
        for rec in self:
            if product_id:
                rec.price_with_tax = self.env['product.product'].browse(product_id).taxes_id.compute_all(price_unit=rec.price)['total_included']
            elif template_id:
                rec.price_with_tax = self.env['product.template'].browse(template_id).taxes_id.compute_all(price_unit=rec.price)['total_included']
            else:
                rec.price_with_tax = 0
                