"""
Extract structured medical info from anonymized transcriptions using OpenAI function calling.

Pipeline: load CSV → call gpt-4o-mini per row → parse tool_call JSON → build DataFrame.
"""

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

TOOL_DEFINITION = [
    {
        'type': 'function',
        'function': {
            'name': 'extract_medical_info',
            'description': 'Extraia a idade do paciente, o tratamento recomendado e o código CID-10 da transcrição médica.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'age': {'type': 'number'},
                    'recommended_treatment': {'type': 'string'},
                    'icd_code': {'type': 'string'},
                },
                'required': ['age', 'recommended_treatment', 'icd_code'],
            },
        },
    }
]

COLUMN_RENAME = {
    'age': 'idade',
    'recommended_treatment': 'tratamento_recomendado',
    'icd_code': 'codigo_cid',
    'medical_specialty': 'especialidade_medica',
}


def extract_from_transcription(client: OpenAI, transcription: str) -> dict:
    """Call gpt-4o-mini and return parsed tool_call arguments dict."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extraia informações desta transcrição: {transcription}"}],
        tools=TOOL_DEFINITION,
        tool_choice="required",
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)


def process_dataframe(df: pd.DataFrame, client: OpenAI) -> pd.DataFrame:
    """Iterate rows, extract medical info, return renamed structured DataFrame."""
    results = []
    for _, row in df.iterrows():
        extracted = extract_from_transcription(client, row['transcription'])
        extracted['medical_specialty'] = row['medical_specialty']
        results.append(extracted)

    df_structured = pd.DataFrame(results)
    df_structured.rename(columns=COLUMN_RENAME, inplace=True)
    return df_structured


if __name__ == "__main__":
    client = OpenAI()
    df = pd.read_csv('src/data/datalab_export_2026-05-10 20_18_24.csv')
    df_structured = process_dataframe(df, client)
    print(df_structured.to_string())
