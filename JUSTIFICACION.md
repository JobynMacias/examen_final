# Respuestas y justificación — Examen II Parcial

Jobyn Macias — 0801-2000-18586

## Parte 1
Se amplía res.partner y su formulario con la pestaña UNICAH. Número de cuenta y carrera aparecen solo para estudiantes. La cuenta del contacto de prueba es 0801200012, conforme al enunciado.

## Parte 2
_name identifica un modelo nuevo con su propia estructura; _inherit sin _name amplía un modelo existente. tienda.convenio necesita permisos porque es un modelo nuevo. res.partner conserva los permisos que ya define Odoo. El vendedor tiene lectura y el responsable de Ventas tiene creación, lectura, modificación y eliminación.

## Parte 3
store=True guarda el convenio calculado en la base y permite buscar y agrupar por él. readonly=False permite cambiar manualmente la propuesta. Al cambiar las dependencias, el cálculo puede sustituir la selección manual. Se excluye display_type porque secciones y notas no son líneas de producto y no deben recibir descuentos.

## Parte 4
required en XML protege la interacción con ese formulario, pero no valida longitud ni contenido y no basta para importaciones o llamadas externas. La restricción Python controla que los estudiantes tengan exactamente 10 dígitos. super().action_confirm() ejecuta la confirmación estándar y las extensiones instaladas; omitirlo impediría completar ese flujo de Odoo.

## Parte 5
Las dependencias son order_line.price_unit, order_line.product_uom_qty, order_line.discount y order_line.display_type. El cálculo suma precio unitario por cantidad por descuento dividido entre 100 de líneas de producto. Si falta una dependencia, una modificación de ese dato podría dejar el valor almacenado desactualizado. El resultado es ahorro antes de impuestos.

## Parte 6: préstamos de equipo
Problema: las entregas de equipo en hojas de cálculo dificultan conocer disponibilidad, responsables y fechas. Lo usaría el personal de laboratorio o biblioteca.

Odoo permite reutilizar contactos y productos, registrar la operación en una base central y consultar los préstamos desde cada contacto.

Diseño: unicah.prestamo tiene referencia, solicitante Many2one a res.partner, equipo Many2one a product.product, fechas inicial/final, duración calculada almacenada, estado y observaciones. Cada producto debe representar una unidad física. Se amplía res.partner con sus préstamos y una pestaña de historial. Las reglas impiden fechas invertidas y préstamos activos superpuestos para el mismo equipo.

Segunda versión: números de serie, recordatorios, permisos por departamento y bloqueo transaccional de reservas simultáneas. La validación actual cubre operaciones sucesivas; no garantiza exclusión ante transacciones concurrentes.

## Evidencia pendiente
Estas respuestas son material para la entrega. Añadir capturas reales: pestaña UNICAH; convenios; cotización con descuento y chatter; errores de validación; lista con ahorro/filtro/agrupación; préstamo y su historial en el contacto. No se han generado ni simulado capturas.
