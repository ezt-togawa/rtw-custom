from odoo import _, api, fields, models

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    image = fields.Binary("image")
    child_attribute_ids = fields.One2many(
        comodel_name="product.attribute.value.related.rel",
        inverse_name="parent_attribute_id",
        string="Related Relations"
    )
        
class ProductAttributeValueRel(models.Model):
    _name = "product.attribute.value.related.rel"
    _description = "Product Attribute Value Relation"
    
    parent_attribute_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Parent Attribute",
    )
    child_attribute_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Attribute",
        required=True
    )
    child_attribute = fields.Char(
        string="属性",
        related="child_attribute_id.attribute_id.name",
        store=True
    )
    child_attribute_name = fields.Char(
        string="Name",
        related="child_attribute_id.name",
        store=True
    )
    image = fields.Binary("Image")
            
    @api.onchange('child_attribute_id','child_attribute_id.attribute_id.name','child_attribute_id.name')
    def _onchange_child_attribute_id(self):
        for record in self:
            if record.child_attribute_id:
                record.child_attribute = record.child_attribute_id.attribute_id.name if record.child_attribute_id.attribute_id.name else ''
                record.child_attribute_name = record.child_attribute_id.name if record.child_attribute_id.name else ''
                
    _sql_constraints = [
        ('unique_parent_child_pair', 'UNIQUE(parent_attribute_id, child_attribute_id)', '親属性には同じ子属性を２重に追加できません'),
        ('check_child_is_parent', 'CHECK(parent_attribute_id != child_attribute_id)', '子属性は親属性と異なる必要があります')
    ]