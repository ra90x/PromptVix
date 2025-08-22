import os
import json
import re
import requests
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from datetime import datetime
from feedback_db import save_feedback
from utils import load_default_dataset, is_code_safe
import sqlite3
from prompt_scenarios import business_problems
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL, DEFAULT_DATASET_PATH, MAX_TOKENS, TEMPERATURE, DB_NAME
import plotly.graph_objects as go

# Configure matplotlib for Streamlit compatibility
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Streamlit

def handle_prompt_tab():
    # Set up the Streamlit app title and subtitle
    st.title("📈 PromptVix")
    st.subheader("IT Artefact | Developed by Ramz A.", divider=True)

    # Streamlit app configuration

    @st.cache_data(show_spinner=True)
    def load_data():
        """Load the default dataset or return an error if not found."""
        if not os.path.exists(DEFAULT_DATASET_PATH):
            st.error(f"Dataset file not found at: {DEFAULT_DATASET_PATH}")
            return None
        try:
            df = pd.read_csv(DEFAULT_DATASET_PATH, encoding='latin1')
            df.to_csv('cleaned_file.csv', encoding='utf-8', index=False)
            return df
        except Exception as e:
            st.error(f"Failed to read CSV file: {e}")
            return None

    # Allow dataset upload or use default
    df = None
    st.subheader("Upload Dataset (optional)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Failed to read uploaded CSV: {e}")
            df = None
    else:
        df = load_data()

    if st.button("Reload Dataset"):
        st.cache_data.clear()
        df = load_data()

    if df is not None:
        st.subheader("Data Preview:")
        st.dataframe(df.head(10))

        # --- Business Problem Dropdown and Custom Prompt Toggle ---
        st.subheader("Select a Business Problem or Write Your Own Prompt:")
        
        selected_problem = st.selectbox(
            "Choose a Business Problem:",
            list(business_problems.keys()),
            key="business_problem_select"
        )
        # Display details of the selected business problem
        details = business_problems[selected_problem]
        st.info(f"**Visualization Type:** {details['Visualization Type']}\n**Complexity:** {details['Complexity']}")

        # Toggle for custom prompt input
        use_custom_prompt = st.checkbox("Write your own prompt instead", value=False)
        if use_custom_prompt:
            if 'user_request' not in st.session_state:
                st.session_state['user_request'] = selected_problem + " using " + details['Visualization Type']
            user_request = st.text_area(
                "🚀 Enter your custom prompt:",
                key='user_request',
                height=100
            )
            prompt_to_use = user_request
        else:
            prompt_to_use = selected_problem + " using " + details['Visualization Type']

        # Use session_state to persist generated_code
        if 'generated_code' not in st.session_state:
            st.session_state['generated_code'] = None
        vis_error = None

        if st.button("Generate Visualization") and prompt_to_use:
            if not prompt_to_use.strip():
                st.error("Please enter a valid visualization request.")
            else:
                # Prepare the prompt for OpenAI
                columns_str = ", ".join(df.columns)
                df_head_str = df.head().to_string(index=False)
                prompt = f"""
You are a Python data visualization expert. The DataFrame 'df' has columns: {columns_str}.

Sample data:
{df_head_str}

Write Python code to generate the requested visualization.

Request: {prompt_to_use}

Show the plot using matplotlib, seaborn, or plotly - whichever is most appropriate. Use plt.show() or fig.show(). Only use appropriate libraries and pandas. Return only the code, nothing else.
"""
                try:
                    with st.spinner("Generating code with DeepSeek via OpenRouter..."):
                        # OpenRouter API call
                        url = f"{OPENROUTER_BASE_URL}/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "model": OPENROUTER_MODEL,
                            "messages": [
                                {"role": "system", "content": "You are a Python data visualization expert. Given a pandas DataFrame named 'df', write Python code to generate the requested visualization. Show the plot using matplotlib, seaborn, or plotly - whichever is most appropriate. Use plt.show() or fig.show(). Only use appropriate libraries and pandas. Return only the code, nothing else."},
                                {"role": "user", "content": prompt}
                            ],
                            "max_tokens": MAX_TOKENS,
                            "temperature": TEMPERATURE
                        }
                        
                        response = requests.post(url, headers=headers, json=payload)
                        response.raise_for_status()  # Raise exception for bad status codes
                        
                        response_data = response.json()
                        code = response_data['choices'][0]['message']['content']
                        
                        # Remove the opening and closing triple backticks and optional 'python' specifier
                        code = re.sub(r"^```(?:python)?\s*", "", code.strip(), flags=re.IGNORECASE)
                        code = re.sub(r"\s*```$", "", code, flags=re.IGNORECASE)
                        if not code:
                            st.error("No code was returned by DeepSeek.")
                        else:
                            st.session_state['generated_code'] = code  # Store the generated code in session state
                            st.subheader("Generated Python code:")
                            st.code(code, language="python")
                            # Execute the generated code safely
                            if "plt.show()" not in code and "fig.show()" not in code:
                                vis_error = "Generated code does not contain plt.show() or fig.show()."
                                st.error(vis_error)
                            else:
                                try:
                                    # Create a new figure before executing the code
                                    plt.figure()
                                    
                                    # Remove both plt.show() and fig.show() from the code
                                    code = code.replace("plt.show()", "")
                                    code = code.replace("fig.show()", "")
                                    
                                    # Create the global namespace with required modules
                                    global_vars = {
                                        'plt': plt,
                                        'pd': pd,
                                        'df': df,
                                        'go': go
                                    }
                                    
                                    # Execute the code with both global and local contexts
                                    exec(code, global_vars, global_vars)
                                    
                                    # Store the code in session state
                                    st.session_state['generated_code'] = code
                                except Exception as e:
                                    vis_error = f"Error executing generated code: {e}"
                                    st.error(vis_error)
                                    plt.close('all')  # Clean up in case of error
                except Exception as e:
                    vis_error = f"Unexpected error with OpenRouter API: {e}"
                    st.error(vis_error)

        # Recreate the visualization if code exists in session state
        if 'generated_code' in st.session_state and st.session_state['generated_code']:
            try:
                plt.figure()
                code = st.session_state['generated_code']
                code = code.replace("plt.show()", "")
                code = code.replace("fig.show()", "")
                global_vars = {
                    'plt': plt,
                    'pd': pd,
                    'df': df,
                    'go': go
                }
                exec(code, global_vars, global_vars)
                st.subheader("Current Visualization:")  # Label the last visualization as 'Current Visualization'
                if 'fig' in global_vars and isinstance(global_vars['fig'], go.Figure):
                    st.plotly_chart(global_vars['fig'])
                else:
                    st.pyplot(plt.gcf())
                plt.close('all')
            except Exception as e:
                st.error(f"Error recreating visualization: {e}")
                plt.close('all')

        # Feedback form only after visualization is generated and code is available
        if st.session_state['generated_code'] is not None:
            if 'comment' not in st.session_state:
                st.session_state['comment'] = ''
            with st.form("feedback_form"):
                st.write("### Rate the generated visualization")
                visual_accuracy = st.slider("Visual Accuracy (1=Poor, 5=Excellent)", 1, 5, 3)
                visual_insightfulness = st.slider("Visual Insightfulness (1=Low, 5=High)", 1, 5, 3)
                business_relevance = st.slider("Business Relevance (1=Low, 5=High)", 1, 5, 3)
                comment = st.text_area("Comment (optional)", key='comment')
                submitted = st.form_submit_button("Submit Feedback")
                if submitted:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO feedback (prompt, visual_accuracy, visual_insightfulness, business_relevance, comment, timestamp, code) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (prompt_to_use, visual_accuracy, visual_insightfulness, business_relevance, comment, datetime.now().isoformat(), st.session_state['generated_code'])
                    )
                    conn.commit()
                    conn.close()
                    st.session_state['clear_form'] = True
                    st.session_state['generated_code'] = None
                    st.success("Thank you for your feedback!")
                    st.rerun()
    else:
        st.error("Dataset could not be loaded. Please check the file path or format.")
