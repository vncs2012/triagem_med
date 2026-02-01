# 🏥 AgentTriagem

> Sistema Híbrido de Agentes de IA para Triagem Médica Automatizada - Detecção de Pneumonia em Raio-X

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Google ADK](https://img.shields.io/badge/Google-ADK-orange.svg)](https://github.com/google/adk)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20+-FF6F00.svg)](https://tensorflow.org)

<p align="center">
  <strong>🇧🇷 Português</strong> •
  <a href="README.en.md">🇺🇸 English</a>
</p>

---

## 📋 Descrição

O **AgentTriagem** é um sistema híbrido que combina **Redes Neurais Convolucionais (CNN)** com uma **arquitetura multiagente** para triagem médica automatizada. O sistema utiliza a arquitetura **DenseNet121** para detecção de pneumonia em imagens de raio-X torácico, com orquestração via **Google ADK** e interoperabilidade através do **Model Context Protocol (MCP)**.

### 🎯 Principais Características

- **Detecção de Pneumonia**: Modelo CNN DenseNet121 com acurácia de **88.3%** e AUC de **0.96**
- **Arquitetura Multiagente**: 5 agentes especializados colaborando através de 10 ferramentas
- **Classificação por Prioridade**: Baixa, Média, Alta e Crítica
- **Integração Completa**: Banco de dados, notificações por email e geração de relatórios
- **Interface MCP**: Conectividade externa via Server-Sent Events (SSE)

---

## 📚 Documentação

Para mais detalhes sobre o sistema, consulte os documentos na pasta [docs/](docs):

- [Artigo Técnico (Markdown)](docs/artigo_tecnico.md) - Descrição detalhada da arquitetura e resultados.
- [Short Paper (Docx)](docs/Short%20Paper%20AgentTriagem.docx) - Formato de submissão SBC.
- [Short Paper (PDF)](docs/Short%20Paper%20AgentTriagem.pdf) - Versão em PDF.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      MCP Server (SSE)                           │
│                  http://localhost:8001                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                           │
│              (Coordenador Central - LLM)                        │
└───┬───────────────┬───────────────┬───────────────┬─────────────┘
    │               │               │               │
┌───▼───┐     ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
│TRIAGEM│     │ DATABASE  │   │NOTIFICATION│  │  REPORT   │
│ AGENT │     │   AGENT   │   │   AGENT   │   │   AGENT   │
└───┬───┘     └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
    │               │               │               │
┌───▼───┐  ┌───────┴───────┐   ┌───▼───┐      ┌────▼────┐
│  CNN  │  │   SQLite DB   │   │ SMTP  │      │   PDF   │
│ Model │  │               │   │ Queue │      │ Reports │
└───────┘  └───────────────┘   └───────┘      └─────────┘
```

---

## 🤖 Agentes e Ferramentas

| Agente                 | Descrição                              | Ferramentas                                                                                                           |
| ---------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Orchestrator**       | Coordenador central que delega tarefas | Gerencia fluxos de trabalho                                                                                           |
| **Triagem Agent**      | Análise de imagens via CNN             | `analisar_imagem()`                                                                                                   |
| **Database Agent**     | CRUD de pacientes e diagnósticos       | `obter_paciente()`, `listar_pacientes()`, `obter_historico_paciente()`, `obter_diagnostico()`, `obter_diagnosticos()` |
| **Notification Agent** | Comunicação e alertas                  | `enviar_email()`, `enviar_alerta()`                                                                                   |
| **Report Agent**       | Geração de documentos                  | `generate_pdf()`, `generate_stats()`                                                                                  |

---

## 📊 Níveis de Prioridade

| Prioridade     | Confiança | Ação Recomendada                            |
| -------------- | --------- | ------------------------------------------- |
| 🟢 **BAIXA**   | < 45%     | Exame normal, acompanhamento de rotina      |
| 🟡 **MÉDIA**   | 45-50%    | Sinais suspeitos, acompanhamento em 24-48h  |
| 🟠 **ALTA**    | 50-70%    | Pneumonia detectada, avaliação no mesmo dia |
| 🔴 **CRÍTICA** | > 70%     | Caso grave, atenção médica imediata         |

---

## 📈 Resultados do Modelo

O modelo DenseNet121 foi treinado com o dataset [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) e avaliado em conjunto de teste independente:

| Métrica                   | Valor |
| ------------------------- | ----- |
| Acurácia                  | 88.3% |
| AUC                       | 0.96  |
| Sensibilidade (Pneumonia) | 95%   |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.13+
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências
- [Ollama](https://ollama.ai/) para LLM local

### Passos

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/AgentTriagem.git
   cd AgentTriagem
   ```

2. **Instale as dependências**

   ```bash
   poetry install
   ```

3. **Configure as variáveis de ambiente**

   ```bash
   cp .env_exemple .env
   # Edite o arquivo .env com suas configurações
   ```

4. **Inicie o Ollama** (em outro terminal)
   ```bash
   ollama run hermes3:8b
   ```

---

## ▶️ Execução

### Iniciar o Servidor MCP

```bash
poetry run python src/mcp_server.py
```

O servidor MCP estará disponível em `http://localhost:8001`

### Iniciar a API Frontend

```bash
poetry run python src/api.py
```

A API estará disponível em `http://localhost:8000`

### Interface de Chat

Acesse `http://localhost:8000/` para a interface de chat web.

---

## 💬 Exemplos de Uso

```
• "Analise a imagem /caminho/para/raio-x.jpg"
• "Busque o paciente P001 e envie email com o diagnóstico"
• "Liste todos os pacientes cadastrados"
• "Gere um relatório PDF do diagnóstico do paciente P002"
• "Mostre estatísticas de todos os diagnósticos"
• "Envie alerta crítico para a equipe sobre o paciente P003"
```

---

## 📁 Estrutura do Projeto

```
AgentTriagem/
├── src/
│   ├── agents/
│   │   ├── orchestrator/     # Agente orquestrador
│   │   ├── triagem/          # Agente de análise CNN
│   │   ├── database/         # Agente de banco de dados
│   │   ├── notification/     # Agente de notificações
│   │   └── report/           # Agente de relatórios
│   ├── database/             # Modelos e conexão SQLite
│   ├── client/               # Interface web (chat.html)
│   ├── api.py                # API FastAPI
│   ├── mcp_server.py         # Servidor MCP
│   └── config.py             # Configurações
├── models/                   # Modelo CNN treinado
├── data/                     # Dados e uploads
├── docs/                     # Documentação
└── scripts/                  # Scripts auxiliares
```

---

## 🛠️ Tecnologias

- **[Google ADK](https://github.com/google/adk)** - Agent Development Kit
- **[LiteLLM](https://github.com/BerriAI/litellm)** - Integração com LLMs
- **[TensorFlow/Keras](https://tensorflow.org)** - Modelo CNN DenseNet121
- **[FastAPI](https://fastapi.tiangolo.com/)** - API REST
- **[MCP](https://modelcontextprotocol.io/)** - Model Context Protocol
- **[SQLAlchemy](https://sqlalchemy.org/)** - ORM para SQLite
- **[Ollama](https://ollama.ai/)** - LLM local

---

## 📚 Referências

- HUANG, G. et al. **Densely Connected Convolutional Networks**. CVPR, 2017.
- KERMANY, D. S. et al. **Identifying Medical Diagnoses by Image-Based Deep Learning**. Cell, 2018.
- ANTHROPIC. **Model Context Protocol (MCP)**: Specification. 2024.
- GOOGLE. **Agent Development Kit (ADK)**: Framework for AI Agents. 2025.

---

## 📝 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

## 👤 Autor

**Vinicius Miranda**  
📧 vncs2012@gmail.com

---
