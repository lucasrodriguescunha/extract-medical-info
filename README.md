# Extração de Informações Médicas com Function Calling / Medical Info Extraction with Function Calling

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![dotenv](https://img.shields.io/badge/dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

---

## PT-BR

Extrai informações médicas estruturadas de transcrições clínicas anonimizadas usando function calling da OpenAI, com mapeamento automático de códigos ICD-10 para fluxos de seguro e faturamento.

### Visão Geral

Profissionais de saúde resumem consultas em transcrições de texto livre contendo sintomas, diagnósticos e tratamentos. Este pipeline analisa essas transcrições e retorna dados estruturados prontos para sistemas de documentação.

**Campos de saída:** idade do paciente · tratamento recomendado · código ICD-10 · especialidade médica

### Como Funciona

1. Carrega CSV de transcrições médicas (colunas `medical_specialty` + `transcription`)
2. Chama `gpt-4o-mini` por linha com definição de tool `extract_medical_info`
3. Parseia `tool_calls[0].function.arguments` → adiciona à lista de resultados
4. Exporta `DataFrame` estruturado com os campos extraídos

`tool_choice="required"` garante saída estruturada — sem parsing de texto livre.

### Configuração

```bash
pip install -r requirements.txt
```

Defina sua chave da API OpenAI:

```bash
export OPENAI_API_KEY=sua_chave_aqui
```

### Uso

```bash
python src/client.py
```

### Testes

```bash
python -m pytest tests/ -v
```

Testes usam mocks do OpenAI — sem consumo de API key.

### Dados

| Coluna | Descrição |
|---|---|
| `medical_specialty` | Especialidade médica associada à transcrição |
| `transcription` | Texto completo da transcrição clínica |

Fonte: `src/data/` — CSV exportado do DataLab (nome do arquivo inclui timestamp de exportação).

---

## EN-US

Extracts structured medical information from anonymized clinical transcriptions using OpenAI function calling, with automatic ICD-10 code mapping for insurance and billing workflows.

### Overview

Healthcare professionals summarize patient visits in free-text transcriptions containing symptoms, diagnoses, and treatments. This pipeline parses those transcriptions and returns structured data ready for downstream documentation systems.

**Output fields:** patient age · recommended treatment · ICD-10 code · medical specialty

### How It Works

1. Load CSV of medical transcriptions (`medical_specialty` + `transcription` columns)
2. Call `gpt-4o-mini` per row with an `extract_medical_info` tool definition
3. Parse `tool_calls[0].function.arguments` → append to results list
4. Export structured `DataFrame` with extracted fields

`tool_choice="required"` guarantees structured output — no free-text parsing.

### Setup

```bash
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_key_here
```

### Usage

```bash
python src/client.py
```

### Tests

```bash
python -m pytest tests/ -v
```

Tests mock OpenAI — no API key consumed.

### Data

| Column | Description |
|---|---|
| `medical_specialty` | Medical specialty associated with the transcription |
| `transcription` | Full clinical transcription text |

Source: `src/data/` — CSV exported from DataLab (filename includes export timestamp).
