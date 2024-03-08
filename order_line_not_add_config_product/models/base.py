from odoo import models, api

class CustomModel(models.AbstractModel):
    _inherit = 'base' 
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        new_args = args or []
        has_sale_ok_condition = any(arg[0] == 'sale_ok' for arg in new_args if isinstance(arg, list))
        if has_sale_ok_condition:
            new_args.append(('config_ok', '=', False))
            
        return super(CustomModel, self).name_search(name=name, args=new_args, operator=operator, limit=limit)


