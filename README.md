# 📈 PromptVix - AI-Powered Data Visualization Platform

University of Liverpool | MSc Dissertation Project | Developed by Ramz A.

PromptVix is a Streamlit-based application that compares how different Large Language Models generate data visualizations from natural language prompts. The platform allows users to evaluate visualization outputs from multiple AI models and provide structured feedback on their effectiveness for business intelligence tasks.

## Overview

This research tool investigates the capabilities of contemporary LLMs in generating meaningful business visualizations. The application supports three leading models: DeepSeek v3.1, OpenAI GPT-4o, and Claude 3.7 Sonnet, enabling direct comparison of their visualization generation approaches.

## Key Features

### Multi-Model Comparison
The platform simultaneously generates visualizations from three different AI models, allowing for direct comparison of their outputs. Each model processes the same prompt independently, providing insights into varying approaches to data visualization tasks.

### Business Problem Library
The application includes 18 pre-defined business scenarios with varying complexity levels:

- Basic problems: Simple bar charts and pie charts for fundamental business questions
- Intermediate problems: Multi-dimensional scatter plots, stacked charts, and treemaps
- Advanced problems: Complex heatmaps, network analysis, and correlation studies

### Custom Prompt Support
Users can input their own natural language requests for visualizations, testing the models' ability to interpret and respond to novel prompts beyond the pre-defined scenarios.

### Comprehensive Feedback System
The platform collects structured feedback on three key dimensions:

- Visual accuracy and clarity
- Insightfulness of generated visualizations
- Business relevance and applicability

Feedback data is stored in Supabase for subsequent analysis and research purposes.

## Technical Implementation

### Architecture
The application follows a modular architecture with separate components for prompt handling, visualization generation, feedback collection, and data management. The core visualization logic processes natural language prompts and generates executable Python code using matplotlib, seaborn, and plotly libraries.

### Data Processing
The platform works with CSV datasets, with a sample Superstore dataset included for demonstration purposes. Users can upload custom datasets to test model performance across different data domains.

### Model Integration
AI models are accessed through the OpenRouter API, which provides unified access to multiple LLM providers. Each model receives identical prompts and dataset context, ensuring fair comparison conditions.


## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key
- Supabase account (for feedback storage)

### Installation

### Installation Steps

1. Clone or download the project repository
2. Install required Python packages:
//pip install -r requirements.txt

3. Configure environment variables in a .env file:

//OPENROUTER_API_KEY: Your OpenRouter API key
//SUPABASE_URL: Database connection URL
//SUPABASE_ANON_KEY: Database access key


4. Launch the application:
//streamlit run app.py


The application will be accessible at http://localhost:8501 in your web browser.

## 📋 Usage Guide

### 1. Dataset Management
- Default Dataset: Superstore_Dataset.csv (included)
- Custom Upload: Support for any CSV file
- Data Preview: First 10 rows displayed automatically

### 2. Visualization Generation

#### Option A: Pre-defined Business Problems
Select from 18 carefully crafted business scenarios:
- Easy: Basic bar charts, pie charts (Problems 1-6)
- Medium: Scatter plots, stacked charts, treemaps (Problems 7-15)
- Complex: Heatmaps, network graphs, correlation analysis (Problems 16-18)

#### Option B: Custom Prompts
Write your own visualization requests in natural language:

