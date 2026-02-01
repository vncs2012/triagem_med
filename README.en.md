# 🏥 AgentTriagem

> Hybrid AI Agent System for Automated Medical Triage - Pneumonia Detection in Chest X-Ray

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Google ADK](https://img.shields.io/badge/Google-ADK-orange.svg)](https://github.com/google/adk)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20+-FF6F00.svg)](https://tensorflow.org)

<p align="center">
  <a href="README.md">🇧🇷 Português</a> •
  <strong>🇺🇸 English</strong>
</p>

---

## 📋 Description

**AgentTriagem** is a hybrid system that combines **Convolutional Neural Networks (CNN)** with a **multi-agent architecture** for automated medical triage. The system uses the **DenseNet121** architecture for pneumonia detection in chest X-ray images, with orchestration via **Google ADK** and interoperability through the **Model Context Protocol (MCP)**.

### 🎯 Key Features

- **Pneumonia Detection**: DenseNet121 CNN model with **88.3% accuracy** and **0.96 AUC**
- **Multi-Agent Architecture**: 5 specialized agents collaborating through 10 tools
- **Priority Classification**: Low, Medium, High, and Critical
- **Complete Integration**: Database, email notifications, and report generation
- **MCP Interface**: External connectivity via Server-Sent Events (SSE)

---

## 📚 Documentation

For more details about the system, see the documents in the [docs/](file:///home/vncs/Documentos/Particular/AgentTriagem/docs) folder:

- [Technical Article (Markdown)](file:///home/vncs/Documentos/Particular/AgentTriagem/docs/artigo_tecnico.md) - Detailed description of the architecture and results.
- [Short Paper (Docx)](file:///home/vncs/Documentos/Particular/AgentTriagem/docs/Short%20Paper%20AgentTriagem.docx) - SBC submission format.
- [Short Paper (PDF)](file:///home/vncs/Documentos/Particular/AgentTriagem/docs/Short%20Paper%20AgentTriagem.pdf) - PDF version.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      MCP Server (SSE)                           │
│                  http://localhost:8001                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                           │
│                (Central Coordinator - LLM)                      │
└───┬───────────────┬───────────────┬───────────────┬─────────────┘
    │               │               │               │
┌───▼───┐     ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
│TRIAGE │     │ DATABASE  │   │NOTIFICATION│  │  REPORT   │
│ AGENT │     │   AGENT   │   │   AGENT   │   │   AGENT   │
└───┬───┘     └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
    │               │               │               │
┌───▼───┐  ┌───────┴───────┐   ┌───▼───┐      ┌────▼────┐
│  CNN  │  │   SQLite DB   │   │ SMTP  │      │   PDF   │
│ Model │  │               │   │ Queue │      │ Reports │
└───────┘  └───────────────┘   └───────┘      └─────────┘
```

---

## 🤖 Agents and Tools

| Agent                  | Description                              | Tools                                                                                             |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Orchestrator**       | Central coordinator that delegates tasks | Manages workflows                                                                                 |
| **Triage Agent**       | Image analysis via CNN                   | `analyze_image()`                                                                                 |
| **Database Agent**     | Patient and diagnosis CRUD               | `get_patient()`, `list_patients()`, `get_patient_history()`, `get_diagnosis()`, `get_diagnoses()` |
| **Notification Agent** | Communication and alerts                 | `send_email()`, `send_alert()`                                                                    |
| **Report Agent**       | Document generation                      | `generate_pdf()`, `generate_stats()`                                                              |

---

## 📊 Priority Levels

| Priority        | Confidence | Recommended Action                       |
| --------------- | ---------- | ---------------------------------------- |
| 🟢 **LOW**      | < 45%      | Normal exam, routine follow-up           |
| 🟡 **MEDIUM**   | 45-50%     | Suspicious signs, follow-up in 24-48h    |
| 🟠 **HIGH**     | 50-70%     | Pneumonia detected, same-day evaluation  |
| 🔴 **CRITICAL** | > 70%      | Severe case, immediate medical attention |

---

## 📈 Model Results

The DenseNet121 model was trained with the [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) dataset and evaluated on an independent test set:

| Metric                  | Value |
| ----------------------- | ----- |
| Accuracy                | 88.3% |
| AUC                     | 0.96  |
| Sensitivity (Pneumonia) | 95%   |

---

## 🚀 Installation

### Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) for local LLM

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/AgentTriagem.git
   cd AgentTriagem
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Configure environment variables**

   ```bash
   cp .env_exemple .env
   # Edit .env file with your settings
   ```

4. **Start Ollama** (in another terminal)
   ```bash
   ollama run hermes3:8b
   ```

---

## ▶️ Running

### Start MCP Server

```bash
poetry run python src/mcp_server.py
```

MCP server will be available at `http://localhost:8001`

### Start Frontend API

```bash
poetry run python src/api.py
```

API will be available at `http://localhost:8000`

### Chat Interface

Access `http://localhost:8000/` for the web chat interface.

---

## 💬 Usage Examples

```
• "Analyze the image /path/to/xray.jpg"
• "Find patient P001 and send email with diagnosis"
• "List all registered patients"
• "Generate PDF report for patient P002's diagnosis"
• "Show statistics for all diagnoses"
• "Send critical alert to team about patient P003"
```

---

## 📁 Project Structure

```
AgentTriagem/
├── src/
│   ├── agents/
│   │   ├── orchestrator/     # Orchestrator agent
│   │   ├── triagem/          # CNN analysis agent
│   │   ├── database/         # Database agent
│   │   ├── notification/     # Notification agent
│   │   └── report/           # Report agent
│   ├── database/             # Models and SQLite connection
│   ├── client/               # Web interface (chat.html)
│   ├── api.py                # FastAPI API
│   ├── mcp_server.py         # MCP Server
│   └── config.py             # Settings
├── models/                   # Trained CNN model
├── data/                     # Data and uploads
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

---

## 🛠️ Technologies

- **[Google ADK](https://github.com/google/adk)** - Agent Development Kit
- **[LiteLLM](https://github.com/BerriAI/litellm)** - LLM Integration
- **[TensorFlow/Keras](https://tensorflow.org)** - DenseNet121 CNN Model
- **[FastAPI](https://fastapi.tiangolo.com/)** - REST API
- **[MCP](https://modelcontextprotocol.io/)** - Model Context Protocol
- **[SQLAlchemy](https://sqlalchemy.org/)** - SQLite ORM
- **[Ollama](https://ollama.ai/)** - Local LLM

---

## 📚 References

- HUANG, G. et al. **Densely Connected Convolutional Networks**. CVPR, 2017.
- KERMANY, D. S. et al. **Identifying Medical Diagnoses by Image-Based Deep Learning**. Cell, 2018.
- ANTHROPIC. **Model Context Protocol (MCP)**: Specification. 2024.
- GOOGLE. **Agent Development Kit (ADK)**: Framework for AI Agents. 2025.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Vinicius Miranda**  
📧 vncs2012@gmail.com
