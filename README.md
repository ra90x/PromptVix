# Telco Customer Churn Visualizer

This app allows you to:
- Automatically download the Telco Customer Churn dataset from Kaggle
- Preview the first 10 rows of the dataset
- Enter a visualization request in natural language
- Generate and display both the Python code and the resulting visualization using OpenAI LLM

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Usage:**
   - The app will download the dataset on launch.
   - Enter your visualization request (e.g., "Create a pie chart showing the distribution of payment methods").
   - Click "Generate Visualization" to see the code and plot.

**Note:** The OpenAI API key is set in the code. For production, use environment variables for security. 