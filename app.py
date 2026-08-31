import streamlit as st

from modules.data_loader import load_dataset
from pathlib import Path
from modules.report_generator import generate_pdf_report
from modules.ai_agent import (
    generate_dataset_insights,
    answer_dataset_question,
)
from modules.statistical_analysis import (
    calculate_numeric_statistics,
    get_distribution_analysis,
    find_correlations,
)
from modules.data_cleaner import clean_dataset
from modules.chart_generator import (
    get_column_types,
    create_histogram,
    create_box_plot,
    create_scatter_plot,
    create_line_chart,
    create_bar_chart,
    create_correlation_heatmap,
)
from modules.data_quality import detect_data_quality_issues
from modules.data_profiler import (
    get_dataset_summary,
    get_column_information,
    get_numeric_summary,
    get_categorical_summary,
)

def load_custom_css():
    css_path = Path("assets/style.css")

    if css_path.exists():
        with open(
            css_path,
            "r",
            encoding="utf-8",
        ) as css_file:
            st.markdown(
                f"<style>{css_file.read()}</style>",
                unsafe_allow_html=True,
            )


st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide",
)

load_custom_css()


st.markdown(
    """
<div class="hero-3d">
<div class="hero-copy-3d">
<div class="hero-badge-3d"><span class="badge-dot"></span>INTELLIGENT ANALYTICS WORKSPACE</div>
<h1 class="hero-title-3d">Turn Data Into <span class="gradient-word">Decisions.</span></h1>
<p class="hero-description-3d">An autonomous AI data analyst that cleans datasets, discovers statistical patterns, builds interactive visualizations and explains results using Gemini.</p>
<div class="hero-features">
<span class="feature-pill">Automatic Profiling</span>
<span class="feature-pill">Smart Cleaning</span>
<span class="feature-pill">Interactive Charts</span>
<span class="feature-pill">Gemini Insights</span>
</div>
</div>
<div class="analytics-scene">
<div class="dashboard-object">
<div class="dashboard-top">
<span>LIVE ANALYTICS</span>
<div class="dashboard-dots"><span></span><span></span><span></span></div>
</div>
<div class="mini-chart">
<span class="chart-bar"></span>
<span class="chart-bar"></span>
<span class="chart-bar"></span>
<span class="chart-bar"></span>
<span class="chart-bar"></span>
<span class="chart-bar"></span>
<span class="chart-bar"></span>
</div>
<div class="dashboard-bottom">
<div class="small-stat"><strong>PROFILE</strong><span>DATA QUALITY</span></div>
<div class="small-stat"><strong>ANALYSE</strong><span>AI INSIGHTS</span></div>
<div class="small-stat"><strong>VISUALISE</strong><span>SMART CHARTS</span></div>
</div>
</div>
<div class="floating-card float-one">AI INSIGHTS ✦</div>
<div class="floating-card float-two">DATA CLEANED ✓</div>
<div class="floating-card float-three">LIVE ANALYSIS</div>
</div>
</div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">
            📊 Analysis Workflow
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="workflow-step">1. Upload Dataset</div>
        <div class="workflow-step">2. Profile Data</div>
        <div class="workflow-step">3. Check Quality</div>
        <div class="workflow-step">4. Clean Dataset</div>
        <div class="workflow-step">5. Generate Charts</div>
        <div class="workflow-step">6. Analyse Statistics</div>
        <div class="workflow-step">7. Generate AI Insights</div>
        <div class="workflow-step">8. Download Report</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Technology")

    st.caption(
        """
        Python • Pandas • Plotly • Streamlit •
        Gemini API • ReportLab
        """
    )

    st.divider()

    st.caption(
        "AI Data Analyst Agent | Portfolio Project"
    )


uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"],
)

if uploaded_file is None:
    st.sidebar.info("Waiting for a dataset")
else:
    st.sidebar.success(
        f"Loaded: {uploaded_file.name}"
    )


if uploaded_file is None:
    st.info("Upload a CSV or Excel dataset to begin.")

else:
    try:
        df = load_dataset(uploaded_file)

        if df.empty:
            st.warning("The uploaded dataset is empty.")
            st.stop()

        st.success(
            f"Successfully loaded: {uploaded_file.name}"
        )

        summary = get_dataset_summary(df)

        st.subheader("Dataset Overview")

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "Rows",
            f"{summary['rows']:,}",
        )

        metric2.metric(
            "Columns",
            f"{summary['columns']:,}",
        )

        metric3.metric(
            "Missing Values",
            f"{summary['missing_values']:,}",
        )

        metric4.metric(
            "Duplicate Rows",
            f"{summary['duplicate_rows']:,}",
        )

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "Data Preview",
    "Column Information",
    "Numerical Statistics",
    "Categorical Statistics",
    "Data Quality",
    "Data Cleaning",
    "Visualizations",
    "Statistical Analysis",
    "AI Agent",
    "Report",
])

        with tab1:
            st.subheader("Dataset Preview")

            number_of_rows = st.slider(
                "Number of rows to display",
                min_value=5,
                max_value=min(100, len(df)),
                value=min(10, len(df)),
            )

            st.dataframe(
                df.head(number_of_rows),
                use_container_width=True,
            )

        with tab2:
            st.subheader("Column Information")

            column_information = get_column_information(df)

            st.dataframe(
                column_information,
                use_container_width=True,
                hide_index=True,
            )

        with tab3:
            st.subheader("Numerical Statistics")

            numeric_summary = get_numeric_summary(df)

            if numeric_summary.empty:
                st.info(
                    "The dataset does not contain numerical columns."
                )
            else:
                st.dataframe(
                    numeric_summary,
                    use_container_width=True,
                )

        with tab4:
            st.subheader("Categorical Statistics")

            categorical_summary = get_categorical_summary(df)

            if categorical_summary.empty:
                st.info(
                    "The dataset does not contain categorical columns."
                )
            else:
                st.dataframe(
                    categorical_summary,
                    use_container_width=True,
                    hide_index=True,
                )

        with tab5:
            st.subheader("Automatic Data-Quality Report")

            quality_issues = detect_data_quality_issues(df)

            if quality_issues.empty:
                st.success(
                    "No common data-quality problems were detected."
                )

            else:
                issue1, issue2, issue3 = st.columns(3)

                issue1.metric(
                    "Detected Issues",
                    len(quality_issues),
                )

                issue2.metric(
                    "Affected Columns",
                    quality_issues["Column"].nunique(),
                )

                issue3.metric(
                    "Issue Categories",
                    quality_issues["Issue Type"].nunique(),
                )

                selected_issue = st.selectbox(
                    "Filter by issue type",
                    options=[
                        "All Issues",
                        *quality_issues[
                            "Issue Type"
                        ].unique().tolist(),
                    ],
                )

                if selected_issue == "All Issues":
                    displayed_issues = quality_issues
                else:
                    displayed_issues = quality_issues[
                        quality_issues["Issue Type"]
                        == selected_issue
                    ]

                st.dataframe(
                    displayed_issues,
                    use_container_width=True,
                    hide_index=True,
                )

                st.warning(
                    """
                    Possible outliers are observations identified
                    using the IQR rule. They should be reviewed and
                    should not automatically be deleted.
                    """
                )

        with tab6:
            st.subheader("Automatic Data Cleaning")

            st.write(
                """
                Select the operations you want to apply. The
                original uploaded dataset will remain unchanged.
                """
            )

            option1, option2, option3 = st.columns(3)

            with option1:
                convert_blanks = st.checkbox(
                    "Convert blank text to missing values",
                    value=True,
                )

            with option2:
                remove_duplicates = st.checkbox(
                    "Remove duplicate rows",
                    value=True,
                )

            with option3:
                remove_empty = st.checkbox(
                    "Remove completely empty rows and columns",
                    value=True,
                )

            method1, method2 = st.columns(2)

            with method1:
                numeric_method = st.selectbox(
                    "Numerical missing-value method",
                    options=[
                        "Median",
                        "Mean",
                        "Zero",
                        "Do Not Fill",
                    ],
                )

            with method2:
                categorical_method = st.selectbox(
                    "Categorical missing-value method",
                    options=[
                        "Mode",
                        "Unknown",
                        "Do Not Fill",
                    ],
                )

            st.info(
                """
                Median is generally safer for numerical columns
                containing extreme values. Possible outliers will
                not be removed automatically.
                """
            )

            if st.button(
                "Clean Dataset",
                type="primary",
                use_container_width=True,
            ):
                cleaned_df, cleaning_log = clean_dataset(
                    df=df,
                    convert_blanks=convert_blanks,
                    remove_duplicates=remove_duplicates,
                    remove_empty=remove_empty,
                    numeric_method=numeric_method,
                    categorical_method=categorical_method,
                )

                st.session_state["cleaned_df"] = cleaned_df
                st.session_state["cleaning_log"] = cleaning_log
                st.session_state["cleaned_source"] = (
                    uploaded_file.name
                )

            cleaned_available = (
                "cleaned_df" in st.session_state
                and st.session_state.get("cleaned_source")
                == uploaded_file.name
            )

            if cleaned_available:
                cleaned_df = st.session_state["cleaned_df"]
                cleaning_log = st.session_state["cleaning_log"]

                st.success(
                    "Dataset cleaned successfully."
                )

                before1, before2, before3 = st.columns(3)

                before1.metric(
                    "Rows After Cleaning",
                    f"{len(cleaned_df):,}",
                    delta=len(cleaned_df) - len(df),
                )

                before2.metric(
                    "Columns After Cleaning",
                    f"{cleaned_df.shape[1]:,}",
                    delta=cleaned_df.shape[1] - df.shape[1],
                )

                before3.metric(
                    "Missing Values Remaining",
                    f"{cleaned_df.isnull().sum().sum():,}",
                )

                st.subheader("Cleaning Log")

                for message in cleaning_log:
                    st.write(f"✅ {message}")

                st.subheader("Cleaned Dataset Preview")

                st.dataframe(
                    cleaned_df.head(20),
                    use_container_width=True,
                )

                cleaned_csv = cleaned_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Cleaned Dataset",
                    data=cleaned_csv,
                    file_name="cleaned_dataset.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        with tab7:
            st.subheader("Interactive Chart Generator")

            cleaned_available = (
                "cleaned_df" in st.session_state
                and st.session_state.get("cleaned_source")
                == uploaded_file.name
            )

            available_sources = ["Original Dataset"]

            if cleaned_available:
                available_sources.append("Cleaned Dataset")

            chart_source = st.radio(
                "Select data source",
                options=available_sources,
                horizontal=True,
            )

            if chart_source == "Cleaned Dataset":
                chart_df = st.session_state["cleaned_df"]
            else:
                chart_df = df

            numerical_columns, categorical_columns = (
                get_column_types(chart_df)
            )

            chart_type = st.selectbox(
                "Select chart type",
                options=[
                    "Histogram",
                    "Box Plot",
                    "Scatter Plot",
                    "Line Chart",
                    "Bar Chart",
                    "Correlation Heatmap",
                ],
            )

            figure = None

            if chart_type == "Histogram":
                if numerical_columns:
                    selected_column = st.selectbox(
                        "Select a numerical column",
                        numerical_columns,
                        key="histogram_column",
                    )

                    figure = create_histogram(
                        chart_df,
                        selected_column,
                    )
                else:
                    st.warning(
                        "No numerical columns are available."
                    )

            elif chart_type == "Box Plot":
                if numerical_columns:
                    selected_column = st.selectbox(
                        "Select a numerical column",
                        numerical_columns,
                        key="box_column",
                    )

                    figure = create_box_plot(
                        chart_df,
                        selected_column,
                    )
                else:
                    st.warning(
                        "No numerical columns are available."
                    )

            elif chart_type == "Scatter Plot":
                if len(numerical_columns) >= 2:
                    chart1, chart2 = st.columns(2)

                    with chart1:
                        x_column = st.selectbox(
                            "Select X-axis",
                            numerical_columns,
                            key="scatter_x",
                        )

                    with chart2:
                        y_column = st.selectbox(
                            "Select Y-axis",
                            numerical_columns,
                            index=1,
                            key="scatter_y",
                        )

                    figure = create_scatter_plot(
                        chart_df,
                        x_column,
                        y_column,
                    )
                else:
                    st.warning(
                        "At least two numerical columns are required."
                    )

            elif chart_type == "Line Chart":
                if len(numerical_columns) >= 2:
                    line1, line2 = st.columns(2)

                    with line1:
                        x_column = st.selectbox(
                            "Select X-axis",
                            numerical_columns,
                            key="line_x",
                        )

                    with line2:
                        y_column = st.selectbox(
                            "Select Y-axis",
                            numerical_columns,
                            index=1,
                            key="line_y",
                        )

                    figure = create_line_chart(
                        chart_df,
                        x_column,
                        y_column,
                    )
                else:
                    st.warning(
                        "At least two numerical columns are required."
                    )

            elif chart_type == "Bar Chart":
                if categorical_columns:
                    selected_column = st.selectbox(
                        "Select a categorical column",
                        categorical_columns,
                        key="bar_column",
                    )

                    figure = create_bar_chart(
                        chart_df,
                        selected_column,
                    )
                else:
                    st.warning(
                        "No categorical columns are available."
                    )

            elif chart_type == "Correlation Heatmap":
                figure = create_correlation_heatmap(
                    chart_df
                )

                if figure is None:
                    st.warning(
                        "At least two numerical columns are required."
                    )

            if figure is not None:
                st.plotly_chart(
                    figure,
                    use_container_width=True,
                )

        with tab8:
            st.subheader("Automatic Statistical Analysis")

            cleaned_available = (
                "cleaned_df" in st.session_state
                and st.session_state.get("cleaned_source")
                == uploaded_file.name
            )

            statistical_sources = ["Original Dataset"]

            if cleaned_available:
                statistical_sources.append("Cleaned Dataset")

            statistical_source = st.radio(
                "Select analysis data",
                options=statistical_sources,
                horizontal=True,
                key="statistical_source",
            )

            if statistical_source == "Cleaned Dataset":
                analysis_df = st.session_state["cleaned_df"]
            else:
                analysis_df = df

            statistical_tab1, statistical_tab2, statistical_tab3 = (
                st.tabs([
                    "Statistical Measures",
                    "Distribution Analysis",
                    "Correlation Analysis",
                ])
            )

            with statistical_tab1:
                st.write(
                    """
                    Statistical measures describe the centre,
                    spread and shape of every numerical column.
                    """
                )

                numeric_statistics = (
                    calculate_numeric_statistics(analysis_df)
                )

                if numeric_statistics.empty:
                    st.info(
                        "No numerical columns are available."
                    )
                else:
                    st.dataframe(
                        numeric_statistics,
                        use_container_width=True,
                        hide_index=True,
                    )

            with statistical_tab2:
                st.write(
                    """
                    Skewness indicates whether values are balanced
                    or concentrated more heavily on one side.
                    """
                )

                distribution_analysis = (
                    get_distribution_analysis(analysis_df)
                )

                if distribution_analysis.empty:
                    st.info(
                        "No numerical columns are available."
                    )
                else:
                    st.dataframe(
                        distribution_analysis,
                        use_container_width=True,
                        hide_index=True,
                    )

            with statistical_tab3:
                correlation_threshold = st.slider(
                    "Minimum absolute correlation",
                    min_value=0.10,
                    max_value=0.95,
                    value=0.50,
                    step=0.05,
                )

                correlation_results = find_correlations(
                    analysis_df,
                    threshold=correlation_threshold,
                )

                if correlation_results.empty:
                    st.info(
                        "No relationships meet the selected "
                        "correlation threshold."
                    )
                else:
                    relationship1, relationship2 = st.columns(2)

                    relationship1.metric(
                        "Relationships Found",
                        len(correlation_results),
                    )

                    relationship2.metric(
                        "Strongest Correlation",
                        correlation_results.iloc[0][
                            "Correlation"
                        ],
                    )

                    st.dataframe(
                        correlation_results,
                        use_container_width=True,
                        hide_index=True,
                    )

                st.caption(
                    """
                    Correlation measures association, not causation.
                    Identifier columns such as product IDs may
                    produce meaningless correlations and should be
                    interpreted carefully.
                    """
                )

        with tab9:
            st.subheader("Gemini AI Data Analyst")

            st.write(
                """
                Generate an AI explanation of the dataset or ask
                a question about its patterns and statistics.
                """
            )

            cleaned_available = (
                "cleaned_df" in st.session_state
                and st.session_state.get("cleaned_source")
                == uploaded_file.name
            )

            ai_sources = ["Original Dataset"]

            if cleaned_available:
                ai_sources.append("Cleaned Dataset")

            ai_source = st.radio(
                "Select data for AI analysis",
                options=ai_sources,
                horizontal=True,
                key="ai_source",
            )

            if ai_source == "Cleaned Dataset":
                ai_df = st.session_state["cleaned_df"]
            else:
                ai_df = df

            st.caption(
                """
                Only dataset summaries and a five-row sample are
                sent to Gemini—not the complete uploaded file.
                Avoid using confidential or personally identifiable
                data with an external AI service.
                """
            )

            ai_tab1, ai_tab2 = st.tabs([
                "Generate Insights",
                "Ask the Dataset",
            ])

            with ai_tab1:
                if st.button(
                    "Generate AI Insights",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        with st.spinner(
                            "Gemini is analysing the dataset..."
                        ):
                            insights = generate_dataset_insights(
                                ai_df
                            )

                        st.session_state["ai_insights"] = insights
                        st.session_state["ai_insight_source"] = (
                            uploaded_file.name
                        )

                    except Exception as error:
                        st.error(
                            f"Gemini could not generate insights: "
                            f"{error}"
                        )

                if (
                    "ai_insights" in st.session_state
                    and st.session_state.get(
                        "ai_insight_source"
                    ) == uploaded_file.name
                ):
                    st.markdown(
                        st.session_state["ai_insights"]
                    )

            with ai_tab2:
                dataset_question = st.text_area(
                    "Ask a question about the dataset",
                    placeholder=(
                        "For example: Which variables have the "
                        "strongest relationships?"
                    ),
                )

                if st.button(
                    "Ask Gemini",
                    use_container_width=True,
                ):
                    try:
                        with st.spinner(
                            "Gemini is examining the summary..."
                        ):
                            answer = answer_dataset_question(
                                ai_df,
                                dataset_question,
                            )

                        st.session_state[
                            "dataset_answer"
                        ] = answer

                    except Exception as error:
                        st.error(
                            f"Gemini could not answer: {error}"
                        )

                if "dataset_answer" in st.session_state:
                    st.markdown(
                        st.session_state["dataset_answer"]
                    )

        with tab10:
            st.subheader("Automated Analysis Report")

            cleaned_available = (
                "cleaned_df" in st.session_state
                and st.session_state.get("cleaned_source")
                == uploaded_file.name
            )

            report_sources = ["Original Dataset"]

            if cleaned_available:
                report_sources.append("Cleaned Dataset")

            report_source = st.radio(
                "Select report data",
                options=report_sources,
                horizontal=True,
                key="report_source",
            )

            if report_source == "Cleaned Dataset":
                report_df = st.session_state["cleaned_df"]
                report_cleaning_log = st.session_state.get(
                    "cleaning_log",
                    [],
                )
            else:
                report_df = df
                report_cleaning_log = []

            include_ai = st.checkbox(
                "Include generated Gemini insights",
                value=True,
            )

            available_ai_insights = st.session_state.get(
                "ai_insights"
            )

            if include_ai and not available_ai_insights:
                st.info(
                    """
                    Generate insights in the AI Agent tab first
                    if you want them included in the report.
                    The report can still be created without them.
                    """
                )

            if st.button(
                "Generate PDF Report",
                type="primary",
                use_container_width=True,
            ):
                try:
                    with st.spinner(
                        "Creating the analysis report..."
                    ):
                        report_pdf = generate_pdf_report(
                            df=report_df,
                            dataset_name=uploaded_file.name,
                            cleaning_log=report_cleaning_log,
                            ai_insights=(
                                available_ai_insights
                                if include_ai
                                else None
                            ),
                        )

                    st.session_state["report_pdf"] = report_pdf
                    st.session_state["report_source_file"] = (
                        uploaded_file.name
                    )

                    st.success(
                        "PDF report generated successfully."
                    )

                except Exception as error:
                    st.error(
                        f"Unable to create report: {error}"
                    )

            if (
                "report_pdf" in st.session_state
                and st.session_state.get(
                    "report_source_file"
                ) == uploaded_file.name
            ):
                st.download_button(
                    label="Download PDF Report",
                    data=st.session_state["report_pdf"],
                    file_name="AI_Data_Analyst_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

    except Exception as error:
        st.error(
            f"Unable to process the uploaded file: {error}"
        )