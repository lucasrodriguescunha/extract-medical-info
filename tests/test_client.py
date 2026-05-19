"""Tests for src/client.py — mock OpenAI calls, no API key needed."""

import json
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

from src.client import extract_from_transcription, process_dataframe, COLUMN_RENAME


def make_mock_client(arguments: dict):
    """Return OpenAI client mock that yields tool_call with given arguments."""
    tool_call = MagicMock()
    tool_call.function.arguments = json.dumps(arguments)

    choice = MagicMock()
    choice.message.tool_calls = [tool_call]

    response = MagicMock()
    response.choices = [choice]

    client = MagicMock()
    client.chat.completions.create.return_value = response
    return client


SAMPLE_EXTRACTION = {
    "age": 45,
    "recommended_treatment": "Antibiótico oral por 7 dias",
    "icd_code": "J06.9",
}


def test_extract_from_transcription_returns_dict():
    """extract_from_transcription parses tool_call JSON into dict."""
    client = make_mock_client(SAMPLE_EXTRACTION)
    result = extract_from_transcription(client, "Paciente de 45 anos com infecção respiratória.")
    assert result == SAMPLE_EXTRACTION


def test_extract_from_transcription_calls_correct_model():
    """extract_from_transcription uses gpt-4o-mini."""
    client = make_mock_client(SAMPLE_EXTRACTION)
    extract_from_transcription(client, "texto qualquer")
    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "gpt-4o-mini"


def test_extract_from_transcription_forces_tool_choice():
    """tool_choice must be 'required' to guarantee structured output."""
    client = make_mock_client(SAMPLE_EXTRACTION)
    extract_from_transcription(client, "texto qualquer")
    call_kwargs = client.chat.completions.create.call_args.kwargs
    assert call_kwargs["tool_choice"] == "required"


def test_process_dataframe_renames_columns():
    """process_dataframe returns DataFrame with Portuguese column names."""
    df_input = pd.DataFrame([
        {"transcription": "t1", "medical_specialty": "Cardiologia"},
        {"transcription": "t2", "medical_specialty": "Ortopedia"},
    ])
    client = make_mock_client(SAMPLE_EXTRACTION)

    result = process_dataframe(df_input, client)

    assert list(result.columns) == list(COLUMN_RENAME.values())


def test_process_dataframe_preserves_specialty():
    """medical_specialty from CSV row maps to especialidade_medica in output."""
    df_input = pd.DataFrame([
        {"transcription": "t1", "medical_specialty": "Cardiologia"},
    ])
    client = make_mock_client(SAMPLE_EXTRACTION)

    result = process_dataframe(df_input, client)

    assert result["especialidade_medica"].iloc[0] == "Cardiologia"


def test_process_dataframe_row_count():
    """Output row count matches input row count."""
    df_input = pd.DataFrame([
        {"transcription": f"t{i}", "medical_specialty": "Geral"} for i in range(5)
    ])
    client = make_mock_client(SAMPLE_EXTRACTION)

    result = process_dataframe(df_input, client)

    assert len(result) == 5
