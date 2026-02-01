# Arquitetura Multiagente com CNN para Triagem Automatizada de Pneumonia

**Vinicius Carvalho Miranda**

Universidade de Rio Verde (UniRV)

📧 vncs2012@gmail.com

---

## Resumo

Este trabalho apresenta o AgentTriagem, um sistema híbrido que integra Redes Neurais Convolucionais (CNN) a uma arquitetura multiagente para triagem médica automatizada. O sistema utiliza a arquitetura DenseNet121 para detecção de pneumonia em imagens de raio-X torácico, empregando o conjunto de dados Chest X-Ray Images (Pneumonia), disponibilizado no Kaggle. A orquestração do fluxo de triagem é realizada por meio do Agent Development Kit (ADK) da Google, utilizando o Model Context Protocol (MCP) para garantir interoperabilidade entre fontes de dados e agentes inteligentes. Os resultados experimentais indicam acurácia de 88,3% e AUC de 0,96, demonstrando que a solução é eficaz como ferramenta de apoio à decisão clínica em ambientes hospitalares de alta demanda.

**Palavras-chave:** Triagem médica; Redes neurais convolucionais; Sistemas multiagente; Pneumonia; Inteligência artificial em saúde.

---

## Abstract

This paper presents AgentTriagem, a hybrid system that integrates Convolutional Neural Networks (CNN) with a multi-agent architecture for automated medical triage. The system employs the DenseNet121 architecture for pneumonia detection in chest X-ray images, using the Chest X-Ray Images (Pneumonia) dataset made publicly available on Kaggle. The triage workflow is orchestrated through Google's Agent Development Kit (ADK), while data interoperability among agents and external systems is ensured by the Model Context Protocol (MCP). Experimental results show an accuracy of 88.3% and an AUC of 0.96, indicating that the proposed solution is effective as a clinical decision-support tool in high-demand hospital environments.

**Keywords:** Medical triage; Convolutional neural networks; Multi-agent systems; Pneumonia; Artificial intelligence in healthcare.

---

## 1. Introdução

A pneumonia permanece como uma das principais causas de mortalidade em nível global, exigindo diagnósticos rápidos e precisos para redução de complicações graves [2]. Em unidades de emergência, a elevada demanda por atendimentos e a escassez de especialistas podem atrasar a análise de radiografias torácicas, impactando negativamente o prognóstico dos pacientes.

Embora modelos de Deep Learning tenham apresentado avanços significativos na classificação de imagens médicas, grande parte dessas soluções opera de forma isolada, sem integração aos fluxos clínicos e sistemas hospitalares. Nesse contexto, este trabalho propõe o AgentTriagem, uma solução que combina a capacidade diagnóstica da arquitetura DenseNet121 [1] com a flexibilidade de Sistemas Multiagente, permitindo automatizar não apenas a inferência, mas todo o processo de triagem, desde a consulta a bases de dados até a notificação médica, utilizando o ADK e o MCP [3][4].

---

## 2. Trabalhos Relacionados

Diversos estudos demonstram que arquiteturas baseadas em CNN apresentam desempenho comparável ou superior ao de especialistas humanos na detecção de patologias pulmonares em imagens de raio-X, especialmente no que se refere à velocidade de análise [2][5]. Entretanto, pesquisas recentes apontam que a eficácia clínica desses modelos depende fortemente de sua integração aos sistemas de informação em saúde.

Nesse cenário, protocolos de interoperabilidade como o Model Context Protocol (MCP), proposto em 2024, surgem como uma solução padronizada para conectar modelos de IA a diferentes fontes de dados de forma segura e estruturada [3]. O AgentTriagem diferencia-se dos trabalhos existentes ao aplicar essa interoperabilidade no contexto específico da triagem de pneumonia, utilizando uma arquitetura multiagente orquestrada pelo ADK [4].

---

## 3. Metodologia

### 3.1 Arquitetura do Sistema e Orquestração

O sistema adota uma arquitetura multiagente hierárquica implementada sobre o Agent Development Kit (ADK). Um agente orquestrador central é responsável por coordenar o fluxo da triagem, delegando tarefas a agentes especializados em diagnóstico, obtenção de contexto clínico e notificação médica. Essa abordagem permite modularidade, escalabilidade e fácil manutenção do sistema [4].

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

**Figura 1:** Estrutura dos agentes e ferramentas do sistema.

### 3.2 Desenvolvimento do Modelo de Machine Learning

O modelo de classificação utiliza a arquitetura DenseNet121, escolhida por sua eficiência no reaproveitamento de características e redução do número de parâmetros [1]. Foi empregada a técnica de Transfer Learning, com pesos pré-treinados no conjunto ImageNet. As imagens foram redimensionadas para 224 × 224 pixels e normalizadas conforme os padrões da arquitetura adotada.

### 3.3 Base de Dados

O treinamento e a avaliação do modelo utilizaram o dataset Chest X-Ray Images (Pneumonia), disponível publicamente no Kaggle [6]. O conjunto contém 5.856 imagens de radiografias torácicas, provenientes de coortes retrospectivas do Guangzhou Women and Children's Medical Center, amplamente utilizadas na literatura científica [2].

### 3.4 Model Context Protocol (MCP)

A integração entre agentes e fontes de dados é realizada por meio do Model Context Protocol (MCP), que permite a comunicação padronizada com sistemas externos, como bancos de imagens DICOM e prontuários eletrônicos, utilizando mensagens estruturadas no formato JSON-RPC 2.0 [3].

---

## 4. Resultados e Avaliação

O modelo foi avaliado em um conjunto de teste independente composto por 624 imagens. Os resultados obtidos estão apresentados na Tabela 1.

| Métrica                   | Valor |
| ------------------------- | ----- |
| Acurácia                  | 88,3% |
| AUC                       | 0,96  |
| Sensibilidade (Pneumonia) | 95%   |
| Especificidade            | 81%   |

**Tabela 1:** Métricas de performance do modelo CNN DenseNet121.

A elevada sensibilidade observada para a classe pneumonia (0,95) é particularmente relevante em cenários de triagem hospitalar, pois reduz a probabilidade de falsos negativos em casos críticos [2].

---

## 5. Conclusão

Os resultados demonstram que o AgentTriagem é uma solução viável e promissora para triagem médica automatizada. A integração de modelos de visão computacional com arquiteturas multiagente interoperáveis possibilita não apenas a detecção de doenças, mas também a orquestração inteligente do fluxo de cuidado ao paciente. O uso do MCP e do ADK estabelece uma base sólida para futuras expansões do sistema em ambientes clínicos reais.

---

## Referências Bibliográficas

[1] HUANG, G.; LIU, Z.; VAN DER MAATEN, L.; WEINBERGER, K. Q. **Densely Connected Convolutional Networks**. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017.

[2] KERMANY, D. S. et al. **Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning**. Cell, v. 172, n. 5, p. 1122–1131, 2018.

[3] ANTHROPIC. **Model Context Protocol (MCP): Specification and Open Standard**. Anthropic Engineering, 2024.

[4] GOOGLE CLOUD. **Agent Development Kit (ADK): Framework for AI Agents**. Google Developers, 2025.

[5] KUNDU, R. et al. **Pneumonia detection in chest X-ray images using an ensemble of deep learning models**. PLOS ONE, v. 16, n. 9, 2021.

[6] MOONEY, P. T. **Chest X-Ray Images (Pneumonia)**. Kaggle Dataset, 2018. Disponível em: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia.
