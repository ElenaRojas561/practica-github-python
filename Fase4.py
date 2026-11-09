"""Software FJ - Sistema Integral. Ejecutar: python main.py"""
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ
import logger
from excepciones import *

def operacion(n, titulo, fn):
    print(f"\n{'='*60}\nOPERACIÓN {n}: {titulo}")
    try: return fn()
    except Exception as e:
        logger.error(f"Op {n} - {titulo}: {type(e).__name__}: {e}")
        print(f"  -> Capturada y controlada: {e} | La app SIGUE funcionando.")
        return None

def main():
    print("="*60); print("  SOFTWARE FJ - Gestión de Clientes, Servicios y Reservas"); print("  Sin BD | POO + Excepciones | Logs en logs/sistema.log"); print("="*60)
    g = GestorSoftwareFJ()
    # 1-3 Clientes válidos
    operacion(1,"Registrar cliente válido (premium)", lambda: g.registrar_cliente(Cliente("C-001","Felipe Jaramillo","felipe@softwarefj.com","3001234567","premium")))
    operacion(2,"Registrar cliente válido (corporativo)", lambda: g.registrar_cliente(Cliente("C-002","Ana María Ruiz","ana@empresa.com","3109876543","corporativo")))
    # 3 Cliente inválido (email)
    operacion(3,"Registrar cliente INVÁLIDO - email malformado", lambda: g.registrar_cliente(Cliente("C-003","Juan","juan-mal","123","regular")))
    # 4 Cliente duplicado
    operacion(4,"Registrar cliente DUPLICADO", lambda: g.registrar_cliente(Cliente("C-001","Otro Nombre","felipe@softwarefj.com","3000000000","regular")))
    # 5-7 Servicios válidos (3 tipos = polimorfismo)
    operacion(5,"Crear Sala", lambda: g.agregar_servicio(ReservaSala("S-001","Sala Innovación",80000,capacidad=20,incluye_video_beam=True)))
    operacion(6,"Crear Alquiler Equipo", lambda: g.agregar_servicio(AlquilerEquipo("E-001","Portátil Gamer",60000,cantidad_stock=5)))
    operacion(7,"Crear Asesoría", lambda: g.agregar_servicio(AsesoriaEspecializada("A-001","Asesoría Python",120000,nivel="experta",consultor="Ing. Felipe")))
    # 8 Servicio inválido (precio negativo)
    operacion(8,"Crear servicio INVÁLIDO - precio negativo", lambda: g.agregar_servicio(ReservaSala("S-999","Sala Mala",-100,capacidad=10)))
    # 9-12 Reservas
    operacion(9,"Reserva EXITOSA sala (con descuento premium + polimorfismo)", lambda: g.crear_reserva("C-001","S-001",duracion=3))
    operacion(10,"Reserva EXITOSA equipo x2 días x2 und.", lambda: g.crear_reserva("C-002","E-001",duracion=2,cantidad=2))
    operacion(11,"Reserva FALLIDA - cliente inexistente", lambda: g.crear_reserva("C-999","S-001",duracion=2))
    operacion(12,"Reserva FALLIDA - stock insuficiente", lambda: g.crear_reserva("C-001","E-001",duracion=1,cantidad=99))
    # 13 Servicio no disponible
    def op13():
        s=g.buscar_servicio("A-001"); s.disponible=False; return g.crear_reserva("C-001","A-001",duracion=2)
    operacion(13,"Reserva FALLIDA - servicio no disponible", op13)
    # 14 Sobrecarga: variantes de cálculo
    def op14():
        s=g.buscar_servicio("S-001")
        print(f"  Base 2h: ${s.calcular_costo(2):,.0f} | +19% impuesto: ${s.calcular_costo_con_impuesto(2):,.0f} | -10% desc: ${s.calcular_costo_con_descuento(2, descuento=0.10):,.0f}")
        try: s.calcular_costo_con_descuento(2, descuento=0.9)
        except CalculoInconsistenteError as e: print(f"  Descuento 90% rechazado correctamente: {e}")
    operacion(14,"Métodos SOBRECARGADOS - costo / impuesto / descuento", op14)
    # 15 Cancelar / operación no permitida
    def op15():
        r=g.reservas[0]; print(f"  Antes: {r.describir()}"); r.cancelar(); print(f"  Cancelada: {r.describir()}")
        try: r.cancelar()
        except OperacionNoPermitidaError as e: print(f"  Doble cancelación bloqueada: {e}")
    operacion(15,"Cancelar reserva + doble cancelación (operación no permitida)", op15)
    # 16 Encadenamiento explícito
    def op16():
        try:
            try: raise DatoInvalidoError("Duración inválida original")
            except DatoInvalidoError as e: raise ReservaInvalidaError("No se pudo crear reserva") from e
        except ReservaInvalidaError as e: print(f"  Encadenamiento: {e} | Causa: {e.__cause__}")
    operacion(16,"Demostrar encadenamiento de excepciones (raise ... from)", op16)
    print("\n"+"="*60); print("RESUMEN FINAL"); g.listar()
    print(f"\nTotal clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    print("Revisa logs/sistema.log para el registro completo."); print("="*60)
if __name__=="__main__": main()

# Compañeros, explico que hice en el Software FJ para que puedas entender y continuar con el proceso:

QUE SI ESTA HECHO:
- main.py ya esta completo con las 16 operaciones que pidio el profe.
- entidades.py (Cliente), servicios.py (Sala, Equipo, Asesoria), gestor.py, excepciones.py y logger.py ya estan creados.
- Funciona: registrar clientes, crear servicios, crear reservas con descuento segun tipo de cliente (premium 15%, corporativo 10%), controlar stock, cancelar reservas y calcular costo / impuesto / descuento.

POR QUE SALEN ERRORES (Y ES NORMAL POR AHORA):
- Las operaciones 3, 4, 8, 11, 12 y 13 salen como "Capturada y controlada" a proposito. Son pruebas de error: email malo, cliente duplicado, precio negativo, cliente que no existe, stock insuficiente y servicio no disponible.
- La app NO se cae, eso es lo que el profe quiere demostrar con try/except. El mensaje "La app SIGUE funcionando" significa que el manejo de excepciones esta bien.
- Si te sale algun otro error raro, es porque falta la otra parte del complemento que todavia no hemos pegado / conectado. No es que el codigo este danado, es que main.py necesita todos los archivos juntos en la misma carpeta para correr. Si falta uno, Python no lo encuentra y marca error.
