"""Software FJ - Sistema Integral Interactivo. Ejecutar: python este_archivo.py"""

import logging
import os
import re
from abc import ABC, abstractmethod
from enum import Enum
from excepciones import *

# COnfiguración de logging

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "sistema.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH, level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", encoding="utf-8"
)
logger = logging.getLogger("SoftwareFJ")

def info(msg): logger.info(msg); print(f"[INFO] {msg}")
def error(msg): logger.error(msg); print(f"[ERROR] {msg}")
def advertencia(msg): logger.warning(msg); print(f"[WARN] {msg}")


# Entidades y clases abstractas

class Entidad(ABC):
    def __init__(self, id_entidad):
        if not id_entidad: raise ParametroFaltanteError("El id es obligatorio.")
        self._id = str(id_entidad)
    @property
    def id(self): return self._id
    @abstractmethod
    def validar(self): pass
    @abstractmethod
    def describir(self) -> str: pass
    def __str__(self): return self.describir()

class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, email, telefono, tipo="regular"):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipo = tipo
        self.validar()
    
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, v):
        nombre_formateado = str(v or "").strip()
        if len(nombre_formateado) < 3: raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$", nombre_formateado):
            raise DatoInvalidoError("El nombre solo puede contener letras y espacios.")
        self._nombre = nombre_formateado.title()
    
    @property
    def email(self): return self._email
    @email.setter
    def email(self, v):
        if not v or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str(v)):
            raise DatoInvalidoError(f"Email inválido: {v}")
        self._email = str(v).lower()
    
    @property
    def telefono(self): return self._telefono
    @telefono.setter
    def telefono(self, v):
        d = re.sub(r"\D", "", str(v or ""))
        if len(d) < 7: raise DatoInvalidoError("Teléfono debe tener al menos 7 dígitos.")
        self._telefono = d
    
    @property
    def tipo(self): return self._tipo
    @tipo.setter
    def tipo(self, v):
        v = str(v or "regular").lower()
        if v not in ("regular","premium","corporativo"): 
            raise DatoInvalidoError("El tipo debe ser: regular, premium o corporativo.")
        self._tipo = v
    
    def validar(self):
        self.nombre = self._nombre
        self.email = self._email
        self.telefono = self._telefono
        self.tipo = self._tipo

    def describir(self):
        return f"Cliente[{self.id}] {self.nombre} | {self.email} | {self.telefono} | {self.tipo.capitalize()}"
    
    def descuento_base(self):
        return {"regular": 0.0, "premium": 0.10, "corporativo": 0.15}[self.tipo]

class Servicio(ABC):
    def __init__(self, codigo, nombre, precio_base, disponible=True):
        if not codigo or not nombre: raise ParametroFaltanteError("Servicio requiere código y nombre.")
        if precio_base is None or precio_base < 0: raise DatoInvalidoError("Precio base no puede ser negativo.")
        self.codigo = str(codigo)
        self.nombre = str(nombre)
        self.precio_base = float(precio_base)
        self.disponible = bool(disponible)
    
    @abstractmethod
    def calcular_costo(self, duracion=1, **kwargs) -> float: pass
    @abstractmethod
    def describir(self) -> str: pass
    @abstractmethod
    def validar_parametros(self, duracion, **kwargs): pass

    def calcular_costo_con_impuesto(self, duracion=1, impuesto=0.19, **kwargs):
        try:
            base = self.calcular_costo(duracion, **kwargs)
            if impuesto < 0: raise CalculoInconsistenteError("Impuesto no puede ser negativo.")
            return round(base * (1 + impuesto), 2)
        except ErrorSoftwareFJ as e: 
            raise CalculoInconsistenteError(f"Error al calcular impuesto en {self.codigo}") from e
    
    def calcular_costo_con_descuento(self, duracion=1, descuento=0.0, impuesto=0.0, **kwargs):
        try:
            if not 0 <= descuento <= 0.5: raise CalculoInconsistenteError("Descuento debe estar entre 0 y 50%.")
            base = self.calcular_costo(duracion, **kwargs)
            total = base * (1 - descuento) * (1 + impuesto)
            if total < 0: raise CalculoInconsistenteError("Total calculado negativo.")
            return round(total, 2)
        except ErrorSoftwareFJ as e: 
            raise CalculoInconsistenteError("Fallo en cálculo con descuento") from e
    
    def verificar_disponibilidad(self):
        if not self.disponible: 
            raise ServicioNoDisponibleError(f"Servicio {self.codigo} - {self.nombre} no disponible.")
        return True

