from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import base64
from io import BytesIO
from xlrd import open_workbook

import logging

_logger = logging.getLogger(__name__)

class ProductPricelistWizard(models.TransientModel):
    _name = 'product.pricelist.wizard'
    _description = 'Actualización de precios'

    # pricelist_id = fields.Many2one('product.pricelist',string='Lista de precios')
    excel_file_for_import = fields.Binary("Archivo")

    @api.model
    def default_get(self, field_names):
        defaults = super(
            ProductPricelistWizard, self).default_get(field_names)
        # defaults['pricelist_id'] = self.env.context['active_id']
        return defaults
    
    def do_update(self):
        try:
            inputx = BytesIO()
            inputx.write(base64.decodestring(self.excel_file_for_import))
            book = open_workbook(file_contents=inputx.getvalue())
        except TypeError as e:
            raise UserError(u'ERROR: {}'.format(e))

        sheet = book.sheets()[0]        
        
        modificaciones = 0
        altas = 0
        for i in list(range(sheet.nrows)):
            if i == 0:
                continue
            
            # 0
            default_code = sheet.cell(i, 0).value
            # 1
            descripcion = sheet.cell(i, 1).value
            # 2
            replenishment_base_cost = sheet.cell(i, 2).value
            
            if default_code.strip() == "":
                break            
            
            # import pdb; pdb.set_trace()
            product = self.env['product.template'].search([('default_code','=',default_code.strip())])
            if product:
                # actualizar precio
                product.write({
                    'replenishment_base_cost': replenishment_base_cost,
                })
                # 
                _logger.info("{} actualizado ".format(default_code))
                # import pdb; pdb.set_trace()
            else:
                vals = {
                    'default_code': default_code,
                    'name': descripcion,
                    'replenishment_base_cost': replenishment_base_cost,
                    'standard_price': replenishment_base_cost,
                }
                self.env['product.template'].create(vals)
                # import pdb; pdb.set_trace()
                _logger.info("{} creado ".format(default_code))
                # import pdb; pdb.set_trace()
            if i % 100 == 0:
                _logger.info("{} productos actualizados hasta ACA!".format(i))
        return

    