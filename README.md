# NYC Taxi Data Analytics Pipeline

A comprehensive data analytics pipeline for NYC Yellow Taxi trip data using modern Python tools and workflow orchestration. This project demonstrates end-to-end data processing, exploratory data analysis, and automated report generation with robust PDF conversion capabilities.

## 🚀 Project Overview

This project implements a complete data pipeline that:
- **Extracts** NYC taxi data from parquet files
- **Transforms** and cleans the data for analysis
- **Loads** processed data into SQLite database
- **Analyzes** patterns and trends through exploratory data analysis
- **Generates** professional HTML and PDF reports

## 📊 Key Features

### Data Processing
- **Robust ETL Pipeline**: Handles large datasets with memory-efficient processing
- **Data Quality Validation**: Removes invalid records and ensures data integrity
- **Temporal Feature Engineering**: Extracts time-based patterns for analysis

### Visualization & Analysis
- **Distribution Analysis**: Trip distance, duration, and fare amount patterns
- **Relationship Analysis**: Correlation between distance and fare
- **Temporal Patterns**: Hourly and daily usage trends
- **Statistical Summaries**: Comprehensive descriptive statistics

### Report Generation
- **Self-Contained HTML Reports**: No external dependencies for portability
- **PDF Conversion**: Robust PDF generation with multiple engine support
- **Base64 Image Embedding**: Solves external resource loading issues
- **Professional Styling**: Clean, modern report templates

### Workflow Orchestration
- **Prefect Integration**: Modern workflow management with logging
- **Task Dependencies**: Proper execution order and error handling
- **Configurable Parameters**: Flexible processing options

## 🏗️ Project Structure