"Create a scatter plot showing the relationship between sales and profit, 
with point size representing quantity and color representing category"
```

### 3. Model Comparison
- Simultaneous Generation: All 3 models process your request concurrently
- Tab-based Results: Each model gets its own dedicated tab
- Side-by-side Comparison: Easy evaluation of different approaches
- Code Transparency: View and analyze generated Python code

### 4. Feedback Collection
For each model output, provide comprehensive feedback:
- Visual Accuracy (1-5): Clarity, formatting, appropriate chart type
- Visual Insightfulness (1-5): Value of insights gained
- Business Relevance (1-5): Alignment with business objectives
- Iteration Count: Number of refinements needed
- Outcome Classification: Select positive/negative aspects
- Comments: Detailed observations and suggestions

## Architecture

### Core Components


PromptVix/
├── app.py                 # Main application entry point
├── prompt_handler.py      # Core visualization logic
├── config.py              # Configuration management
├── supabase_feedback.py   # Database operations
├── analysis.py            # Feedback analysis interface
├── prompt_scenarios.py    # Business problem definitions
├── utils.py               # Utility functions
├── public/                # Model logos
│   ├── deepseek.png
│   ├── openai.png
│   └── claude.png
└── Superstore_Dataset.csv # Sample dataset


### Technology Stack
- Frontend: Streamlit
- Data Processing: Pandas, NumPy
- Visualization: Matplotlib, Seaborn, Plotly
- AI Integration: OpenRouter API
- Database: Supabase (PostgreSQL)
- Environment: Python 3.8+

## Business Problems Catalog

### Easy Complexity (Problems 1-6)
1. Profitability by Customer Segment - Bar chart analysis
2. Top 10 Products by Sales Volume - Horizontal bar chart
3. Customer Profitability Analysis - Top customers table
4. Sales Distribution Across Regions - Pie chart
5. Segment-wise Purchase Behavior - Average quantity analysis
6. Top 5 Most Profitable Cities - Geographic profitability

### Medium Complexity (Problems 7-15)
7. Profit Relationship Across Product Categories - Scatter plot
8. Regional Profit Contribution - Stacked bar chart
9. Impact of Discounts on Profit Margins - Line chart
10. Sub-Category Performance - Dual-axis line chart
11. Discount Effectiveness by Category - Grouped bar chart
12. State-Level Profitability Analysis - Treemap
13. Customer Loyalty vs. Profitability - Scatter plot
14. Product Sales Distribution by Cities - Maps
15. Product Profitability Efficiency - Profit/Sales ratio analysis

### Complex Complexity (Problems 16-18)
16. Product Sub-Category Risk Assessment - Heatmap
17. Market Basket Analysis - Network graph
18. Correlation Between Discount and Sales Volume - Pair plot

## Configuration

### Environment Variables
//env
# Required
OPENROUTER_API_KEY=your_key_here
SUPABASE_ANON_KEY=your_key_here

# Optional
SUPABASE_URL=https://nafxymsdbtdxkjknorvl.supabase.co
DEFAULT_DATASET_PATH=Superstore_Dataset.csv
MAX_TOKENS=800
TEMPERATURE=0.2
```

### Model Configuration
Models are configured in `config.py`:
//python
AVAILABLE_MODELS = {
    "DeepSeek v3.1": "deepseek/deepseek-chat-v3.1",
    "OpenAI GPT-4o": "openai/chatgpt-4o-latest",
    "Claude 3.7 Sonnet": "anthropic/claude-3.7-sonnet"
}
```

## 📈 Feedback Analysis

### Data Collection
- Structured Ratings: Numerical scores for key metrics
- Qualitative Feedback: Detailed comments and observations
- Outcome Classification: Systematic categorization of results
- Session Tracking: Unique session IDs for analysis

### Analysis Features
- Real-time Dashboard: View all submitted feedback
- CSV Export: Download feedback data for external analysis
- Filtering: Sort by date, model, or problem type
- Statistics: Aggregate ratings and outcome distributions

##  Development

### Code Quality
- PEP8 Compliant: Follows Python style guidelines
- Type Hints: Comprehensive type annotations
- Documentation: Detailed docstrings for all functions
- Error Handling: Robust exception management

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure PEP8 compliance
5. Add tests if applicable
6. Submit a pull request

## License

This project is developed as part of academic research at the University of Liverpool. Please respect the academic nature of this work.

## Support

For questions, issues, or contributions:
- GitHub Issues: Report bugs or request features
- Academic Contact: University of Liverpool
- Developer: Ramz Aftab

## Future Enhancements

- Additional LLM Models: Integration of more AI models
- Advanced Analytics: Statistical analysis of feedback patterns
- Export Features: Multiple format support (PNG, SVG, PDF)
- Collaboration: Multi-user feedback and comparison
- API Integration: RESTful API for external applications

---

PromptVix - Empowering data-driven decisions through AI-generated visualizations.