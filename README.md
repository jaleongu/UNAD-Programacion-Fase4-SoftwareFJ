# Sistema Integral de Gestion de Clientes, Servicios y Reservas - Software FJ

**Curso:** Programacion (213023) - Universidad Nacional Abierta y a Distancia (UNAD)  
**Actividad:** Fase 4 - Componente Practico (Practicas Simuladas)  
**Modalidad de desarrollo:** Individual  

## Descripcion del Proyecto
Aplicacion desarrollada en Python bajo el paradigma de **Programacion Orientada a Objetos (POO)** sin uso de bases de datos, diseñada para gestionar clientes, servicios especializados (salas, equipos tecnologicos y asesorias) y reservas para la empresa **Software FJ**. El sistema implementa manejo avanzado de excepciones y auditoria mediante archivos de texto plano (`.log`).

## Estructura del Proyecto
```text
UNAD-Programacion-Fase4-SoftwareFJ/
    exceptions/
        __init__.py
        errores.py          # Jerarquia de excepciones personalizadas
    models/
        __init__.py
        entidad.py          # Clase abstracta base (EntidadSistema)
        cliente.py          # Encapsulacion y validaciones estrictas
        servicio.py         # Clase abstracta Servicio y 3 clases derivadas
        reserva.py          # Gestion de estados y encadenamiento de excepciones
    utils/
        __init__.py
        logger.py           # Escritura de eventos y errores en logs/sistema.log
    logs/
        sistema.log         # Registro historico de ejecucion
    main.py                 # Simulacion de 13 operaciones validas e invalidas
    README.md               # Documentacion tecnica
