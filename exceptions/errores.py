"""Modulo: errores.py
Descripcion: Define la jerarquia de excepciones personalizadas para el sistema
integral de gestion de clientes, servicios y reservas de Software FJ."""


class ErrorBaseSistema(Exception):
    """Clase base para todas las excepciones personalizadas del sistema."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        # Almacenamos el mensaje descriptivo y un codigo identificador del error
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        # Llamamos al constructor de la clase padre Exception
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatosInvalidosError(ErrorBaseSistema):
    """Se lanza cuando los datos ingresados no cumplen con el formato o reglas."""

    def __init__(self, mensaje: str):
        # Asigna el codigo especifico para errores de validacion de datos
        super().__init__(mensaje, codigo_error="ERR-DATOS")


class ParametrosFaltantesError(ErrorBaseSistema):
    """Se lanza cuando faltan parámetros obligatorios para crear un objeto o ejecutar un proceso."""

    def __init__(self, mensaje: str):
        # Asigna el codigo especifico para parametros nulos o vacios
        super().__init__(mensaje, codigo_error="ERR-PARAMS")


class ServicioNoDisponibleError(ErrorBaseSistema):
    """Se lanza cuando un servicio no esta activo o no tiene cupo/disponibilidad."""

    def __init__(self, mensaje: str):
        # Asigna el codigo especifico para indisponibilidad de servicios
        super().__init__(mensaje, codigo_error="ERR-SERVICIO")


class ReservaInvalidaError(ErrorBaseSistema):
    """Se lanza ante operaciones no permitidas o inconsistencias en una reserva."""

    def __init__(self, mensaje: str):
        # Asigna el codigo especifico para errores en el ciclo de vida de la reserva
        super().__init__(mensaje, codigo_error="ERR-RESERVA")


class CalculoInconsistenteError(ErrorBaseSistema):
    """Se lanza cuando el calculo de tarifas, impuestos o descuentos arroja valores incoherentes."""

    def __init__(self, mensaje: str):
        # Asigna el codigo especifico para fallos matematicos o financieros
        super().__init__(mensaje, codigo_error="ERR-CALCULO")