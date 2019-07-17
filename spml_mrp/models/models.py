# # -*- coding: utf-8 -*-
#
from odoo import models, fields, api ,_
# from odoo.addons import decimal_precision as dp
# from odoo.exceptions import UserError, ValidationError
# from odoo.tools import float_round

from itertools import groupby, filterfalse


#
class MrpBom(models.Model):

     _inherit =  'mrp.bom'

     comp_total = fields.Float(string="BOM Total" ,compute="_calc_comp_total")
     bom_extra_line_ids = fields.One2many('mrp.bom.extra', 'bom_id', 'BoM Extra', copy=True)

     @api.multi
     def _calc_comp_total(self):
         if self.bom_line_ids :
             for rec in  self.bom_line_ids:
                 self.comp_total +=rec.Total




#
#     @api.multi
#     def _compute_bom_cost(self):
#         for bom in self:
#             totale_cost = 0.0
#             # for bom_line in bom.bom_line_ids:
#             #     if bom_line.related_bom_ids:
#             #         for sub_bom in bom_line.related_bom_ids:
#             #             if bom.type in [sub_bom.type, 'phantom']:
#             #                 if sub_bom:
#             #                     totale_cost = totale_cost + sub_bom.standard_price * bom_line.product_qty
#             #                     break
#             #     else:
#             #         totale_cost = totale_cost + bom_line.product_id.standard_price * bom_line.product_qty
#             # bom.standard_price = totale_cost
#
#     standard_price = fields.Float(compute=_compute_bom_cost)
#
#

# class MRPBom_in (models.Model):
#     _inherit ='mrp.bom'
#     bom_line_ids = fields.One2many('mrp.bom.extra', 'bom_id', 'BoM Extra', copy=True)
#

class MRPBomExtra (models.Model):
    _name='mrp.bom.extra'


    name=fields.Char(string="Name")
    quantity=fields.Float(string="Quantity")
    actual_cost=fields.Float(string="Actual Cost")
    total=fields.Float("Total",compute="_calc_total")
    extra_total =fields.Float("Extra Total")



    bom_id = fields.Many2one(
        'mrp.bom', 'Parent BoM',
        index=True, ondelete='cascade', required=True)
    # product_id = fields.Many2one(
    #     'product.product', 'Component', required=True)
    # product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id',
    #                                   readonly=False)
    # sequence = fields.Integer(
    #     'Sequence', default=1,
    #     help="Gives the sequence order when displaying.")


    @api.depends('actual_cost', 'quantity')
    def _calc_total(self):
        self.extra_total = 0.0
        if self:
            for rec in self:

                self.extra_total += rec.quantity * rec.actual_cost
                rec.total = rec.quantity * rec.actual_cost


        print(self.extra_total)



class MrpBomLine(models.Model):
#
    _inherit = 'mrp.bom.line'
    product_cost=fields.Float(related='product_id.standard_price',store=True)
    actual_cost=fields.Float(string="Actual Cost",default=0)

    Total=fields.Float(string="Total",compute="_calc_total")


    @api.depends ('product_id','actual_cost','product_qty')
    def _calc_total(self):
        self.comp_total=0.0
        if self:
            for rec in self:
                    if  rec.actual_cost ==0 :
                        rec.actual_cost = rec.product_cost

                    self.comp_total += rec.product_qty * rec.actual_cost
                    rec.Total = rec.product_qty * rec.actual_cost
        print(self.comp_total)

#     @api.depends ('product_id')
#     def _calc_total(self):
#
#         if self:
#             for rec in self:
#                 if  rec.actual_cost !=  rec.product_cost and  rec.actual_cost !=0:
#                     rec.actual_cost= rec.product_cost
#
# #
#     @api.multi
#     def _compute_bom_cost(self):
#         for bom_line in self:
#             totale_cost = 0.0
#         #     cost_found = False
#         #     if bom_line.related_bom_ids:
#         #         for sub_bom in bom_line.related_bom_ids:
#         #             if bom_line.bom_id.type == sub_bom.type:
#         #                 if sub_bom:
#         #                     bom_line.standard_price = totale_cost + sub_bom.standard_price
#         #                     cost_found = True
#         #                     break
#         #     if not cost_found:
#         #         bom_line.standard_price = bom_line.product_id.standard_price
#
#     standard_price = fields.Float(compute=_compute_bom_cost)
