"""Modulo: main.py
Descripcion: Punto de entrada del Sistema Integral de Gestion de Clientes,
Servicios y Reservas para Software FJ. Simula 12 operaciones (validas e invalidas)
demostrando estabilidad, manejo avanzado de excepciones y registro en logs sin bases de datos."""

from utils.logger import GestorLogs
from models.cliente import Cliente
from models.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from models.reserva import Reserva
from exceptions.errores import (
    ErrorBaseSistema,
    DatosInvalidosError,
    ParametrosFaltantesError,
    ReservaInvalidaError,
)


class SistemaSoftwareFJ:
    """Controlador principal que administra las listas en memoria de clientes, servicios y reservas."""

    def __init__(self):
        # Listas internas para almacenamiento en memoria (sin uso de bases de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []
        # Instancia del gestor de archivos de log
        self.logger = GestorLogs("logs/sistema.log")
        self.logger.registrar_info("=== INICIO DE EJECUCION DEL SISTEMA SOFTWARE FJ ===")

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Cliente | None:
        """Intenta crear y registrar un cliente usando bloque try/except/else."""
        try:
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorBaseSistema as err:
            # Captura errores de validacion o parametros faltantes sin detener el sistema
            print(f"[ERROR CLIENTE] {err}")
            self.logger.registrar_error(f"Fallo al registrar cliente '{nombre}': {err}")
            return None
        else:
            # El bloque 'else' se ejecuta unicamente si no hubo excepciones en el 'try'
            self.clientes.append(nuevo_cliente)
            mensaje = f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}"
            print(f"[OK] {mensaje}")
            self.logger.registrar_info(mensaje)
            return nuevo_cliente

    def registrar_servicio(self, servicio_obj) -> bool:
        """Agrega un servicio instanciado al catalogo interno."""
        if servicio_obj is not None:
            self.servicios.append(servicio_obj)
            mensaje = f"Servicio habilitado: {servicio_obj.obtener_resumen()}"
            print(f"[OK] {mensaje}")
            self.logger.registrar_info(mensaje)
            return True
        return False

    def crear_y_procesar_reserva(
        self, id_reserva: str, cliente: Cliente, servicio, duracion_horas: int, descuento: float = 0.0
    ) -> Reserva | None:
        """
        Crea y confirma una reserva utilizando try/except/finally y gestionando
        el encadenamiento de excepciones proveniente de Reserva.procesar_y_confirmar().
        """
        reserva_actual = None
        try:
            reserva_actual = Reserva(id_reserva, cliente, servicio, duracion_horas)
            costo = reserva_actual.procesar_y_confirmar(descuento=descuento)
            self.reservas.append(reserva_actual)
            mensaje = f"Reserva confirmada -> {reserva_actual.obtener_resumen()}"
            print(f"[OK] {mensaje}")
            self.logger.registrar_info(mensaje)
            return reserva_actual

        except ReservaInvalidaError as err_reserva:
            # Extrae la causa raiz si existe encadenamiento de excepciones (__cause__)
            causa_raiz = str(err_reserva.__cause__) if err_reserva.__cause__ else "Sin causa encadenada"
            print(f"[ERROR RESERVA] {err_reserva} -> Causa raiz: {causa_raiz}")
            self.logger.registrar_error(str(err_reserva), detalle_tecnico=causa_raiz)
            return None

        except ErrorBaseSistema as err_general:
            print(f"[ERROR VALIDACION RESERVA] {err_general}")
            self.logger.registrar_error(f"Error al instanciar reserva {id_reserva}: {err_general}")
            return None

        finally:
            # El bloque 'finally' siempre se ejecuta para auditar el cierre de la transaccion
            self.logger.registrar_info(f"Auditoria de cierre ejecutada para intento de reserva [{id_reserva}].")


