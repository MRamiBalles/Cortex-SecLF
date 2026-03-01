# Guía de Contribución: Cortex-SecLF

¡Gracias por tu interés en contribuir a la soberanía neural! Como este es un proyecto de gobernanza crítica, seguimos estándares profesionales estrictos.

## Estándares de Código

### 1. Robustez y Logging
- **Logging**: No uses `print()`. Utiliza el módulo `logging` con el logger del componente (ej. `logging.getLogger("cslf.nombre_modulo")`).
- **Excepciones**: Sé específico. No uses `except: pass`. Captura excepciones conocidas y loggea el error con el contexto adecuado.
- **Tipado**: Usa *Type Hints* de Python para todas las funciones nuevas.

### 2. Seguridad
- **Sandboxing**: Cualquier ejecución de código de terceros o de agentes DEBE realizarse dentro de los límites de Docker o un entorno controlado.
- **Privacidad**: Respeta el flujo de consentimiento. Nunca loggees datos sensibles del usuario o señales neurodinámicas crudas.

## Flujo de Trabajo

1.  **Issue/Propuesta**: Antes de un cambio mayor, discute la arquitectura en el Technical Manifesto.
2.  **Ramas**: Usa prefijos descriptivos como `feat/`, `fix/`, o `docs/`.
3.  **Tests**: Cada motor (`engine`) debe tener un script de verificación en `backend/tests/`.
4.  **Documentación**: Actualiza el `README.md` o los documentos en `/docs` si cambias la lógica central.

## Revisión de Pares (Peer Review)
Todas las contribuciones técnicas pasan por un proceso de revisión centrado en:
- Veracidad técnica y seguridad.
- Legibilidad y mantenibilidad.
- Alineación con el manifiesto soberano.

---
Mantenemos la excelencia técnica para asegurar que la IA permanezca bajo control humano.
