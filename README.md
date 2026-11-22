# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Aplicación desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) para la gestión operativa de Software FJ, sin el uso de motores de bases de datos externos.
Toda la persistencia operativa se gestiona en memoria mediante estructuras internas y objetos referenciados, complementada con un sistema de auditoría y registro de eventos en archivo plano (logs).

Contexto Académico: Universidad Nacional Abierta y a Distancia (UNAD) — Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI) | Programa: Ingeniería de Sistemas | Curso: Programación (Código: 213023) — Fase 4.

## Características Principales

Gestión de Clientes: Registro, consulta, actualización de información y eliminación lógica/física mediante colecciones internas en memoria, con validación estricta de formato de nombres, correos electrónicos, teléfonos y categorías (regular, premium, corporativo).

Catálogo Polimórfico de Servicios: Administración de tres líneas de negocio especializadas:

Reserva de Salas: Cálculo por horas, capacidad de asistentes y cargos adicionales por equipamiento audiovisual.

Alquiler de Equipos: Cálculo por días/horas, cantidad de unidades y recargos por póliza de seguro.

Asesoría Especializada: Cálculo por horas de consultoría, nivel de experiencia del especialista (junior, senior, arquitecto) y modalidad (remota o presencial).

Ciclo de Vida de Reservas: Integración de instancias de Cliente y Servicio, aplicando descuentos por fidelidad, recargos e impuestos mediante métodos sobrecargados (calcular_costo), control de estados (pendiente, confirmada, cancelada, procesada) y liberación automática de cupos/inventario.

Tolerancia a Fallos y Auditoría: Captura controlada de excepciones personalizadas sin interrumpir la ejecución del programa, registrando cada evento y traza de error en el archivo sistema.log.

## Ejecución y casos de prueba

Requisitos: Python 3.10 o superior. No se requieren librerías externas.

Modo interactivo (menú de consola):

```
python Fase4.py
```

Simulación automática de operaciones (Anexo 3 y feedback del tutor):

```
python simulacion.py
```

El módulo `simulacion.py` ejecuta 15 operaciones completas reutilizando las clases del sistema, entre ellas los dos casos de prueba solicitados por el tutor:

- Caso con datos válidos: registro del cliente `C-101` con nombre, email y teléfono correctos (operación exitosa).
- Caso con entrada incorrecta: registro de un cliente con email sin formato válido; la excepción personalizada `DatoInvalidoError` muestra un mensaje claro y el programa continúa de forma controlada.

Además se prueban: clientes duplicados, servicios con precio negativo, niveles de asesoría inexistentes, reservas con cliente inexistente, stock insuficiente, duración no numérica (encadenamiento `ValueError` → `DatoInvalidoError`), cancelación doble de una reserva (operación no permitida) y el cálculo sobrecargado de costos con impuesto. Todos los eventos y errores quedan registrados en `logs/sistema.log`.

## Autores

Equipo de Desarrollo — Grupo [Número de Grupo]

Elena Rojas

Samuel Gómez Rendón
