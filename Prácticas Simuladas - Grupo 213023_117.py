"""Software FJ - Simulación de operaciones del sistema (Fase 4).

En este módulo realizo las pruebas del programa de forma automática:
ejecuto 15 operaciones completas, combinando casos con datos válidos y
casos con entradas incorrectas, para comprobar que el manejo de
excepciones muestra un mensaje claro ante cada error y que el programa
continúa funcionando de forma controlada, sin interrumpirse.

Reutilizo las clases ya definidas en Fase4.py y excepciones.py.

Ejecutar con:  python simulacion.py
Los eventos y errores quedan registrados en logs/sistema.log
"""

# Importo las clases del sistema y el logger definidos en Fase4.py
from Fase4 import (
    GestorSoftwareFJ,
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    logger,
)
from excepciones import ErrorSoftwareFJ, DatoInvalidoError

# Contadores para el resumen final de la simulación.
RESULTADOS = {"exitosas": 0, "controladas": 0}


def ejecutar_paso(numero, titulo, funcion):
    """Ejecuta una operación de la simulación con manejo robusto de errores.

    Aquí aplico la estructura try/except/else/finally:
    - try: intenta la operación.
    - except: captura la excepción, muestra un mensaje claro y registra
      el error en el log SIN detener el programa (continuación controlada).
    - else: se ejecuta solo si NO hubo error (operación exitosa).
    - finally: se ejecuta siempre, confirmando que la app sigue activa.
    """
    print(f"\n[{numero:02d}] {titulo}")
    try:
        resultado = funcion()
    except ErrorSoftwareFJ as e:
        # Excepción personalizada del sistema: error esperado y controlado.
        RESULTADOS["controladas"] += 1
        logger.error(f"Simulación paso {numero}: {type(e).__name__}: {e}")
        print(f"     -> [CONTROLADO] {type(e).__name__}: {e}")
        # Si la excepción fue encadenada, muestro también la causa original.
        if e.__cause__ is not None:
            print(f"        Causa original: {type(e.__cause__).__name__}: {e.__cause__}")
    except Exception as e:
        # Red de seguridad para cualquier error no previsto: la app no se cae.
        RESULTADOS["controladas"] += 1
        logger.error(f"Simulación paso {numero} (no previsto): {type(e).__name__}: {e}")
        print(f"     -> [CONTROLADO/NO PREVISTO] {type(e).__name__}: {e}")
    else:
        RESULTADOS["exitosas"] += 1
        print(f"     -> [OK] Resultado: {resultado}")
    finally:
        print("     ... la aplicación continúa funcionando.")


def leer_duracion_simulada(entrada_usuario):
    """Simula la lectura de una duración digitada por el usuario.

    Si la entrada no es numérica (p. ej. 'tres'), encadeno el ValueError
    nativo a una excepción personalizada usando raise ... from ..., para
    conservar la causa original del error.
    """
    try:
        return float(entrada_usuario)
    except ValueError as e:
        raise DatoInvalidoError(
            f"La duración digitada no es un número válido: '{entrada_usuario}'"
        ) from e