class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, precio_base, capacidad, incluye_video_beam=False, **kw):
        super().__init__(codigo, nombre, precio_base, **kw)
        self.capacidad = capacidad
        self.incluye_video_beam = incluye_video_beam
        self.validar_parametros(1, capacidad=capacidad)
    
    def validar_parametros(self, duracion, **kw):
        if duracion is None or duracion <= 0: raise ReservaInvalidaError("Duración de sala debe ser > 0 horas.")
        cap = kw.get("capacidad", getattr(self, "capacidad", 0))
        if cap <= 0 or cap > 200: raise DatoInvalidoError("Capacidad debe ser 1-200.")
    
    def calcular_costo(self, duracion=1, **kw):
        self.validar_parametros(duracion, capacidad=self.capacidad)
        extra = 25000 if self.incluye_video_beam else 0
        return round((self.precio_base * duracion) + extra, 2)
    
    def describir(self): 
        return f"Sala[{self.codigo}] {self.nombre} | Cap:{self.capacidad} | Beam:{'Sí' if self.incluye_video_beam else 'No'} | ${self.precio_base:,.0f}/h"

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, precio_base, cantidad_stock, dias_minimos=1, **kw):
        super().__init__(codigo, nombre, precio_base, **kw)
        self.cantidad_stock = cantidad_stock
        self.dias_minimos = dias_minimos
    
    def validar_parametros(self, duracion, **kw):
        if duracion < self.dias_minimos: raise ReservaInvalidaError(f"Mínimo {self.dias_minimos} día(s).")
        if kw.get("cantidad", 1) > self.cantidad_stock: raise ServicioNoDisponibleError(f"Stock insuficiente: hay {self.cantidad_stock}.")
        if kw.get("cantidad", 1) <= 0: raise DatoInvalidoError("Cantidad debe ser > 0.")
    
    def calcular_costo(self, duracion=1, **kw):
        cantidad = kw.get("cantidad", 1)
        self.validar_parametros(duracion, cantidad=cantidad)
        return round(self.precio_base * duracion * cantidad, 2)
    
    def describir(self): 
        return f"Equipo[{self.codigo}] {self.nombre} | Stock:{self.cantidad_stock} | ${self.precio_base:,.0f}/día"

class AsesoriaEspecializada(Servicio):
    NIVELES = {"basica": 1.0, "avanzada": 1.5, "experta": 2.0}
    
    def __init__(self, codigo, nombre, precio_base, nivel="basica", consultor="Sin asignar", **kw):
        super().__init__(codigo, nombre, precio_base, **kw)
        self.nivel = str(nivel).lower()
        self.consultor = consultor
        if self.nivel not in self.NIVELES: raise DatoInvalidoError("Nivel: basica/avanzada/experta.")
    
    def validar_parametros(self, duracion, **kw):
        if duracion <= 0 or duracion > 8: raise ReservaInvalidaError("Asesoría: duración 1-8 horas por sesión.")
    
    def calcular_costo(self, duracion=1, **kw):
        self.validar_parametros(duracion)
        return round(self.precio_base * duracion * self.NIVELES[self.nivel], 2)
    
    def describir(self): 
        return f"Asesoría[{self.codigo}] {self.nombre} | Nivel:{self.nivel} | Consultor:{self.consultor} | ${self.precio_base:,.0f}/h base"

# ==========================================
# 4. ESTADOS Y GESTIÓN DE RESERVAS
# ==========================================
class EstadoReserva(Enum): 
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"

