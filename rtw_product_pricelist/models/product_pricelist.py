# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from lxml import etree
from odoo.exceptions import UserError, ValidationError


class rtw_product_pricelist(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection([
        ('3_global', 'All Products'),
        ('2_product_category', 'Product Category'),
        ('1_product', 'Product'),
        ('0_product_variant', 'Product Variant'),
        ('4_product_attribute', '属性価格'),
    ],
        "Apply On",
        default='3_global', required=True,
        help='Pricelist Item applicable on selected option')

    product_template_attribute_value_id = fields.Many2one(
        'product.template.attribute.value', string='属性価格', ondelete='cascade'
    )

    @api.onchange('applied_on')
    def _onchange_applied_on(self):
        for item in self:
            if item.applied_on == '4_product_attribute':
                item.compute_price = 'fixed'

    @api.depends('applied_on', 'categ_id', 'product_tmpl_id', 'product_id', 'compute_price', 'fixed_price',
                 'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge', 'product_template_attribute_value_id')
    def _get_pricelist_item_name_price(self):
        res = super(rtw_product_pricelist,
                    self)._get_pricelist_item_name_price()
        for item in self:
            if item.categ_id and item.applied_on == '2_product_category':
                item.name = _("Category: %s") % (item.categ_id.display_name)
            elif item.product_tmpl_id and item.applied_on == '1_product':
                item.name = _("Product: %s") % (
                    item.product_tmpl_id.display_name)
            elif item.product_id and item.applied_on == '0_product_variant':
                item.name = _("Variant: %s") % (item.product_id.with_context(
                    display_default_code=False).display_name)
            elif item.product_template_attribute_value_id and item.applied_on == '4_product_attribute':
                item.name = _("Product Attribute: %s") % (item.product_template_attribute_value_id.attribute_id.name +
                                                          ' : ' + item.product_template_attribute_value_id.product_attribute_value_id.name)
            else:
                item.name = _("All Products")
        return res


class rtw_product_attribute_value(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def get_attribute_value_extra_prices(
        self, product_tmpl_id, pt_attr_value_ids, pricelist=None
    ):
        sale_order_id = None
        pricelist_2 = None
        print('>>>>>>>>>>>>>>>>>> ctx', self.env.context)
        if 'default_order_id' in self.env.context:
            sale_order_id = self.env.context.get('default_order_id')

        sale_order = self.env['sale.order'].search(
            [('id', '=', sale_order_id)])
        sale_order_price_list = sale_order.pricelist_id
        print('>>>>>>>>>>>>>>>>> sale_order_price_list', sale_order_price_list)
        pricelist_items = self.env['product.pricelist.item'].search(
            [('pricelist_id', '=', sale_order_price_list.id), ('applied_on', '=', '4_product_attribute')])
        extra_prices = {}

        if not pricelist:
            pricelist = self.env.user.partner_id.property_product_pricelist
        if sale_order_price_list:
            pricelist_2 = sale_order_price_list
        related_product_av_ids = self.env["product.attribute.value"].search(
            [("id", "in", pt_attr_value_ids.ids), ("product_id", "!=", False)]
        )

        extra_prices = {
            av.id: av.product_id.with_context(pricelist=pricelist.id).price
            for av in related_product_av_ids
        }
        extra_prices_2 = {
            av.product_template_attribute_value_id.product_attribute_value_id.id: av.with_context(
                pricelist=pricelist_2.id).fixed_price
            for av in pricelist_items
        }
        print('>>>>>>>>> pricelist_items', pricelist_items)
        print('>>>>>>>>> extra_prices', extra_prices)
        print('>>>>>>>>> extra_prices_2', extra_prices_2)

        remaining_av_ids = pt_attr_value_ids - related_product_av_ids

        pe_lines = self.env["product.template.attribute.value"].search(
            [
                ("product_attribute_value_id", "in", remaining_av_ids.ids),
                ("product_tmpl_id", "=", product_tmpl_id),
            ]
        )
        for line in pe_lines:
            attr_val_id = line.product_attribute_value_id
            if attr_val_id.id not in extra_prices:
                extra_prices[attr_val_id.id] = 0
            extra_prices[attr_val_id.id] += line.price_extra

        for line in pricelist_items:
            attr_val_id = line.product_template_attribute_value_id.product_attribute_value_id
            if attr_val_id.id in extra_prices:
                extra_prices[attr_val_id.id] = line.fixed_price
        print('>>>>>>> extra_prices', extra_prices)
        return extra_prices


class rtw_product_config_session(models.Model):
    _inherit = 'product.config.session'

    @api.model
    def get_cfg_price(self, value_ids=None, custom_vals=None):
        """Computes the price of the configured product based on the
            configuration passed in via value_ids and custom_values

        :param value_ids: list of attribute value_ids
        :param custom_vals: dictionary of custom attribute values
        :returns: final configuration price"""

        sale_order_id = self.env['product.configurator.sale'].search(
            [('config_session_id', '=', self.id)], limit=1).order_id.id
        sale_order = self.env['sale.order'].search(
            [('id', '=', sale_order_id)])
        sale_order_price_list = sale_order.pricelist_id
        pricelist_items = self.env['product.pricelist.item'].search(
            [('pricelist_id', '=', sale_order_price_list.id), ('applied_on', '=', '4_product_attribute')])

        if sale_order_price_list:
            pricelist_2 = sale_order_price_list

        if value_ids is None:
            value_ids = self.value_ids.ids

        if custom_vals is None:
            custom_vals = {}

        product_tmpl = self.product_tmpl_id
        self = self.with_context(
            {"active_id": product_tmpl.id, "default_order_id": sale_order_id})

        value_ids = self.flatten_val_ids(value_ids)
        price_extra = 0.0
        attr_val_obj = self.env["product.attribute.value"]
        av_ids = attr_val_obj.browse(value_ids)

        extra_prices = attr_val_obj.with_context(
            {"active_id": product_tmpl.id, "default_order_id": sale_order_id}).get_attribute_value_extra_prices(
            product_tmpl_id=product_tmpl.id, pt_attr_value_ids=av_ids
        )
        extra_prices_price_list_variant = {
            av.product_template_attribute_value_id.product_attribute_value_id.id: av.with_context(
                pricelist=pricelist_2.id).fixed_price
            for av in pricelist_items
        }
        for key, value in extra_prices_price_list_variant.items():
            if key in extra_prices:
                extra_prices[key] = value

        price_extra = sum(extra_prices.values())

        return product_tmpl.list_price + price_extra


class rtw_product_configurator_sale_order_line(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        if self.config_session_id:
            price = self.config_session_id.get_cfg_price()
            account_tax_obj = self.env["account.tax"]
            self.price_unit = account_tax_obj._fix_tax_included_price_company(
                price,
                self.product_id.taxes_id,
                self.tax_id,
                self.company_id,
            )
        else:
            super(rtw_product_configurator_sale_order_line,
                  self).product_uom_change()


class rtw_product_configurator(models.TransientModel):
    _inherit = "product.configurator"
    # _inherits = {"product.config.session": "config_session_id"}
    # _description = "Product configuration Wizard"

    @property
    def _prefixes(self):
        """Return a dictionary with all dynamic field prefixes used to generate
        fields in the wizard. Any module extending this functionality should
        override this method to add all extra prefixes"""
        return {
            "field_prefix": "__attribute-",
            "custom_field_prefix": "__custom-",
        }

    @api.model
    def add_dynamic_fields(self, res, dynamic_fields, wiz):
        """Create the configuration view using the dynamically generated
        fields in fields_get()
        """

        field_prefix = self._prefixes.get("field_prefix")
        custom_field_prefix = self._prefixes.get("custom_field_prefix")

        try:
            # Search for view container hook and add dynamic view and fields
            xml_view = etree.fromstring(res["arch"])
            xml_static_form = xml_view.xpath("//group[@name='static_form']")[0]
            xml_dynamic_form = etree.Element(
                "group", colspan="2", name="dynamic_form")
            xml_parent = xml_static_form.getparent()
            xml_parent.insert(xml_parent.index(
                xml_static_form) + 1, xml_dynamic_form)
            xml_dynamic_form = xml_view.xpath(
                "//group[@name='dynamic_form']")[0]
        except Exception:
            raise UserError(
                _("There was a problem rendering the view " "(dynamic_form not found)")
            )

        # Get all dynamic fields inserted via fields_get method
        attr_lines = wiz.product_tmpl_id.attribute_line_ids.sorted()

        # Loop over the dynamic fields and add them to the view one by one
        for attr_line in attr_lines:
            (
                attrs,
                field_name,
                custom_field,
                config_steps,
                cfg_step_ids,
            ) = self.prepare_attrs_initial(
                attr_line, field_prefix, custom_field_prefix, dynamic_fields, wiz
            )

            if len(attrs["readonly"]) > 1 and attrs["readonly"][0] != "|":
                attrs["readonly"].insert(0, "|")
            if len(attrs["invisible"]) > 1 and attrs["invisible"][0] != "|":
                attrs["invisible"].insert(0, "|")
            # Create the new field in the view

            node = etree.Element(
                "field",
                name=field_name,
                on_change="1",
                default_focus="1" if attr_line == attr_lines[0] else "0",
                attrs=str(attrs),
                context=str(
                    {
                        "show_attribute": False,
                        "show_price_extra": True,
                        "active_id": wiz.product_tmpl_id.id,
                        "default_order_id": wiz.order_id.id if 'order_id' in wiz else None
                    }
                ),
                options=str(
                    {
                        "no_create": True,
                        "no_create_edit": True,
                        "no_open": True,
                    }
                ),
            )

            field_type = dynamic_fields[field_name].get("type")
            if field_type == "many2many":
                node.attrib["widget"] = "many2many_tags"
            # Apply the modifiers (attrs) on the newly inserted field in the
            # arch and add it to the view
            self.setup_modifiers(node)
            xml_dynamic_form.append(node)

            if attr_line.custom and custom_field in dynamic_fields:
                widget = ""
                config_session_obj = self.env["product.config.session"]
                custom_option_id = config_session_obj.get_custom_value_id().id

                if field_type == "many2many":
                    field_val = [(6, False, [custom_option_id])]
                else:
                    field_val = custom_option_id

                attrs["readonly"] += [(field_name, "!=", field_val)]
                attrs["invisible"] += [(field_name, "!=", field_val)]
                attrs["required"] += [(field_name, "=", field_val)]

                if config_steps:
                    attrs["required"] += [("state", "in", cfg_step_ids)]

                # TODO: Add a field2widget mapper
                if attr_line.attribute_id.custom_type == "color":
                    widget = "color"

                if len(attrs["invisible"]) > 1 and attrs["invisible"][0] != "|":
                    attrs["invisible"].insert(0, "|")
                if len(attrs["readonly"]) > 1 and attrs["readonly"][0] != "|":
                    attrs["readonly"].insert(0, "|")

                node = etree.Element(
                    "field", name=custom_field, attrs=str(attrs), widget=widget
                )
                self.setup_modifiers(node)
                xml_dynamic_form.append(node)
        return xml_view

    def action_next_step(self):
        """Proceeds to the next step of the configuration process. This usually
        implies the next configuration step (if any) defined via the
        config_step_line_ids on the product.template.

        More importantly it sets metadata on the context
        variable so the fields_get and fields_view_get methods can generate the
        appropriate dynamic content"""
        print('>>>>>>>>>>>> action next step', self)
        wizard_action = self.with_context(
            allow_preset_selection=False,
            default_order_id=self.env.context.get('default_order_id')

        ).get_wizard_action(wizard=self)

        if not self.product_tmpl_id:
            return wizard_action

        if not self.product_tmpl_id.attribute_line_ids:
            raise ValidationError(
                _("Product Template does not have any attribute lines defined")
            )
        next_step = self.config_session_id.get_next_step(
            state=self.state,
            product_tmpl_id=self.product_tmpl_id,
            value_ids=self.config_session_id.value_ids,
            custom_value_ids=self.config_session_id.custom_value_ids,
        )
        if not next_step:
            return self.action_config_done()
        return self.with_context(default_order_id=self.env.context.get('default_order_id')).open_step(step=next_step)

    def open_step(self, step):
        """Open wizard step 'step'
        :param step: recordset of product.config.step.line
        """
        wizard_action = self.with_context(
            allow_preset_selection=False,
            default_order_id=self.env.context.get('default_order_id')
        ).get_wizard_action(wizard=self)
        wizard_action['context'].update(
            {"default_order_id": self.env.context.get('default_order_id')})

        if not step:
            return wizard_action
        if isinstance(step, type(self.env["product.config.step.line"])):
            step = "%s" % (step.id)
        self.state = step
        self.config_session_id.config_step = step
        return wizard_action

    def read(self, fields=None, load="_classic_read"):
        """Remove dynamic fields from the fields list and update the
        returned values with the dynamic data stored in value_ids"""

        field_prefix = self._prefixes.get("field_prefix")
        custom_field_prefix = self._prefixes.get("custom_field_prefix")

        attr_vals = [f for f in fields if f.startswith(field_prefix)]
        custom_attr_vals = [
            f for f in fields if f.startswith(custom_field_prefix)]

        dynamic_fields = attr_vals + custom_attr_vals
        fields = self._remove_dynamic_fields(fields)

        custom_val = self.env["product.config.session"].get_custom_value_id()
        dynamic_vals = {}

        res = super(rtw_product_configurator, self).read(
            fields=fields, load=load)

        if not dynamic_fields:
            return res

        for attr_line in self.product_tmpl_id.attribute_line_ids:
            attr_id = attr_line.attribute_id.id
            field_name = field_prefix + str(attr_id)

            if field_name not in dynamic_fields:
                continue

            custom_field_name = custom_field_prefix + str(attr_id)

            # Handle default values for dynamic fields on Odoo frontend
            res[0].update({field_name: False, custom_field_name: False})

            custom_vals = self.custom_value_ids.filtered(
                lambda x: x.attribute_id.id == attr_id
            ).with_context({"show_attribute": False})
            vals = attr_line.value_ids.filtered(
                lambda v: v in self.value_ids
            ).with_context(
                {
                    "show_attribute": False,
                    "show_price_extra": True,
                    "active_id": self.product_tmpl_id.id,
                    'default_order_id': self.env.context.get('default_order_id')
                }
            )

            if not attr_line.custom and not vals:
                continue

            if attr_line.custom and custom_vals:
                custom_field_val = custom_val.id
                if load == "_classic_read":
                    custom_field_val = custom_val.name_get()[0]
                dynamic_vals.update(
                    {
                        field_name: custom_field_val,
                        custom_field_name: custom_vals.eval(),
                    }
                )
            elif attr_line.multi:
                dynamic_vals = {field_name: vals.ids}
            else:
                try:
                    vals.ensure_one()
                    field_value = vals.id
                    if load == "_classic_read":
                        field_value = vals.name_get()[0]
                    dynamic_vals = {field_name: field_value}
                except Exception:
                    continue
            res[0].update(dynamic_vals)
        return res


class rtw_product_template(models.Model):
    _inherit = "product.template"

    def create_config_wizard(
        self,
        model_name="product.configurator",
        extra_vals=None,
        click_next=True,
    ):
        """create product configuration wizard
        - return action to launch wizard
        - click on next step based on value of click_next"""
        wizard_obj = self.env[model_name]
        wizard_vals = {"product_tmpl_id": self.id}
        if extra_vals:
            wizard_vals.update(extra_vals)
        wizard = wizard_obj.create(wizard_vals)
        if click_next:
            action = wizard.with_context(default_order_id=self.env.context.get(
                'default_order_id')).action_next_step()
        else:
            wizard_obj = wizard_obj.with_context(
                wizard_model=model_name,
                allow_preset_selection=True,
            )
            action = wizard_obj.with_context(default_order_id=self.env.context.get(
                'default_order_id')).get_wizard_action(wizard=wizard)
        return action
