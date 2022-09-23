import json

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from datetime import date


class ProductSale(models.Model):
    _inherit = "sale.order.line"

    product_warranty = fields.Text(string='Product Warranty Code', related='product_template_id.product_warranty')
    Sale_order_discount_estimated = fields.Monetary(string='Discount',
                                                    compute='_compute_discount')  # Monetary kieu float co ku tu
    day_under_warranty = fields.Char(string="Time under warranty")

    @api.depends("product_warranty")
    def _compute_discount(self):
        today = date.today()

        for rec in self:
            if rec.product_warranty and not rec.product_warranty == '':
                day_to = int(rec.product_warranty[6:8])
                month_to = int(rec.product_warranty[4:6])
                year_to = int("20" + rec.product_warranty[8:10])
                date_to = date(year_to, month_to, day_to)
                day_from = rec.product_warranty[13:15]
                month_from = rec.product_warranty[11:13]
                year_from = "20" + rec.product_warranty[15:17]
                date_from = date(int(year_from), int(month_from), int(day_from))

                if date_to < today < date_from:
                    rec.Sale_order_discount_estimated = 0
                    day_convert = str(date_from - today)
                    rec.day_under_warranty = day_convert[0:len(day_convert) - 9]
                else:
                    percent = 10
                    rec.Sale_order_discount_estimated = (rec.price_subtotal * percent) / 100
                    rec.day_under_warranty = ''


            else:
                percent = 10
                rec.Sale_order_discount_estimated = (rec.price_subtotal * percent) / 100


class Sale(models.Model):
    _inherit = "sale.order"

    discount_total = fields.Monetary(string='Discount',
                                     compute='_compute_total_discount_payment')  # Monetary kieu float co ku tu

    @api.depends('order_line.Sale_order_discount_estimated')
    def _compute_total_discount_payment(self):
        for rec in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in rec.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += line.Sale_order_discount_estimated
            rec.discount_total = amount_discount
            amount_total = amount_untaxed + amount_tax - amount_discount

            rec.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_total,
            })

