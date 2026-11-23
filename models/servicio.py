"""Modulo: servicio.py
Descripcion: Contiene la clase abstracta Servicio y las tres implementaciones
especializadas de Software FJ (ReservaSala, AlquilerEquipo, AsesoriaEspecializada),
aplicando herencia, polimorfismo y sobrecarga en el calculo de costos."""

from abc import abstractmethod
from models.entidad import EntidadSistema
from exceptions.errores import (
    DatosInvalidosError,
    ParametrosFaltantesError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(EntidadSistema):
    """Clase abstracta que modela un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametrosFaltantesError("El nombre del servicio es obligatorio.")
        if tarifa_base is None or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base del servicio debe ser mayor a cero.")

        self._nombre_servicio = nombre_servicio.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        """Valida que la duracion y disponibilidad sean aptas para este tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Metodo polimorfico y sobrecargado (via parametros opcionales) para calcular
        el costo total segun horas, porcentaje de impuesto (IVA 19% por defecto) y descuento.
        """
        pass

    def _aplicar_ajustes_financieros(self, subtotal: float, impuesto: float, descuento: float) -> float:
        """Valida consistencia financiera y aplica descuentos e impuestos al subtotal."""
        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError(f"Porcentaje de impuesto invalido: {impuesto}.")
        if descuento < 0 or descuento >= subtotal:
            raise CalculoInconsistenteError(
                f"El descuento ({descuento}) no puede ser negativo ni mayor o igual al subtotal ({subtotal})."
            )
        base_gravable = subtotal - descuento
        total = base_gravable * (1 + impuesto)
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitacion."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, capacidad_personas: int, disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        if capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0 personas.")
        self.capacidad_personas = capacidad_personas

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre_servicio}' no se encuentra disponible.")
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas.")

    def calcular_costo(self, duracion_horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        self.validar_parametros_operacion(duracion_horas)
        # Si supera 4 horas, aplica un recargo fijo por limpieza de 15.000 COP
        recargo_limpieza = 15000.0 if duracion_horas > 4 else 0.0
        subtotal = (self.tarifa_base * duracion_horas) + recargo_limpieza
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.id_entidad}]: {self.nombre_servicio} (Cap: {self.capacidad_personas} pers.) - ${self.tarifa_base}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnologicos de alto rendimiento."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, tipo_equipo: str, disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ParametrosFaltantesError("Debe especificar el tipo de equipo tecnologico.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre_servicio}' ({self.tipo_equipo}) esta alquilado.")
        if duracion_horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un minimo de 2 horas.")

    def calcular_costo(self, duracion_horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        self.validar_parametros_operacion(duracion_horas)
        # Incluye poliza obligatoria de seguro del 5% sobre la tarifa base por hora
        subtotal = (self.tarifa_base * 1.05) * duracion_horas
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo [{self.id_entidad}]: {self.nombre_servicio} ({self.tipo_equipo}) - ${self.tarifa_base}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoria y desarrollo de software."""

    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, tarifa_base, disponible)
        if not especialidad or not str(especialidad).strip():
            raise ParametrosFaltantesError("Debe indicar el area de especialidad de la asesoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros_operacion(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El consultor para '{self.especialidad}' no tiene agenda disponible.")
        if duracion_horas <= 0:
            raise DatosInvalidosError("La duracion de la asesoria debe ser de al menos 1 hora.")

    def calcular_costo(self, duracion_horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        self.validar_parametros_operacion(duracion_horas)
        subtotal = self.tarifa_base * duracion_horas
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Sin agenda"
        return f"Asesoria [{self.id_entidad}]: {self.nombre_servicio} (Area: {self.especialidad}) - ${self.tarifa_base}/h [{estado}]"