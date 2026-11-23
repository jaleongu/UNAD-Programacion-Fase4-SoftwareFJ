"""Modulo: reserva.py
Descripcion: Define la clase Reserva que articula un Cliente con un Servicio,
gestionando estados (PENDIENTE, CONFIRMADA, CANCELADA), procesamiento de costos
y encadenamiento de excepciones."""

from models.entidad import EntidadSistema
from models.cliente import Cliente
from models.servicio import Servicio
from exceptions.errores import (
    ReservaInvalidaError,
    ParametrosFaltantesError,
    ErrorBaseSistema,
)


class Reserva(EntidadSistema):
    """Gestiona el ciclo de vida de una reserva en Software FJ."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(id_reserva)
        # Valida que cliente y servicio correspondan a instancias validas
        if not isinstance(cliente, Cliente):
            raise ParametrosFaltantesError("Se requiere una instancia valida de Cliente para la reserva.")
        if not isinstance(servicio, Servicio):
            raise ParametrosFaltantesError("Se requiere una instancia valida de Servicio para la reserva.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Calcula el costo del servicio, marca el servicio como ocupado y confirma la reserva.
        Implementa encadenamiento de excepciones (raise ... from e) si falla alguna validacion.
        """
        if self.estado != "PENDIENTE":
            raise ReservaInvalidaError(
                f"No se puede confirmar la reserva {self.id_entidad} porque su estado actual es '{self.estado}'."
            )

        try:
            # Delega el calculo polimorfico al servicio correspondiente
            self.costo_total = self.servicio.calcular_costo(
                duracion_horas=self.duracion_horas,
                impuesto=impuesto,
                descuento=descuento
            )
            # Bloquea la disponibilidad del servicio tras confirmar
            self.servicio.disponible = False
            self.estado = "CONFIRMADA"
            return self.costo_total

        except ErrorBaseSistema as error_original:
            # Encadenamiento de excepciones: conserva la traza original bajo un error de reserva
            raise ReservaInvalidaError(
                f"Fallo al procesar la reserva {self.id_entidad} para el cliente {self.cliente.nombre}."
            ) from error_original

    def cancelar_reserva(self) -> None:
        """Cancela una reserva activa y libera nuevamente la disponibilidad del servicio."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id_entidad} ya se encuentra cancelada.")

        # Si estaba confirmada, libera el recurso para futuros clientes
        if self.estado == "CONFIRMADA":
            self.servicio.disponible = True

        self.estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio} | "
            f"Duracion: {self.duracion_horas}h | Total: ${self.costo_total:,.2f}"
        )