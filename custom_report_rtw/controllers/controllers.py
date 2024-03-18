# from odoo import http
# from odoo.http import request

# class SaleOrderController(http.Controller):
    
#     @http.route('/sale_order/<int:order_id>/print_pdf', type='http', auth='user')
#     def print_sale_order_pdf(self, order_id):
#         order = request.env['sale.order'].browse(order_id)
#         pdf_content = order.generate_pdf_report()
        
#         # Trả về PDF dưới dạng tệp để tải xuống
#         return request.make_response(
#             pdf_content,
#             headers=[
#                 ('Content-Type', 'application/pdf'),
#                 ('Content-Disposition', 'attachment; filename="sale_order_report.pdf"')
#             ]
#         )
