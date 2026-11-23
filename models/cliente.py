"""Modulo: cliente.py
Descripcion: Define la clase Cliente heredando de EntidadSistema, aplicando
encapsulacion estricta y validaciones para documento, nombre, correo y telefono."""

import re
from models.entidad import EntidadSistema
from exceptions.errores import DatosInvalidosError, ParametrosFaltantesError


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con validacion de datos personales."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llama al constructor de la clase abstracta padre
        super().__init__(id_cliente)
        # Usa los setters con validacion al asignar cada atributo
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametrosFaltantesError("El nombre del cliente no puede estar vacio.")
        if len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametrosFaltantesError("El correo electronico es obligatorio.")
        # Expresion regular basica para validar el formato usuario@dominio.ext
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, valor.strip()):
            raise DatosInvalidosError(f"Formato de correo invalido: '{valor}'.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametrosFaltantesError("El numero de telefono es obligatorio.")
        # Limpia espacios o guiones y verifica que sean solo digitos (minimo 7)
        limpio = str(valor).strip().replace(" ", "").replace("-", "")
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosInvalidosError(f"Numero de telefono invalido: '{valor}'. Debe tener al menos 7 dígitos.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementacion polimorfica del resumen de la entidad Cliente."""
        return f"Cliente [{self.id_entidad}] - {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"