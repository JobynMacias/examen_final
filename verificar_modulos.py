from odoo.exceptions import ValidationError, UserError, AccessError
from lxml import etree

def rejects(label, error, action):
    try:
        with env.cr.savepoint():
            action()
    except error:
        print('PASS:', label)
    else:
        raise AssertionError(label)

Partner = env['res.partner']
Convenio = env['tienda.convenio']
student = Partner.create({'name': 'QA Estudiante', 'tipo_cliente': 'estudiante', 'numero_cuenta': '0801200012'})
teacher = Partner.create({'name': 'QA Docente', 'tipo_cliente': 'docente'})
for account in ['12345678', '', 'abcdefghij', '0801-2000-18586']:
    rejects('cuenta inválida ' + account, ValidationError, lambda: student.write({'numero_cuenta': account}))
for percent in [0, -1, 50]:
    rejects('porcentaje ' + str(percent), ValidationError, lambda: Convenio.create({'name': 'QA inválido', 'tipo_cliente': 'externo', 'porcentaje': percent}))
rejects('fechas convenio', ValidationError, lambda: Convenio.create({'name': 'QA fechas', 'tipo_cliente': 'externo', 'porcentaje': 10, 'fecha_inicio': '2026-02-02', 'fecha_fin': '2026-01-01'}))
product = env['product.product'].create({'name': 'QA Equipo', 'type': 'consu', 'list_price': 100})
order = env['sale.order'].create({'partner_id': student.id, 'date_order': '2026-11-13 12:00:00', 'order_line': [(0,0,{'display_type': 'line_section', 'name': 'Sección'}), (0,0,{'product_id': product.id, 'product_uom_qty': 2, 'price_unit': 100}), (0,0,{'product_id': product.id, 'product_uom_qty': 3, 'price_unit': 200})]})
assert order.convenio_id == env.ref('tienda_unicah.convenio_estudiantes')
order.action_aplicar_convenio()
lines = order.order_line.filtered(lambda line: not line.display_type)
assert all(line.discount == 15 for line in lines)
assert not order.order_line.filtered('display_type').discount
assert order.monto_ahorro == 120
assert any('15 %' in str(msg.body) for msg in order.message_ids)
lines[0].product_uom_qty = 4
assert order.monto_ahorro == 150
lines[0].price_unit = 200
assert order.monto_ahorro == 210
lines[0].discount = 10
assert order.monto_ahorro == 170
print('PASS: convenio automático, productos, sección, chatter y recálculo del ahorro')
lines[0].product_uom_qty = 9
rejects('límite estudiante 12 unidades', UserError, order.action_confirm)
order.partner_id = teacher
assert order.convenio_id == env.ref('tienda_unicah.convenio_docentes')
order.action_confirm()
assert order.state == 'sale'
rejects('aplicar convenio a venta confirmada', UserError, order.action_aplicar_convenio)
print('PASS: docente confirma 12 unidades con super')
Loan = env['unicah.prestamo']
values = {'name': 'QA préstamo', 'partner_id': teacher.id, 'equipo_id': product.id, 'fecha_inicio': '2026-11-13', 'fecha_fin': '2026-11-15'}
loan = Loan.create(values)
assert loan.dias == 3
loan.action_prestar()
rejects('préstamo superpuesto', ValidationError, lambda: Loan.create(dict(values, state='prestado')))
rejects('fechas préstamo', ValidationError, lambda: Loan.create(dict(values, fecha_fin='2026-11-12')))
loan.action_devolver()
assert loan.state == 'devuelto'
Loan.create(dict(values, state='prestado'))
print('PASS: préstamo, duración, devolución y disponibilidad')
salesperson = env['res.users'].create({'name': 'QA Vendedor', 'login': 'qa_vendedor_unicah', 'group_ids': [(6,0,[env.ref('base.group_user').id, env.ref('sales_team.group_sale_salesman').id])]})
assert Convenio.with_user(salesperson).search_count([]) >= 2
rejects('vendedor no crea convenios', AccessError, lambda: Convenio.with_user(salesperson).create({'name': 'No autorizado', 'tipo_cliente': 'externo', 'porcentaje': 10}))
for model, xmlid, kind in [('res.partner', 'base.view_partner_form', 'form'), ('sale.order', 'sale.view_order_form', 'form'), ('sale.order', 'sale.sale_order_tree', 'list'), ('sale.order', 'sale.view_sales_order_filter', 'search'), ('unicah.prestamo', 'unicah_prestamos.prestamo_form', 'form')]:
    result = env[model].get_view(view_id=env.ref(xmlid).id, view_type=kind)
    etree.fromstring(result['arch'])
print('PASS: permisos y vistas combinadas')
env.cr.rollback()
print('TODAS LAS PRUEBAS CORRECTAS; datos QA revertidos')
