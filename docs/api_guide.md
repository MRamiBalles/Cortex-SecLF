# Guía de API: Cortex-SecLF

La API está construida con **FastAPI** y sigue una estructura modular de routers. Por defecto, corre en `http://localhost:8000`.

## Endpoints Principales

### 1. Archive (RAG)
- **POST `/archive/search`**: Realiza búsquedas semánticas.
  - *Payload*: `{"query": "string", "collection": "doctrine|trench|future"}`
- **POST `/archive/ingest/trigger`**: Inicia el escaneo de archivos locales en background.

### 2. Agent Lab
- **POST `/lab/start`**: Inicia una simulación de contención.
  - *Scenarios*: `scream_test`, `self_replication`, `exfiltration`.
- **POST `/lab/reset`**: Limpia el entorno del sandbox.

### 3. AI Scientist
- **POST `/scientist/research`**: Inicia un ciclo autónomo de investigación.
  - *Payload*: `{"topic": "descripción del tema"}`

### 4. Neuro-Rights
- **GET `/neuro/stream`**: Obtiene datos neurodinámicos simulados (sujeto a consentimiento).
- **POST `/neuro/consent`**: Actualiza el estado de consentimiento (`GRANT` | `REVOKE`).

---

## Ejemplos de Uso (cURL)

### Búsqueda en el Archivo
```bash
curl -X POST "http://localhost:8000/archive/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "vector de ataque EEG", "collection": "trench"}'
```

### Iniciar Investigación Autónoma
```bash
curl -X POST "http://localhost:8000/scientist/research" \
     -H "Content-Type: application/json" \
     -d '{"topic": "obfuscación de logs en agentes"}'
```

---

## Documentación Interactiva
Puedes acceder a la documentación interactiva de Swagger UI en:
`http://localhost:8000/docs`
