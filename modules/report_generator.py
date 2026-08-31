from io import BytesIO
from html import escape
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def safe_text(value):
    """Prepare text for ReportLab's standard fonts."""

    text = str(value)

    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2022": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.encode(
        "latin-1",
        errors="replace",
    ).decode("latin-1")

    return escape(text)


def add_page_number(canvas, document):
    """Add a footer and page number."""

    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))

    canvas.drawString(
        1.5 * cm,
        0.8 * cm,
        "AI Data Analyst Agent",
    )

    canvas.drawRightString(
        landscape(A4)[0] - 1.5 * cm,
        0.8 * cm,
        f"Page {document.page}",
    )

    canvas.restoreState()


def dataframe_table(
    dataframe,
    body_style,
    header_style,
    maximum_rows=20,
):
    """Convert a DataFrame into a styled PDF table."""

    displayed_df = dataframe.head(maximum_rows).copy()

    table_data = [
        [
            Paragraph(
                safe_text(column),
                header_style,
            )
            for column in displayed_df.columns
        ]
    ]

    for _, row in displayed_df.iterrows():
        table_data.append([
            Paragraph(
                safe_text(value),
                body_style,
            )
            for value in row
        ])

    available_width = landscape(A4)[0] - (3 * cm)
    column_width = available_width / len(displayed_df.columns)

    table = Table(
        table_data,
        colWidths=[
            column_width
            for _ in displayed_df.columns
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1E3A5F"),
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#F8FAFC"),
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#CBD5E1"),
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),
        ])
    )

    return table


def find_top_correlations(df, limit=15):
    """Return the strongest numerical correlations."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return pd.DataFrame()

    correlation_matrix = numeric_df.corr()
    results = []

    columns = correlation_matrix.columns

    for first_index in range(len(columns)):
        for second_index in range(
            first_index + 1,
            len(columns),
        ):
            first_column = columns[first_index]
            second_column = columns[second_index]

            correlation = correlation_matrix.loc[
                first_column,
                second_column,
            ]

            if pd.isna(correlation):
                continue

            results.append({
                "First Column": first_column,
                "Second Column": second_column,
                "Correlation": round(correlation, 4),
                "Direction": (
                    "Positive"
                    if correlation > 0
                    else "Negative"
                ),
            })

    if not results:
        return pd.DataFrame()

    results_df = pd.DataFrame(results)

    results_df["Absolute Value"] = (
        results_df["Correlation"].abs()
    )

    return (
        results_df
        .sort_values("Absolute Value", ascending=False)
        .drop(columns="Absolute Value")
        .head(limit)
        .reset_index(drop=True)
    )


def generate_pdf_report(
    df,
    dataset_name,
    cleaning_log=None,
    ai_insights=None,
):
    """Generate the complete PDF analysis report."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="AI Data Analyst Report",
        author="AI Data Analyst Agent",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#1E3A5F"),
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=29,
        spaceAfter=14,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#1E3A5F"),
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        spaceBefore=10,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
    )

    paragraph_style = ParagraphStyle(
        "ReportParagraph",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        spaceAfter=7,
    )

    header_style = ParagraphStyle(
        "TableHeader",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        alignment=1,
    )

    story = []

    story.append(
        Paragraph(
            "AI Data Analyst Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Dataset:</b> {safe_text(dataset_name)}",
            paragraph_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Generated:</b> "
            + safe_text(
                datetime.now().strftime(
                    "%d %B %Y, %I:%M %p"
                )
            ),
            paragraph_style,
        )
    )

    story.append(Spacer(1, 10))

    # Dataset overview
    story.append(
        Paragraph("1. Dataset Overview", heading_style)
    )

    overview_df = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Numerical Columns",
            "Categorical Columns",
            "Missing Values",
            "Duplicate Rows",
        ],
        "Value": [
            len(df),
            df.shape[1],
            df.select_dtypes(
                include="number"
            ).shape[1],
            df.select_dtypes(
                exclude="number"
            ).shape[1],
            int(df.isnull().sum().sum()),
            int(df.duplicated().sum()),
        ],
    })

    story.append(
        dataframe_table(
            overview_df,
            body_style,
            header_style,
        )
    )

    story.append(Spacer(1, 12))

    # Data quality
    story.append(
        Paragraph("2. Data Quality", heading_style)
    )

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean()
            .mul(100)
            .round(2)
            .values
        ),
        "Unique Values": (
            df.nunique(dropna=True).values
        ),
    })

    missing_df = (
        missing_df
        .sort_values(
            "Missing Values",
            ascending=False,
        )
        .head(20)
    )

    story.append(
        dataframe_table(
            missing_df,
            body_style,
            header_style,
        )
    )

    # Cleaning log
    if cleaning_log:
        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                "Cleaning Operations",
                heading_style,
            )
        )

        for operation in cleaning_log:
            story.append(
                Paragraph(
                    "- " + safe_text(operation),
                    paragraph_style,
                )
            )

    story.append(PageBreak())

    # Numerical statistics
    story.append(
        Paragraph(
            "3. Numerical Statistics",
            heading_style,
        )
    )

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        story.append(
            Paragraph(
                "No numerical columns were available.",
                paragraph_style,
            )
        )
    else:
        numerical_statistics = pd.DataFrame({
            "Column": numeric_df.columns,
            "Mean": numeric_df.mean().round(3).values,
            "Median": numeric_df.median().round(3).values,
            "Std. Dev.": numeric_df.std().round(3).values,
            "Minimum": numeric_df.min().round(3).values,
            "Maximum": numeric_df.max().round(3).values,
            "Skewness": numeric_df.skew().round(3).values,
        })

        story.append(
            dataframe_table(
                numerical_statistics,
                body_style,
                header_style,
                maximum_rows=40,
            )
        )

    story.append(Spacer(1, 14))

    # Correlations
    story.append(
        Paragraph(
            "4. Strongest Numerical Relationships",
            heading_style,
        )
    )

    correlation_df = find_top_correlations(df)

    if correlation_df.empty:
        story.append(
            Paragraph(
                "No numerical correlations were available.",
                paragraph_style,
            )
        )
    else:
        story.append(
            dataframe_table(
                correlation_df,
                body_style,
                header_style,
            )
        )

        story.append(
            Paragraph(
                "Note: Correlation indicates association and "
                "does not by itself establish causation.",
                paragraph_style,
            )
        )

    # Gemini insights
    if ai_insights:
        story.append(PageBreak())

        story.append(
            Paragraph(
                "5. Gemini AI Insights",
                heading_style,
            )
        )

        for line in ai_insights.splitlines():
            cleaned_line = line.strip()
            cleaned_line = (
                cleaned_line
                .replace("**", "")
                .replace("__", "")
                .replace("`", "")
            )

            if not cleaned_line:
                story.append(Spacer(1, 5))
                continue

            if cleaned_line.startswith("#"):
                cleaned_line = cleaned_line.lstrip("#").strip()

                story.append(
                    Paragraph(
                        safe_text(cleaned_line),
                        heading_style,
                    )
                )

            else:
                cleaned_line = cleaned_line.lstrip(
                    "-* "
                )

                story.append(
                    Paragraph(
                        safe_text(cleaned_line),
                        paragraph_style,
                    )
                )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes