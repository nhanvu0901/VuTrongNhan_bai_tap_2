# -*- coding: utf-8 -*-
# from odoo import http


# class Test1(http.Controller):
#     @http.route('/test1/test1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test1/test1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test1.listing', {
#             'root': '/test1/test1',
#             'objects': http.request.env['test1.test1'].search([]),
#         })

#     @http.route('/test1/test1/objects/<model("test1.test1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test1.object', {
#             'object': obj
#         })
