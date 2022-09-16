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

    def _display_product_discount_code(self):
        today = fields.Date.today()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product',
            'res_model': 'product.template',
            'domain': [('Date_to', '<=', today),('Date_from', '>=', today) ],
            'view_mode': 'tree,form',
            'target': 'current',
        }