def main():
    print("=" * 70)
    print("SOFTWARE FJ - SIMULACIÓN DE OPERACIONES (Fase 4)")
    print("Casos válidos e inválidos con manejo controlado de excepciones")
    print("=" * 70)

    # Creo un gestor propio para la simulación, independiente del menú interactivo.
    gestor = GestorSoftwareFJ()

    # 1. Registro de un cliente con todos sus datos correctos.
    ejecutar_paso(1, "Registrar cliente con datos válidos",
                  lambda: gestor.registrar_cliente(
                      Cliente("C-101", "Laura Martinez", "laura.martinez@mail.com", "3011234567", "premium")))

    # 2. Registro con un email mal escrito: debe mostrarse un mensaje claro
    #    y el programa debe continuar de forma controlada.
    ejecutar_paso(2, "Registrar cliente con email incorrecto",
                  lambda: gestor.registrar_cliente(
                      Cliente("C-102", "Pedro Gomez", "correo-sin-arroba", "3020000000")))

    # 3. Registro con nombre demasiado corto.
    ejecutar_paso(3, "Registrar cliente con nombre inválido (menos de 3 letras)",
                  lambda: gestor.registrar_cliente(
                      Cliente("C-103", "Al", "al@mail.com", "3115551234")))

    # 4. Otro cliente válido, esta vez de tipo corporativo.
    ejecutar_paso(4, "Registrar segundo cliente válido (corporativo)",
                  lambda: gestor.registrar_cliente(
                      Cliente("C-104", "Carlos Perez", "carlos.perez@empresa.com", "3129876543", "corporativo")))

    # 5. Intento de registrar un cliente con un email ya usado.
    ejecutar_paso(5, "Registrar cliente duplicado (mismo email)",
                  lambda: gestor.registrar_cliente(
                      Cliente("C-105", "Laura Clon", "laura.martinez@mail.com", "3000000000")))

    # 6. Creación de un servicio de sala con datos correctos.
    ejecutar_paso(6, "Crear servicio válido: Sala de Juntas",
                  lambda: gestor.agregar_servicio(
                      ReservaSala("S-101", "Sala de Juntas", 90000, capacidad=15, incluye_video_beam=True)).describir())

    # 7. Creación de un servicio con precio negativo (no permitido).
    ejecutar_paso(7, "Crear servicio inválido (precio base negativo)",
                  lambda: gestor.agregar_servicio(
                      ReservaSala("S-102", "Sala Fantasma", -5000, capacidad=10)))

    # 8. Alquiler de equipos con stock limitado a 2 unidades.
    ejecutar_paso(8, "Crear servicio válido: Alquiler de Videobeam (stock 2)",
                  lambda: gestor.agregar_servicio(
                      AlquilerEquipo("E-101", "Videobeam Epson", 45000, cantidad_stock=2)).describir())

    # 9. Asesoría con un nivel que no existe en el catálogo.
    ejecutar_paso(9, "Crear asesoría con nivel inválido ('maestro')",
                  lambda: gestor.agregar_servicio(
                      AsesoriaEspecializada("A-101", "Asesoría POO", 100000, nivel="maestro")))

    # 10. Reserva exitosa: la clienta premium reserva la sala por 3 horas
    #     (crear_reserva controla los errores internamente y devuelve None si falla).
    ejecutar_paso(10, "Crear reserva válida (C-101 reserva Sala de Juntas, 3 horas)",
                  lambda: gestor.crear_reserva("C-101", "S-101", 3).describir())

    # 11. Reserva con un cliente que no está registrado.
    ejecutar_paso(11, "Crear reserva con cliente inexistente (C-999)",
                  lambda: gestor.crear_reserva("C-999", "S-101", 2) or "None (reserva rechazada y registrada en el log)")

    # 12. Reserva pidiendo más equipos de los que hay en stock.
    ejecutar_paso(12, "Crear reserva con stock insuficiente (5 videobeams, hay 2)",
                  lambda: gestor.crear_reserva("C-104", "E-101", 2, cantidad=5) or "None (reserva rechazada y registrada en el log)")

    # 13. Cálculo del costo usando la variante sobrecargada con impuesto.
    ejecutar_paso(13, "Calcular costo de la sala con impuesto del 19% (método sobrecargado)",
                  lambda: gestor.buscar_servicio("S-101").calcular_costo_con_impuesto(3, impuesto=0.19))

    # 14. Entrada no numérica del usuario: demuestra el encadenamiento
    #     ValueError -> DatoInvalidoError.
    ejecutar_paso(14, "Simular duración digitada no numérica ('tres horas')",
                  lambda: leer_duracion_simulada("tres horas"))

    # 15. Intento de cancelar dos veces la misma reserva.
    def cancelar_dos_veces():
        reserva = gestor.reservas[0]      # la reserva confirmada del paso 10
        reserva.cancelar()                # primera cancelación: permitida
        reserva.cancelar()                # segunda: OperacionNoPermitidaError
    ejecutar_paso(15, "Cancelar la misma reserva dos veces (operación no permitida)",
                  cancelar_dos_veces)

    # Resumen final y estado del sistema.
    print("\n" + "=" * 70)
    print("RESUMEN DE LA SIMULACIÓN")
    print(f"  Operaciones exitosas:              {RESULTADOS['exitosas']}")
    print(f"  Errores capturados y controlados:  {RESULTADOS['controladas']}")
    print(f"  Total de operaciones ejecutadas:   {RESULTADOS['exitosas'] + RESULTADOS['controladas']}")
    print("  El programa terminó SIN interrupciones: manejo de excepciones OK.")
    print("  Revise logs/sistema.log para la trazabilidad completa.")
    gestor.listar()


if __name__ == "__main__":
    main()
