from odoo import models, fields,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
      print(11111111111111111111111111111)
      domain = ['|', ('name', operator, name), ('description', operator, name)]
      products = self.search(domain + (args or []), limit=limit)
      return products.name_get()