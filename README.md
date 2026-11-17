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

## Autores

Equipo de Desarrollo — Grupo [Número de Grupo]

Elena Rojas

Samuel Gómez Rendón