class Reserva:
    _contador = 0

    def __init__(self, cliente, servicio, duracion, **params):
        if cliente is None or servicio is None: raise ParametroFaltanteError("Reserva requiere cliente y servicio.")
        if duracion is None: raise ParametroFaltanteError("Reserva requiere duración.")
        Reserva._contador += 1
        self.id = f"R-{Reserva._contador:03d}"
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.params = params
        self.estado = EstadoReserva.PENDIENTE
        self.total = None
    
    def procesar(self):
        try:
            self.servicio.verificar_disponibilidad()
            self.servicio.validar_parametros(self.duracion, **self.params)
            self.total = self.servicio.calcular_costo_con_descuento(
                self.duracion, descuento=self.cliente.descuento_base(), **self.params
            )
        except ErrorSoftwareFJ as e:
            self.estado = EstadoReserva.CANCELADA
            raise ReservaInvalidaError(f"Reserva {self.id} falló: {e}") from e
        else:
            self.estado = EstadoReserva.CONFIRMADA
            return self.total
        finally:
            pass 
    
    def confirmar(self):
        if self.estado != EstadoReserva.PENDIENTE: 
            raise OperacionNoPermitidaError(f"No se puede confirmar reserva en estado {self.estado.value}.")
        return self.procesar()
    
    def cancelar(self):
        if self.estado == EstadoReserva.CANCELADA: raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        if self.estado == EstadoReserva.COMPLETADA: raise OperacionNoPermitidaError("No se puede cancelar una reserva completada.")
        self.estado = EstadoReserva.CANCELADA
        return True
    
    def completar(self):
        if self.estado != EstadoReserva.CONFIRMADA: raise OperacionNoPermitidaError("Solo se completa una reserva confirmada.")
        self.estado = EstadoReserva.COMPLETADA 
        return True
    
    def describir(self): 
        return f"{self.id} | {self.cliente.nombre} -> {self.servicio.nombre} | Dur:{self.duracion} | {self.estado.value} | Total:${self.total if self.total is not None else '-'}"

class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        try:
            if any(c.id == cliente.id or c.email == cliente.email for c in self.clientes):
                raise ClienteDuplicadoError(f"Cliente duplicado id/email: {cliente.id}/{cliente.email}")
            self.clientes.append(cliente)
        except ErrorSoftwareFJ as e:
            logger.error(f"Registrar cliente: {e}")
            raise
        else: 
            logger.info(f"Cliente registrado: {cliente.describir()}")
        finally: 
            logger.info("Intento de registro de cliente finalizado.")
        return cliente
    
    def buscar_cliente(self, id_cliente):
        for c in self.clientes:
            if c.id == id_cliente: return c
        raise ClienteNoEncontradoError(f"No existe cliente {id_cliente}")

    def agregar_servicio(self, servicio):
        try:
            if any(s.codigo == servicio.codigo for s in self.servicios): 
                raise DatoInvalidoError(f"Código duplicado {servicio.codigo}")
            self.servicios.append(servicio)
        except ErrorSoftwareFJ as e: 
            logger.error(f"Agregar servicio: {e}")
            raise
        else: 
            logger.info(f"Servicio agregado: {servicio.describir()}")
        return servicio
    
    def buscar_servicio(self, codigo):
        for s in self.servicios:
            if s.codigo == codigo: return s
        raise ServicioNoDisponibleError(f"No existe servicio {codigo}")

    def crear_reserva(self, id_cliente, codigo_servicio, duracion, **params):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(codigo_servicio)
            r = Reserva(cliente, servicio, duracion, **params)
            total = r.procesar()
            self.reservas.append(r)
        except ErrorSoftwareFJ as e:
            logger.error(f"Crear reserva ({id_cliente}/{codigo_servicio}): {e}")
            return None
        else: 
            logger.info(f"Reserva creada: {r.describir()}")
            return r
        finally: 
            logger.info("Intento de reserva finalizado.")

    def listar(self):
        print("\n--- CLIENTES ---")
        [print(" ", c.describir()) for c in self.clientes] or print("  (sin clientes)")
        print("\n--- SERVICIOS ---")
        [print(" ", s.describir()) for s in self.servicios] or print("  (sin servicios)")
        print("\n--- RESERVAS ---")
        [print(" ", r.describir()) for r in self.reservas] or print("  (sin reservas)")

# ==========================================
# 5. INTERFAZ INTERACTIVA (MENÚS DE CONSOLA)
# ==========================================
gestor_global = GestorSoftwareFJ()

