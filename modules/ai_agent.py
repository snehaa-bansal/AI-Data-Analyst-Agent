import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()


MODEL_NAME = "gemini-3.1-flash-lite"


def get_gemini_client():
    """
    Create a Gemini client using either the local .env file
    or Streamlit Cloud secrets.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except (
            KeyError,
            FileNotFoundError,
        ):
            api_key = None

    if not api_key:
        raise ValueError(
            "Gemini API key was not found. Configure "
            "GEMINI_API_KEY in .env locally or in "
            "Streamlit Cloud secrets."
        )

    return genai.Client(api_key=api_key)

def create_dataset_context(df):
    """
    Create a compact dataset summary for Gemini.

    Only summaries and a small sample are sent instead
    of the complete dataset.
    """

    numeric_df = df.select_dtypes(include="number")

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns

    column_information = pd.DataFrame({
        "column": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "missing_values": df.isnull().sum().values,
        "unique_values": df.nunique(dropna=True).values,
    })

    if numeric_df.empty:
        numeric_summary = "No numerical columns"
        correlation_summary = "No numerical correlations"
    else:
        numeric_summary = (
            numeric_df.describe()
            .T
            .round(3)
            .to_string()
        )

        correlation_summary = (
            numeric_df.corr()
            .round(3)
            .to_string()
        )

    categorical_summaries = []

    for column in categorical_columns[:10]:
        top_values = (
            df[column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(5)
            .to_dict()
        )

        categorical_summaries.append(
            f"{column}: {top_values}"
        )

    categorical_summary = "\n".join(
        categorical_summaries
    )

    dataset_sample = (
        df.head(5)
        .astype(str)
        .to_csv(index=False)
    )

    context = f"""
DATASET DIMENSIONS
Rows: {df.shape[0]}
Columns: {df.shape[1]}

COLUMN INFORMATION
{column_information.to_string(index=False)}

NUMERICAL SUMMARY
{numeric_summary}

CORRELATION MATRIX
{correlation_summary}

TOP CATEGORICAL VALUES
{categorical_summary}

SMALL DATA SAMPLE
{dataset_sample}
"""

    return context


def generate_dataset_insights(df):
    """
    Ask Gemini to generate structured analytical insights.
    """

    client = get_gemini_client()
    dataset_context = create_dataset_context(df)

    prompt = f"""
You are an AI data analyst.

Analyse the dataset summary provided below. Base every
conclusion only on the supplied information.

Provide the response using these headings:

## Executive Summary
Give a short overview of the dataset.

## Data Quality Findings
Explain important missing-value, uniqueness or data-type
issues.

## Numerical Insights
Explain important numerical patterns and distributions.

## Categorical Insights
Explain important categorical patterns.

## Relationships
Explain meaningful correlations without claiming causation.

## Recommended Actions
Provide practical next analytical or cleaning steps.

Important rules:
- Do not invent facts.
- Clearly state when evidence is insufficient.
- Treat identifier columns carefully.
- Use straightforward professional language.
- Do not claim that correlation proves causation.

DATASET SUMMARY:
{dataset_context}
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        store=False,
    )

    return interaction.output_text


def answer_dataset_question(df, question):
    """
    Answer a user's question using the dataset summary.
    """

    if not question.strip():
        raise ValueError("Enter a question first.")

    client = get_gemini_client()
    dataset_context = create_dataset_context(df)

    prompt = f"""
You are an AI data analyst.

Answer the user's question using only the dataset summary
provided below.

If the summary does not contain enough information, explain
what additional calculation or data would be required.

Do not invent values. Do not claim that correlation proves
causation.

USER QUESTION:
{question}

DATASET SUMMARY:
{dataset_context}
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        store=False,
    )

    return interaction.output_text