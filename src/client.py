import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

df = pd.read_csv('src/data/datalab_export_2026-05-10 20_18_24.csv')

function_definition = []

function_definition.append({
    'type': 'function',
    'function': {
        'name': 'extract_medical_info',
        'description': 'Extraia a idade do paciente, o tratamento recomendado e o código CID-10 da transcrição médica.',
        'parameters': {
            'type': 'object',
            'properties': {
                'age': {
                    'type': 'number'
                },
                'recommended_treatment': {
                    'type': 'string',
                },
                'icd_code': {
                    'type': 'string'
                }
            }
        }
    }
})

results = []

for index, row in df.iterrows():
    transcription = row['transcription']
    specialty = row['medical_specialty']

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Extraia informações desta transcrição: {transcription}"
            }
        ],
        tools=function_definition,
        tool_choice="required"
    )

    tool_call = response.choices[0].message.tool_calls[0]
    extracted = json.loads(tool_call.function.arguments)

    extracted['medical_specialty'] = specialty
    results.append(extracted)

df_structured = pd.DataFrame(results)

print(df_structured.head())
