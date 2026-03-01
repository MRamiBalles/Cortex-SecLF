# Arquitectura del Sistema: Cortex-SecLF

## Introducción
Cortex-SecLF es un sistema modular diseñado para la soberanía técnica y la seguridad de la IA. El sistema se organiza en torno a un "Nexus" central que orquesta múltiples motores especializados.

## Diagrama de Bloques

```mermaid
graph TD
    User([Usuario]) --> Frontend[Nexus UI - Next.js]
    Frontend --> Backend[Nexus API - FastAPI]
    
    subgraph "Motores Core"
        Backend --> RAG[RAG Engine - ChromaDB]
        Backend --> Lab[Agent Lab - Docker Container]
        Backend --> Dojo[Dojo - Vulnerable Labs]
        Backend --> Scientist[AI Scientist - Hive/Synthetic]
    end
    
    subgraph "Gobernanza & Datos"
        RAG --> Docs[(Documentos Locales)]
        Lab --> Watcher[Watcher & Kill-Switch]
        Backend --> Neuro[Neuro-Rights & ZKP Ledger]
    end
```

## Motores Detallados

### 1. RAG Engine (Archive)
Gestiona el conocimiento "frío" del sistema.
- **Ingestor**: Clasifica documentos en tres colecciones: `doctrine` (teoría), `trench` (técnica ofensiva) y `future` (especulación/roadmap).
- **Splitter**: Utiliza un divisor recursivo sensible al contexto para no romper la sintaxis de exploits.

### 2. Agent Lab (The Cage)
Un entorno de sandbox para agentes autónomos.
- **Watcher**: Monitorea procesos y logs para detectar intentos de replicación o exfiltración.
- **Kill-Switch**: Protocolo de emergencia que termina contenedores si se detecta una violación de los límites de seguridad.

### 3. Dojo Control
Orquestador de entornos de entrenamiento.
- Permite desplegar laboratorios dinámicos para probar hipótesis del "AI Scientist" o entrenar defensas.

### 4. AI Scientist
Simula el ciclo de investigación científica:
1.  **Ideación**: Genera una hipótesis.
2.  **Experimentación**: Produce código Python para probar la hipótesis.
3.  **Auditoría**: Un "Peer Reviewer" evalúa los resultados y el riesgo de seguridad.

## Análisis de Impacto y Seguridad

### 1. Modelo de Amenazas (Threat Model)
- **Amenaza**: Fuga de datos neurodinámicos.
  - **Mitigación**: Implementación de consentimiento obligatorio y verificación vía ZKP en el motor `NeuroSim`. Los datos crudos nunca tocan el ledger.
- **Amenaza**: Escape del contenedor por parte de un agente.
  - **Mitigación**: El `Watcher` monitoriza syscalls prohibidas y tokens críticos en tiempo real. Configuración de `read_only` y límites de PIDs en Docker para prevenir ataques de denegación de servicio (Fork Bombs).

### 2. Integridad de los Datos (RAG)
El motor de búsqueda utiliza un umbral de distancia estricto (`threshold=0.4`) para evitar alucinaciones. Si no hay evidencia documental en el Archivo, el sistema emite una alerta de **Alto Riesgo de Alucinación**, forzando al operador humano a intervenir o proveer más contexto.

## Restricciones Operativas
- **Modo Soberano**: En caso de fallo de infraestructura crítica (Docker o Base de Datos), el sistema entra en modo de contingencia, limitando las acciones del agente a un sandbox local de subprocesos menos potente pero seguro.
- **Auditoría Permanente**: Cada decisión de la IA (hipótesis y diseño de experimentos) se almacena con un hash SHA-256 para asegurar que el rastro forense no pueda ser alterado post-evento.

---
*Cortex-SecLF: Seguridad por diseño, soberanía por arquitectura.*
