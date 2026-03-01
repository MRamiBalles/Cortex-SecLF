# Cortex-Sec Local Forge (SecLF) v1.0.0

![Cortex-SecLF Logo](https://img.shields.io/badge/Status-Development-orange)
![License](https://img.shields.io/badge/License-Proprietary-red)
![AI-Powered](https://img.shields.io/badge/AI-Autonomous-blue)

**Cortex-SecLF** es un ecosistema de gobernanza de inteligencia artificial y ciberseguridad diseñado para ejecutarse de forma 100% local (Air-Gapped Ready). Proporciona un entorno seguro para el desarrollo, prueba y contención de agentes autónomos bajo protocolos de seguridad estrictos.

## 🚀 Módulos Principales (El Nexus)

### 1. Archive (RAG Engine)
Motor de búsqueda semántica especializado en ciberseguridad y doctrina legal. Utiliza **LangChain** y **ChromaDB** para procesar documentos técnicos sin romper la lógica de los exploits.

### 2. Agent Lab
Entorno de contención "The Cage" para monitorizar agentes autónomos. Incluye un sistema de **Kill-Switch** y monitorización activa de comportamiento anómalo.

### 3. Dojo
Laboratorios de entrenamiento para simular ataques y defensas. Integrado con **Wazuh** para telemetría de seguridad en tiempo real.

### 4. AI Scientist (Hive)
Orquestador de investigación autónoma que genera hipótesis, diseña experimentos en Python y realiza procesos de "Peer Review" automatizados.

### 5. Neuro-Rights Ledger
Sistema basado en **Blockchain Local** y **ZKP (Zero-Knowledge Proofs)** para la gestión soberana de la privacidad mental y datos neurodinámicos.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Next.js 14, Tailwind CSS, Lucide React
- **AI/LLM**: Ollama (Llama 3, DeepSeek), OpenAI/Anthropic (Opcional)
- **Vector DB**: ChromaDB
- **Infra**: Docker & Docker Compose

---

## 🚦 Inicio Rápido

1.  **Requisitos**: Docker, Docker Compose y Python 3.10.
2.  **Configuración**:
    ```bash
    cp .env.example .env
    # Edita tus claves API o activa HIVE_SOVEREIGN_MOCK=TRUE para modo local
    ```
3.  **Despliegue**:
    ```bash
    docker compose -f infra/compose.yaml up --build
    ```

---

## 📂 Documentación Detallada

Para más información, consulta la carpeta [`/docs`](/docs):
- [Arquitectura del Sistema](/docs/architecture.md)
- [Guía de API](/docs/api_guide.md)
- [Guía de Instalación](/docs/setup.md)

---

## ⚖️ Licencia y Propiedad

Desarrollado por **Manuel Ramírez Ballesteros**. Contacto: [ramiballes96@gmail.com](mailto:ramiballes96@gmail.com).
Este proyecto es propiedad intelectual privada. Todos los derechos reservados.
