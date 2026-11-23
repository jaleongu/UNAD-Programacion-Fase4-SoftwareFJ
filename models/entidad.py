"""Modulo: entidad.py
Descripcion: Define la clase abstracta base EntidadSistema que establece
la estructura comun (identificador y fecha de registro) para las entidades
del sistema de Software FJ."""

from abc import ABC, abstractmethod
from datetime import datetime
from exceptions.errores import ParametrosFaltantesError


class EntidadSistema(ABC):
    """Clase abstracta base para las entidades principales del sistema."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacia
        if not id_entidad or not str(id_entidad).strip():
            raise ParametrosFaltantesError("El identificador de la entidad es obligatorio.")
        # Atributo protegido para aplicar encapsulacion
        self._id_entidad = str(id_entidad).strip()
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador unico de la entidad (solo lectura)."""
        return self._id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora en que fue instanciada la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Metodo abstracto que obliga a las clases hijas a describirse."""
        pass