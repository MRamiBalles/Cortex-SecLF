# Guía de Instalación y Configuración: Cortex-SecLF

## Requisitos Previos

- **Docker Desktop** (con Docker Compose).
- **Python 3.10+** (solo si deseas correr tests locales sin contenedores).
- **Ollama** (opcional, para modelos 100% locales).
- **Git**.

## Pasos de Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/MRamiBalles/Cortex-SecLF.git
cd Cortex-SecLF
```

### 2. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz basándote en la plantilla:
```bash
# Ejemplo de configuración mínima
OPENAI_API_KEY=tu_clave_aqui
ANTHROPIC_API_KEY=tu_clave_aqui
HIVE_SOVEREIGN_MOCK=TRUE  # Activa para simulaciones offline
```

### 3. Levantar Infraestructura
Usa Docker Compose para levantar el backend, el frontend y la base de datos vectorial:
```bash
docker compose -f infra/compose.yaml up --build
```

---

## Primeros Pasos

1.  **Verificación**: Accede a `http://localhost:8000/health` para confirmar que el backend está operativo.
2.  **Carga de Datos**: Coloca tus documentos en `data/documents/` y usa el comando de ingesta desde la UI de Archive o vía API.
3.  **Acceso UI**: Abre `http://localhost:3000` para entrar al Nexo de control.

## Resolución de Problemas

- **Error de Conexión Docker**: Asegúrate de que el daemon de Docker esté corriendo.
- **Modelos de IA**: Si usas Ollama, asegúrate de haber ejecutado `ollama pull llama3` antes de iniciar el sistema por primera vez.