```
NYC_Taxi_Project/
├── 📁 data/                           # Raw data storage
│   └── yellow_tripdata_2023-01.parquet
├── 📁 db/                             # Database files
│   └── nyc_taxi.db
├── 📁 flows/                          # Prefect workflow definitions
│   └── taxi_pipeline.py               # Main orchestration pipeline
├── 📁 plots/                          # Generated visualizations
│   ├── duration_distribution.png
│   ├── fare_vs_distance.png
│   ├── hourly_distribution.png
│   ├── trip_distance.png
│   └── weekday_distribution.png
├── 📁 reports/                        # Generated reports
│   ├── eda_report.html
│   └── eda_report.pdf
├── 📁 templates/                      # HTML templates
│   └── report_template.html           # Custom report template
├── 📁 utils/                          # Utility modules
│   └── eda_report_generator.py        # Report generation logic
├── 📄 clean_data.py                   # Standalone ETL script
├── 📄 eda_full.py                     # Standalone EDA script
├── 📄 mini_test.py                    # Database connection test
├── 📄 requirements.txt                # Python dependencies
└── 📄 README.md                       # Project documentation
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- wkhtmltopdf (for PDF generation)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NYC_Taxi_Project
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install wkhtmltopdf** (for PDF generation)
   - **Windows**: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   - **macOS**: `brew install wkhtmltopdf`
   - **Linux**: `sudo apt-get install wkhtmltopdf`

4. **Verify installation**
   ```bash
   python mini_test.py
   ```

## 🚀 Usage

### Option 1: Complete Pipeline (Recommended)
Run the full orchestrated pipeline with Prefect:
```bash
python flows/taxi_pipeline.py
```

### Option 2: Individual Components
Run components separately for development/testing:

**Data Cleaning:**
```bash
python clean_data.py
```

**Exploratory Data Analysis:**
```bash
python eda_full.py
```

**Database Test:**
```bash
python mini_test.py
```

## 📈 Pipeline Workflow

### 1. ETL Task (`etl_task`)
- **Extract**: Loads raw parquet data
- **Transform**: 
  - Removes invalid records (zero passengers/distance)
  - Converts datetime columns
  - Calculates trip duration
  - Optional sampling for performance
- **Load**: Saves to SQLite with chunked processing

### 2. EDA Task (`eda_task`)
- Generates comprehensive visualizations:
  - Trip distance distribution
  - Trip duration patterns
  - Fare vs distance relationships
  - Temporal usage patterns (hourly/daily)

### 3. Report Task (`report_task`)
- Creates HTML report with:
  - Dataset overview and statistics
  - Embedded visualizations (base64 encoded)
  - Professional styling and layout

### 4. PDF Conversion Task (`convert_html_to_pdf_task`)
- Converts HTML to PDF using wkhtmltopdf
- Includes fallback to weasyprint
- Windows-optimized configuration

## 🎯 Key Technical Solutions

### PDF Generation Challenges
The project addresses common PDF conversion issues that occur when using external resources:

**Problem**: wkhtmltopdf fails with "ProtocolUnknownError" when HTML contains external links (CSS, images, etc.)

**Solution**: 
1. **Self-Contained Templates**: Replaced external Bootstrap CSS with inline styles
2. **Base64 Image Embedding**: Converted all plot images to base64 data URLs
3. **Robust Error Handling**: Multiple PDF engines with graceful fallbacks
4. **Windows Optimization**: Specific wkhtmltopdf configuration for Windows environments

### HTML Template Design
The custom `report_template.html` was hand-coded to:
- Eliminate external dependencies (no CDN links)
- Use inline CSS for complete portability
- Embed images as base64 data URLs
- Maintain professional appearance
- Ensure PDF compatibility

### Memory Optimization
- **Chunked Database Writing**: Processes data in chunks to avoid SQLite limits
- **Sampling Options**: Configurable data sampling for large datasets
- **Efficient Plot Generation**: Memory-conscious visualization creation

## 📋 Configuration

### Data Processing Parameters
- `sample_size`: Number of rows to process (default: 10,000)
- `chunk_size`: Database writing chunk size (default: 500)

### PDF Generation Options
- Multiple engine support (wkhtmltopdf, weasyprint)
- Windows-optimized settings
- High-resolution output (300 DPI)
- A4 page format with proper margins

## 🔍 Data Quality Measures

The pipeline implements comprehensive data validation:
- **Passenger Count**: Removes trips with zero passengers
- **Trip Distance**: Filters out zero-distance trips
- **Duration Validation**: Excludes negative or zero-duration trips
- **Datetime Parsing**: Ensures proper timestamp formatting

## 📊 Generated Outputs

### Visualizations
1. **Trip Distance Distribution**: Histogram with KDE
2. **Trip Duration Distribution**: Histogram with KDE  
3. **Fare vs Distance**: Scatter plot with correlation
4. **Hourly Patterns**: Trip count by hour of day
5. **Weekly Patterns**: Trip count by day of week

### Reports
- **HTML Report**: Self-contained with embedded images
- **PDF Report**: High-quality PDF with proper formatting
- **Statistical Summaries**: Comprehensive descriptive statistics

## 🐛 Troubleshooting

### Common Issues

**PDF Generation Fails**
- Ensure wkhtmltopdf is installed and in PATH
- Check for external dependencies in HTML
- Verify file permissions in reports directory

**Memory Issues**
- Reduce `sample_size` parameter
- Increase `chunk_size` if database writing fails
- Monitor system memory during large dataset processing

**Import Errors**
- Verify all requirements are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

## 🔧 GitHub Setup

### Quick Setup
Run the setup script to initialize Git and prepare for GitHub:

**Windows (PowerShell):**
```powershell
.\setup_github.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x setup_github.sh
./setup_github.sh
```

### Manual Setup
1. **Initialize Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NYC Taxi Analytics Pipeline"
   ```

2. **Create GitHub repository** at https://github.com/new

3. **Connect local repo to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/NYC_Taxi_Project.git
   git branch -M main
   git push -u origin main
   ```

### Repository Features
- **Comprehensive `.gitignore`**: Excludes data files, generated outputs, and system files
- **Directory Structure**: Maintained with `.gitkeep` files
- **Documentation**: Detailed README and inline code comments
- **License**: MIT License for open source collaboration

## 🔄 Future Enhancements

- **Real-time Data Processing**: Stream processing capabilities
- **Interactive Dashboards**: Web-based analytics interface
- **Advanced ML Models**: Predictive analytics for demand forecasting
- **API Integration**: RESTful API for data access
- **Cloud Deployment**: AWS/Azure integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙋‍♂️ Support

For issues, questions, or contributions, please create an issue in the repository or contact the development team.

---

**NYC Taxi Project** - Demonstrating modern data engineering practices with Python, Prefect, and robust report generation.