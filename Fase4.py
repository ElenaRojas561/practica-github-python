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

    """Clase abstracta: toda entidad tiene id y debe validarse/describirse."""
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
    """Encapsulación: atributos privados con properties validadas."""
    def __init__(self, id_cliente, nombre, email, telefono, tipo="regular"):
        super().__init__(id_cliente)
        self.nombre = nombre; self.email = email; self.telefono = telefono; self.tipo = tipo
        self.validar()
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, v):
        if not v or len(str(v).strip()) < 3: raise DatoInvalidoError("Nombre debe tener >=3 caracteres.")
        self._nombre = str(v).strip().title()
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
        if len(d) < 7: raise DatoInvalidoError("Teléfono debe tener >=7 dígitos.")
        self._telefono = d
    @property
    def tipo(self): return self._tipo
    @tipo.setter
    def tipo(self, v):
        v = str(v or "regular").lower()
        if v not in ("regular","premium","corporativo"): raise DatoInvalidoError("Tipo debe ser regular/premium/corporativo.")
        self._tipo = v
    def validar(self):
        # Re-valida vía setters
        self.nombre=self._nombre; self.email=self._email; self.telefono=self._telefono; self.tipo=self._tipo
    def describir(self):
        return f"Cliente[{self.id}] {self.nombre} | {self.email} | {self.telefono} | {self.tipo}"
    def descuento_base(self):
        return {"regular":0.0,"premium":0.10,"corporativo":0.15}[self.tipo]

"""Servicio abstracto + 3 servicios especializados. Polimorfismo + sobrecarga simulada."""
from abc import ABC, abstractmethod
from excepciones import *

class Servicio(ABC):
    def __init__(self, codigo, nombre, precio_base, disponible=True):
        if not codigo or not nombre: raise ParametroFaltanteError("Servicio requiere código y nombre.")
        if precio_base is None or precio_base < 0: raise DatoInvalidoError("Precio base no puede ser negativo.")
        self.codigo=str(codigo); self.nombre=nombre; self.precio_base=float(precio_base); self.disponible=bool(disponible)
    @abstractmethod
    def calcular_costo(self, duracion=1, **kwargs) -> float: pass
    @abstractmethod
    def describir(self) -> str: pass
    @abstractmethod
    def validar_parametros(self, duracion, **kwargs): pass
    # --- MÉTODOS SOBRECARGADOS (variantes por parámetros) ---
    def calcular_costo_con_impuesto(self, duracion=1, impuesto=0.19, **kwargs):
        """Variante 1: costo + impuesto."""
        try:
            base = self.calcular_costo(duracion, **kwargs)
            if impuesto < 0: raise CalculoInconsistenteError("Impuesto no puede ser negativo.")
            return round(base*(1+impuesto),2)
        except ErrorSoftwareFJ as e: raise CalculoInconsistenteError(f"Error al calcular con impuesto en {self.codigo}") from e
    def calcular_costo_con_descuento(self, duracion=1, descuento=0.0, impuesto=0.0, **kwargs):
        """Variante 2: costo - descuento + impuesto opcional."""
        try:
            if not 0 <= descuento <= 0.5: raise CalculoInconsistenteError("Descuento debe estar entre 0 y 50%.")
            base = self.calcular_costo(duracion, **kwargs)
            total = base*(1-descuento)*(1+impuesto)
            if total < 0: raise CalculoInconsistenteError("Total calculado negativo.")
            return round(total,2)
        except ErrorSoftwareFJ as e: raise CalculoInconsistenteError("Fallo en cálculo con descuento") from e
    def verificar_disponibilidad(self):
        if not self.disponible: raise ServicioNoDisponibleError(f"Servicio {self.codigo} - {self.nombre} no disponible.")
        return True

class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, precio_base, capacidad, incluye_video_beam=False, **kw):
        super().__init__(codigo,nombre,precio_base,**kw); self.capacidad=capacidad; self.incluye_video_beam=incluye_video_beam; self.validar_parametros(1, capacidad=capacidad)
    def validar_parametros(self, duracion, **kw):
        if duracion is None or duracion<=0: raise ReservaInvalidaError("Duración de sala debe ser >0 horas.")
        cap=kw.get("capacidad", getattr(self,"capacidad",0))
        if cap<=0 or cap>200: raise DatoInvalidoError("Capacidad debe ser 1-200.")
    def calcular_costo(self, duracion=1, **kw):
        self.validar_parametros(duracion, capacidad=self.capacidad)
        extra = 25000 if self.incluye_video_beam else 0
        return round((self.precio_base*duracion)+extra,2)
    def describir(self): return f"Sala[{self.codigo}] {self.nombre} | Cap:{self.capacidad} | Beam:{'Sí' if self.incluye_video_beam else 'No'} | ${self.precio_base:,.0f}/h"

class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, precio_base, cantidad_stock, dias_minimos=1, **kw):
        super().__init__(codigo,nombre,precio_base,**kw); self.cantidad_stock=cantidad_stock; self.dias_minimos=dias_minimos
    def validar_parametros(self, duracion, **kw):
        if duracion<self.dias_minimos: raise ReservaInvalidaError(f"Mínimo {self.dias_minimos} día(s).")
        if kw.get("cantidad",1)>self.cantidad_stock: raise ServicioNoDisponibleError(f"Stock insuficiente: hay {self.cantidad_stock}.")
        if kw.get("cantidad",1)<=0: raise DatoInvalidoError("Cantidad debe ser >0.")
    def calcular_costo(self, duracion=1, **kw):
        cantidad=kw.get("cantidad",1); self.validar_parametros(duracion, cantidad=cantidad)
        return round(self.precio_base*duracion*cantidad,2)
    def describir(self): return f"Equipo[{self.codigo}] {self.nombre} | Stock:{self.cantidad_stock} | ${self.precio_base:,.0f}/día"

class AsesoriaEspecializada(Servicio):
    NIVELES={"basica":1.0,"avanzada":1.5,"experta":2.0}
    def __init__(self, codigo, nombre, precio_base, nivel="basica", consultor="Sin asignar", **kw):
        super().__init__(codigo,nombre,precio_base,**kw); self.nivel=str(nivel).lower(); self.consultor=consultor
        if self.nivel not in self.NIVELES: raise DatoInvalidoError("Nivel: basica/avanzada/experta.")
    def validar_parametros(self, duracion, **kw):
        if duracion<=0 or duracion>8: raise ReservaInvalidaError("Asesoría: duración 1-8 horas por sesión.")
    def calcular_costo(self, duracion=1, **kw):
        self.validar_parametros(duracion)
        return round(self.precio_base*duracion*self.NIVELES[self.nivel],2)
    def describir(self): return f"Asesoría[{self.codigo}] {self.nombre} | Nivel:{self.nivel} | Consultor:{self.consultor} | ${self.precio_base:,.0f}/h base"