# Precargar datos de prueba útiles para que el menú interactivo funcione de inmediato
def precargar_datos_iniciales():
    try:
        gestor_global.registrar_cliente(Cliente("C-001", "Felipe Jaramillo", "felipe@softwarefj.com", "3001234567", "premium"))
        gestor_global.registrar_cliente(Cliente("C-002", "Ana Maria Ruiz", "ana@empresa.com", "3109876543", "corporativo"))
        gestor_global.agregar_servicio(ReservaSala("S-001", "Sala Innovación", 80000, capacidad=20, incluye_video_beam=True))
        gestor_global.agregar_servicio(AlquilerEquipo("E-001", "Portátil Gamer", 60000, cantidad_stock=5))
        gestor_global.agregar_servicio(AsesoriaEspecializada("A-001", "Asesoría Python", 120000, nivel="experta", consultor="Ing. Felipe"))
    except Exception:
        pass

def ejecutar_operacion(titulo, fn):
    print(f"\n{'-'*60}\nEJECUTANDO: {titulo}")
    try:
        resultado = fn()
        print("  -> ¡Operación exitosa!")
        return resultado
    except Exception as e:
        logger.error(f"{titulo}: {type(e).__name__}: {e}")
        print(f"  -> Capturada y controlada: {e} | La app SIGUE funcionando.")
        return None

def mostrar_menu(titulo, opciones, es_principal=False):
    texto_salida = "Salir de la aplicación" if es_principal else "Regresar"
    while True:
        print(f"\n{'='*60}\n{titulo}\n{'='*60}")
        for clave, (descripcion, _) in opciones.items():
            print(f"  {clave}. {descripcion}")
        print(f"  0. {texto_salida}")

        seleccion = input("\nSeleccione una opción: ").strip()
        if seleccion == "0":
            if es_principal:
                print("\nGracias por usar Software FJ. ¡Hasta pronto!")
            break  
        if seleccion in opciones:
            _, accion = opciones[seleccion]
            accion()  
        else:
            print("\n[!] Opción no válida. Intenta nuevamente.")

# Funciones de acciones interactivas para los menús
def ui_registrar_cliente():
    id_c = input("ID del cliente (ej. C-003): ").strip()
    nombre = input("Nombre completo: ").strip()
    email = input("Correo electrónico: ").strip()
    telefono = input("Teléfono (min 7 dígitos): ").strip()
    tipo = input("Tipo (regular / premium / corporativo): ").strip() or "regular"
    
    ejecutar_operacion("Registro de Cliente", lambda: gestor_global.registrar_cliente(Cliente(id_c, nombre, email, telefono, tipo)))

def ui_crear_reserva():
    print("\n--- Listado disponible para reservar ---")
    gestor_global.listar()
    id_c = input("\nID del cliente existente: ").strip()
    id_s = input("Código del servicio a reservar: ").strip()
    try:
        duracion = float(input("Duración (horas/días): ").strip())
    except ValueError:
        print("[!] Duración no válida.")
        return
    
    params = {}
    servicio = next((s for s in gestor_global.servicios if s.codigo == id_s), None)
    if isinstance(servicio, AlquilerEquipo):
        try:
            params["cantidad"] = int(input("Cantidad de equipos a alquilar: ").strip())
        except ValueError:
            params["cantidad"] = 1

    ejecutar_operacion("Creación de Reserva", lambda: gestor_global.crear_reserva(id_c, id_s, duracion, **params))

def menu_clientes():
    opciones = {
        "1": ("Registrar nuevo cliente", ui_registrar_cliente),
        "2": ("Listar todos los registros", lambda: ejecutar_operacion("Listado General", gestor_global.listar)),
    }
    mostrar_menu("GESTIÓN DE CLIENTES", opciones)

def menu_reservas_servicios():
    opciones = {
        "1": ("Crear nueva reserva", ui_crear_reserva),
        "2": ("Ver estado del sistema (Clientes, Servicios y Reservas)", lambda: ejecutar_operacion("Listado del Sistema", gestor_global.listar)),
    }
    mostrar_menu("GESTIÓN DE SERVICIOS Y RESERVAS", opciones)

def main():
    precargar_datos_iniciales()
    menu_principal = {
        "1": ("Gestión de Clientes", menu_clientes),
        "2": ("Gestión de Servicios y Reservas", menu_reservas_servicios),
    }
    mostrar_menu("SOFTWARE FJ - Sistema Integral Interactivo", menu_principal, es_principal=True)

if __name__ == "__main__":
    main()
