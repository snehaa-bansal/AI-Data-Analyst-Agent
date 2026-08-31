# AI Data Analyst Agent

An AI-powered data analysis application that transforms CSV and Excel datasets into cleaned data, statistical findings, interactive visualizations, Gemini-generated insights, and downloadable PDF reports.

The application combines deterministic analysis using Pandas and statistical methods with natural-language interpretation using the Google Gemini API.

## Key Features

* Upload CSV and Excel datasets
* Automatic dataset profiling
* Column type and uniqueness analysis
* Missing-value and duplicate detection
* Blank-text and constant-column detection
* IQR-based possible outlier identification
* Configurable data cleaning
* Numerical and categorical summaries
* Interactive Plotly visualizations
* Correlation and distribution analysis
* Gemini-powered dataset insights
* Natural-language dataset question answering
* Cleaned CSV download
* Automated PDF analysis report
* Responsive 3D glassmorphism interface

## Application Workflow

1. Upload a CSV or Excel dataset.
2. Review its structure and descriptive profile.
3. Detect missing values, duplicates, blank text, constant columns, and possible outliers.
4. Select and apply appropriate cleaning operations.
5. Explore interactive charts and correlations.
6. Generate AI-assisted interpretations using Gemini.
7. Ask natural-language questions about the dataset.
8. Download the cleaned dataset and PDF report.

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Matplotlib
* Seaborn
* SciPy
* Scikit-learn
* Google Gemini API
* ReportLab
* HTML and CSS

## Project Structure

```text
AI-Data-Analyst-Agent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
│   └── style.css
├── modules/
│   ├── __init__.py
│   ├── ai_agent.py
│   ├── chart_generator.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── data_profiler.py
│   ├── data_quality.py
│   ├── report_generator.py
│   └── statistical_analysis.py
└── .streamlit/
    └── config.toml
```

## Local Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd AI-Data-Analyst-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

The `.env` file is excluded from version control and must never be committed.

### 5. Run the application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Gemini Integration

The application sends a compact analytical context to Gemini rather than sending the complete uploaded dataset. The context includes:

* Dataset dimensions
* Column information
* Descriptive statistics
* Correlation results
* Top categorical values
* A five-row sample

Gemini provides plain-language interpretations, while all displayed statistical values are calculated programmatically.

## Data Privacy

* API keys are stored outside the source code.
* The local API key is loaded from `.env`.
* The deployed API key is stored as a protected environment variable.
* Users should avoid uploading confidential or personally identifiable datasets.
* Uploaded datasets are processed during the active application session.

## Analytical Limitations

* AI-generated explanations may occasionally require verification.
* Correlation represents association, not causation.
* IQR-based outliers are possible outliers and should not be removed without contextual review.
* Median, mean, mode, and zero imputation can influence dataset distributions.
* This application is designed for exploratory analysis and should not independently support medical, financial, legal, or other high-stakes decisions.

## Deployment

The application is designed for deployment as a Python web service on Render.

```text
Build Command:
pip install -r requirements.txt

Start Command:
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

The `GEMINI_API_KEY` must be configured securely as a Render environment variable.

## Future Enhancements

* Automated chart recommendations
* Time-series analysis
* Machine-learning model suggestions
* Additional report themes
* Larger-dataset optimization
* Role-based authentication
* Database connectivity

## Author

Sneha Bansal

## Contact

For questions, feedback, or collaboration opportunities, feel free to contact me at **[snehaabansal.11@gmail.com](mailto:snehaabansal.11@gmail.com)**.

