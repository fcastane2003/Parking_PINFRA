"""
Utilidades para la capa de datos.

Responsabilidad:
- Normalizar placas (normalize_plate) usada por consultas e inserciones.
- Mantener una única definición de normalización
  para evitar duplicados lógicos.
"""

import re


def normalize_plate(plate: str) -> str:
    """
    Normaliza una placa para almacenamiento y búsqueda.

    - Convierte a mayúsculas.
    - Elimina caracteres que no sean A-Z o 0-9 (espacios, guiones, puntos).
    - Valida longitud mínima resultante (3).
    """
    if plate is None:
        raise ValueError("La placa es requerida.")

    s = str(plate).upper().strip()
    s = re.sub(r"[^A-Z0-9]", "", s)

    if len(s) < 3:
        raise ValueError(
            "La placa no es válida después de normalizar (longitud < 3)."
        )

    return s
