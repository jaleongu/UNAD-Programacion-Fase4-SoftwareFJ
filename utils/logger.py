"""Modulo: logger.py
Descripcion: Gestiona el registro de eventos y errores del sistema mediante
archivos de texto plano (.log), garantizando trazabilidad sin usar bases de datos."""

import os
from datetime import datetime


class GestorLogs:
    """Clase encargada de escribir eventos informativos y errores en un archivo de log."""

    def __init__(self, ruta_archivo: str = "logs/sistema.log"):
        # Define la ruta del archivo donde se almacenaran los registros
        self.ruta_archivo = ruta_archivo
        # Verifica si el directorio existe; si no, lo crea automaticamente
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

    def _escribir_registro(self, nivel: str, mensaje: str) -> None:
        """Metodo privado que formatea y escribe una linea en el archivo de log."""
        # Obtiene la fecha y hora actual en formato Año-Mes-Dia Hora:Minuto:Segundo
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la linea estructurada del registro
        linea_log = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"

        # Abre el archivo en modo 'append' (a) con codificacion UTF-8 para no sobrescribir lo anterior
        with open(self.ruta_archivo, mode="a", encoding="utf-8") as archivo:
            archivo.write(linea_log)

    def registrar_info(self, mensaje: str) -> None:
        """Registra una operacion exitosa o evento informativo del sistema."""
        self._escribir_registro("INFO", mensaje)

    def registrar_error(self, mensaje: str, detalle_tecnico: str = "") -> None:
        """Registra una excepcion o fallo controlado manteniendo la ejecucion activa."""
        # Si hay detalle tecnico (como encadenamiento de excepciones), lo anexa al mensaje
        texto_completo = f"{mensaje} | Detalle: {detalle_tecnico}" if detalle_tecnico else mensaje
        self._escribir_registro("ERROR", texto_completo)