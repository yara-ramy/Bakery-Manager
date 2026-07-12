# from odoo import http


# class MyBakery(http.Controller):
#     @http.route('/my_bakery/my_bakery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_bakery/my_bakery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_bakery.listing', {
#             'root': '/my_bakery/my_bakery',
#             'objects': http.request.env['my_bakery.my_bakery'].search([]),
#         })

#     @http.route('/my_bakery/my_bakery/objects/<model("my_bakery.my_bakery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_bakery.object', {
#             'object': obj
#         })