def ejecutar_simulacion():
    """Ejecuta secuencialmente 12 operaciones completas (validas e invalidas)."""
    print("\n" + "=" * 70)
    print("SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ (FASE 4 UNAD)")
    print("=" * 70 + "\n")

    sistema = SistemaSoftwareFJ()

    # --- BLOQUE 1: REGISTRO DE CLIENTES (Validos e Invalidos) ---
    print("--- 1. GESTION DE CLIENTES ---")
    # Operacion 1: Registro valido de cliente 1
    c1 = sistema.registrar_cliente("CLI-01", "Laura Gomez", "laura.gomez@empresa.com", "3104567890")
    # Operacion 2: Registro valido de cliente 2
    c2 = sistema.registrar_cliente("CLI-02", "Carlos Mendoza", "cmendoza@tech.co", "3209876543")
    # Operacion 3: Registro invalido (correo sin formato correcto -> DatosInvalidosError)
    sistema.registrar_cliente("CLI-03", "Andres Ruiz", "andres_sin_arroba.com", "3001112233")
    # Operacion 4: Registro invalido (nombre vacio -> ParametrosFaltantesError)
    sistema.registrar_cliente("CLI-04", "", "valido@correo.com", "3150009988")

    # --- BLOQUE 2: CREACION DE SERVICIOS ESPECIALIZADOS (Validos e Invalidos) ---
    print("\n--- 2. GESTION DE SERVICIOS ---")
    # Operacion 5: Creacion valida de Sala de Juntas
    sala_juntas = None
    try:
        sala_juntas = ReservaSala("SRV-01", "Sala Innovacion Norte", 80000.0, capacidad_personas=12)
        sistema.registrar_servicio(sala_juntas)
    except ErrorBaseSistema as e:
        sistema.logger.registrar_error(f"Error creando sala: {e}")

    # Operacion 6: Creacion valida de Equipo de Computo
    estacion_trabajo = None
    try:
        estacion_trabajo = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 35000.0, tipo_equipo="Estacion Grafica")
        sistema.registrar_servicio(estacion_trabajo)
    except ErrorBaseSistema as e:
        sistema.logger.registrar_error(f"Error creando equipo: {e}")

    # Operacion 7: Creacion valida de Asesoria Especializada
    asesoria_arq = None
    try:
        asesoria_arq = AsesoriaEspecializada("SRV-03", "Consultoria Arquitectura Cloud", 120000.0, especialidad="AWS / DevOps")
        sistema.registrar_servicio(asesoria_arq)
    except ErrorBaseSistema as e:
        sistema.logger.registrar_error(f"Error creando asesoria: {e}")

    # Operacion 8: Creacion invalida de servicio (tarifa negativa -> DatosInvalidosError)
    try:
        servicio_erroneo = ReservaSala("SRV-99", "Sala Fantasma", -50000.0, capacidad_personas=5)
        sistema.registrar_servicio(servicio_erroneo)
    except DatosInvalidosError as e:
        print(f"[ERROR SERVICIO] {e}")
        sistema.logger.registrar_error(f"Intento de creacion de servicio con tarifa invalida: {e}")

    # --- BLOQUE 3: PROCESAMIENTO DE RESERVAS (Exitosas, Fallidas y Cancelaciones) ---
    print("\n--- 3. PROCESAMIENTO DE RESERVAS ---")
    # Operacion 9: Reserva exitosa de Sala por 5 horas (aplica recargo limpieza y descuento)
    res1 = sistema.crear_y_procesar_reserva("RES-101", c1, sala_juntas, duracion_horas=5, descuento=20000.0)

    # Operacion 10: Reserva fallida por servicio no disponible (la sala ya fue reservada en RES-101)
    sistema.crear_y_procesar_reserva("RES-102", c2, sala_juntas, duracion_horas=2)

    # Operacion 11: Reserva fallida por duracion invalida en alquiler de equipo (minimo 2 horas)
    sistema.crear_y_procesar_reserva("RES-103", c2, estacion_trabajo, duracion_horas=1)

    # Operacion 12: Reserva exitosa de Asesoria Especializada y posterior cancelacion controlada
    res4 = sistema.crear_y_procesar_reserva("RES-104", c2, asesoria_arq, duracion_horas=3)
    if res4:
        try:
            res4.cancelar_reserva()
            msg_cancel = f"Reserva cancelada correctamente y servicio liberado: {res4.obtener_resumen()}"
            print(f"[OK] {msg_cancel}")
            sistema.logger.registrar_info(msg_cancel)
            # Intento de volver a cancelar la misma reserva (dispara ReservaInvalidaError)
            res4.cancelar_reserva()
        except ReservaInvalidaError as e:
            print(f"[ERROR CANCELACION] {e}")
            sistema.logger.registrar_error(f"Operacion no permitida al cancelar: {e}")

    # Operacion 13 (Extra): Calculo inconsistente (descuento mayor al subtotal)
    sistema.crear_y_procesar_reserva("RES-105", c1, estacion_trabajo, duracion_horas=2, descuento=500000.0)

    sistema.logger.registrar_info("=== FIN DE EJECUCION EXITOSA SIN INTERRUPCIONES ===")
    print("\n" + "=" * 70)
    print(f"Resumen en memoria -> Clientes: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas: {len(sistema.reservas)}")
    print("Revisa el archivo 'logs/sistema.log' para verificar la auditoria completa.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    ejecutar_simulacion()