from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import date, datetime


class Product(models.Model):
    _inherit = 'product.template'

    product_warranty = fields.Text(string='Product Warranty Code')
    Date_to = fields.Date(string='Date Start Warranty')
    Date_from = fields.Date(string='Date Stop Warranty')

    @api.onchange("Date_to")
    def onchange_date_to_code(self):
        if self.Date_to and not self.Date_to == '':
            year_date_to = self.Date_to.strftime("%Y")
            date_to_day_month = self.Date_to.strftime("%m%d")
            date_to = date_to_day_month + year_date_to[2:4]
            for rec in self:
                if rec.Date_from and rec.Date_from != '':
                    year_date_from = self.Date_from.strftime("%Y")
                    date_from_day_month = self.Date_from.strftime("%m%d")
                    date_from = date_from_day_month + year_date_from[2:4]
                    rec.product_warranty = "PWR" + "/" + date_to + "/" + date_from
                else:
                    rec.product_warranty = "PWR" + "/" + date_to + "/0"

        else:  # date_to = ''
            if self.Date_from and not self.Date_from == '':
                year_date_from = self.Date_from.strftime("%Y")
                date_from_day_month = self.Date_from.strftime("%m%d")
                date_from = date_from_day_month + year_date_from[2:4]
                self.product_warranty = "PWR" + "/0/" + date_from
            else:
                self.product_warranty = "PWR" + "0/0"

    @api.onchange("Date_from")
    def onchange_date_from_code(self):
        if self.Date_from and not self.Date_from == '':
            year_date_from = self.Date_from.strftime("%Y")
            date_from_day_month = self.Date_from.strftime("%m%d")
            date_from = date_from_day_month + year_date_from[2:4]
            for rec in self:
                if rec.Date_to and rec.Date_to != '':
                    year_date_to = self.Date_to.strftime("%Y")
                    date_to_day_month = self.Date_to.strftime("%m%d")
                    date_to = date_to_day_month + year_date_to[2:4]
                    rec.product_warranty = "PWR" + "/" + date_to + "/" + date_from
                else:
                    rec.product_warranty = "PWR" + "/0/" + date_from

        else:
            if self.Date_to and not self.Date_to == '':
                year_date_to = self.Date_to.strftime("%Y")
                date_to_day_month = self.Date_to.strftime("%m%d")
                date_to = date_to_day_month + year_date_to[2:4]
                self.product_warranty = "PWR" + "/" + date_to + "/0"
            else:
                self.product_warranty = "PWR" + "0/0"

    def write(self, value):
        user_pool = self.env['res.users']
        user = user_pool.browse(self._uid)
        advance_gr = user.has_group('test2.group_adavance_sale')

        if not advance_gr:
            if value.get('Date_to') or value.get('Date_from'):
                raise ValidationError(_("The field Warranty Code only editable by the Advance Sale"))

        else:
            return super(Product, self).write(value)

    @api.constrains('Date_to', 'Date_from')
    def _constrains_reconcile(self):
        for record in self:
            if record.Date_to > record.Date_from:
                raise ValidationError(_("Date Start Warranty must earlier than Date Stop Warranty"))

    def _display_product_discount_code(self):
        today = fields.Date.today()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product',
            'res_model': 'product.template',
            'domain': [('Date_to', '<=', today), ('Date_from', '>=', today)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        combination_info = super(Product, self)._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )


        combination_info['product_warranty'] = self.product_warranty

        return combination_info


