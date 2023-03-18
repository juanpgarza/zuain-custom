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

        categorias = self.env['product.category'].search([])

        try:
            inputx = BytesIO()
            inputx.write(base64.decodestring(self.excel_file_for_import))
            book = open_workbook(file_contents=inputx.getvalue())
        except TypeError as e:
            raise UserError(u'ERROR: {}'.format(e))

        sheet = book.sheets()[0]        

        for i in list(range(sheet.nrows)):
            if i == 0:
                continue
            
            # 0
            # art_id

            # 1
            default_code = sheet.cell(i, 1).value
            # 2            
            descripcion = sheet.cell(i, 2).value
            # 3
            replenishment_base_cost = sheet.cell(i, 3).value
            # 4            
            categ_id = self.get_category(default_code, categorias, sheet.cell(i, 4).value)
            
            # import pdb; pdb.set_trace()

            if type(default_code) is float:
                default_code = str(int(default_code))
            else:
                default_code = default_code.strip()

            # import pdb; pdb.set_trace()

            vals = {
                'default_code': default_code,
                'name': descripcion,
                'replenishment_base_cost': replenishment_base_cost,
                'standard_price': replenishment_base_cost,
                'categ_id': categ_id,
            }
            self.env['product.template'].create(vals)

            if i % 1000 == 0:
                _logger.info("{} productos actualizados hasta ACA!".format(i))

            # if i > 10:
            #     break
        return


    def get_category(self, default_code, categorias, nombre):
        categ_id = categorias.filtered(lambda x: x.name == nombre)
                
        if categ_id:
            categoria = categ_id.id
        else:
            # raise UserError("No existe la categoría: {} - codigo: {}".format(nombre,default_code))
            _logger.info("No existe la categoría: {} - codigo: {}".format(nombre,default_code))
            # le asigno "VARIOS"
            categoria = 1

        return categoria
    