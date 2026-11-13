# Examen II Parcial — Programación de Negocios

**Estudiante:** Jobyn Macias  
**Número de cuenta:** 0801-2000-18586  
**Plataforma:** Odoo 20.0 / PostgreSQL 16 / Docker Compose

## Módulos
- `tienda_unicah`: partes 1 a 5. Contactos universitarios, convenios, descuentos, validaciones y ahorro.
- `unicah_prestamos`: parte 6. Préstamos de equipo con solicitante, equipo, fechas, duración calculada, estados y validación de disponibilidad.

## Instalación
La carpeta examen_final se monta en /mnt/extra-addons. Desde C:\Odoo 20:
```powershell
docker compose exec -T odoo odoo --db_host=db --db_user=odoo --db_password=odoo123 -d Prueba -i tienda_unicah,unicah_prestamos --stop-after-init --no-http --max-cron-threads=0
docker compose restart odoo
```
Para actualizar, use `-u tienda_unicah,unicah_prestamos` en lugar de `-i`.
Active Descuentos en Ajustes > Ventas para mostrar la columna de descuentos.
Convenios: Ventas > Configuración > Convenios UNICAH (responsable de Ventas).
Préstamos: menú UNICAH > Préstamos de equipo.

## Pruebas del examen
Use el estudiante de ejemplo con cuenta 0801200012. El número personal del autor es un dato de entrega y no sustituye la regla de 10 dígitos exigida a los contactos estudiantes del ejercicio.
Compruebe cuentas inválidas, descuentos fuera de (0,40], fechas invertidas, cotizaciones estudiantiles de más de 10 unidades y confirmación de 12 unidades para docentes.
El ahorro suma precio unitario × cantidad × descuento / 100, sin secciones ni notas, antes de impuestos.

## Propuesta de préstamos
Centraliza las entregas y devoluciones de equipo que hoy se registran en hojas de cálculo. Lo usaría el personal de laboratorio o biblioteca. Reutiliza contactos y productos de Odoo y permite consultar el historial desde el contacto.
El modelo unicah.prestamo incluye referencia, solicitante, equipo, fecha inicial/final, días calculados, estado y observaciones. Impide fechas invertidas y préstamos activos del mismo equipo con fechas superpuestas.
Cada producto representa una unidad física identificable. Una segunda versión debe incorporar inventario por número de serie, reservas concurrentes con bloqueo transaccional, recordatorios y permisos por departamento.

## Entrega
Falta publicar el repositorio y preparar el PDF final con capturas reales de las seis partes y las respuestas de JUSTIFICACION.md. No se incluyen contraseñas personales ni copias de base de datos en Git.

## Verificación automatizada
El archivo verificar_modulos.py se ejecuta mediante Odoo shell; crea datos QA dentro de una transacción y los revierte al terminar. No ejecutarlo con Python independiente.

