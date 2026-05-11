# Medical Info Extractor

Extracts structured medical information from anonymized clinical transcriptions using OpenAI function calling, with automatic ICD-10 code mapping for insurance and billing workflows.

## Overview

Healthcare professionals summarize patient visits in free-text transcriptions containing symptoms, diagnoses, and treatments. This pipeline parses those transcriptions and returns structured data ready for downstream documentation systems.

**Output fields:** patient age · recommended treatment · ICD-10 code · medical specialty

## How It Works

1. Load CSV of medical transcriptions (`medical_specialty` + `transcription` columns)
2. Call `gpt-4o-mini` per row with an `extract_medical_info` tool definition
3. Parse `tool_calls[0].function.arguments` → append to results list
4. Export structured `DataFrame` with extracted fields

`tool_choice="required"` guarantees structured output — no free-text parsing.

## Setup

```bash
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_key_here
```

## Usage

```bash
python src/client.py
```

## Data

| Column | Description |
|---|---|
| `medical_specialty` | Medical specialty associated with the transcription |
| `transcription` | Full clinical transcription text |

Source: `src/data/` — CSV exported from DataLab (filename includes export timestamp).
