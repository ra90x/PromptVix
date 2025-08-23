import os
import json
import re
import requests
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from datetime import datetime
# from feedback_db import save_feedback
from utils import load_default_dataset, is_code_safe

from prompt_scenarios import business_problems
from config import OPENROUTER_API_KEY, AVAILABLE_MODELS, OPENROUTER_BASE_URL, DEFAULT_DATASET_PATH, MAX_TOKENS, TEMPERATURE
from supabase_feedback import save_feedback_to_supabase, get_feedback_count
import plotly.graph_objects as go

# Configure matplotlib for Streamlit compatibility
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Streamlit

def handle_prompt_tab():
    # Set up the Streamlit app title and subtitle
    st.title("📈 PromptVix")
    st.subheader("IT Artefact | Developed by Ramz A.", divider=True)
    
    # Check Supabase database status
    try:
        feedback_count = get_feedback_count()
        st.sidebar.success(f"📊 Supabase: {feedback_count} feedback entries")
        
        # Show session feedback summary
        session_feedback_count = 0
        for model_name in AVAILABLE_MODELS.keys():
            feedback_count_key = f"feedback_count_{model_name}"
            session_feedback_count += st.session_state.get(feedback_count_key, 0)
        
        if session_feedback_count > 0:
            st.sidebar.info(f"📝 Session: {session_feedback_count} feedback entries submitted")
            
    except Exception as e:
        st.sidebar.error(f"❌ Supabase Error: {e}")
        print(f"Supabase connection error: {e}")

    # Initialize session state for storing results persistently
    if 'all_results' not in st.session_state:
        st.session_state['all_results'] = {}
    if 'current_prompt' not in st.session_state:
        st.session_state['current_prompt'] = ""
    if 'selected_problem' not in st.session_state:
        st.session_state['selected_problem'] = ""
    if 'feedback_modal_open' not in st.session_state:
        st.session_state['feedback_modal_open'] = False
    if 'selected_model_for_feedback' not in st.session_state:
        st.session_state['selected_model_for_feedback'] = ""

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

    # Use only the default dataset (no upload/reload functionality)
    df = load_data()

    if df is not None:
        st.subheader("Dataset Information:")
        st.info(f"📊 Using provided dataset: **{DEFAULT_DATASET_PATH}**")
        st.subheader("Data Preview:")
        st.dataframe(df.head(10))

        # --- Business Problem Dropdown and Custom Prompt Toggle ---
        st.subheader("Select a Business Problem or Write Your Own Prompt:")
        
        selected_problem = st.selectbox(
            "Choose a Business Problem:",
            list(business_problems.keys()),
            key="business_problem_select"
        )
        # Store selected problem in session state
        st.session_state['selected_problem'] = selected_problem
        
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

        # Generate Visualizations from All LLM Models
        st.subheader("◆ Generate Visualizations from All LLM Models")
        st.info("Click the button below to generate visualizations using all available AI models simultaneously.")
        
        # Clear results button
        col1, col2 = st.columns([1, 1])
        with col1:
            generate_clicked = st.button("🚀 Generate All Visualizations")
        with col2:
            if st.button("🗑️ Clear Results"):
                st.session_state['all_results'] = {}
                st.session_state['current_prompt'] = ""
                st.rerun()
        
        if generate_clicked and prompt_to_use:
            if not prompt_to_use.strip():
                st.error("Please enter a valid visualization request.")
            else:
                # Store the current prompt
                st.session_state['current_prompt'] = prompt_to_use
                
                # Prepare the prompt for LLM
                columns_str = ", ".join(df.columns)
                df_head_str = df.head().to_string(index=False)
                prompt = f"""Create a Python visualization for this request: {prompt_to_use}

DataFrame 'df' has columns: {columns_str}
Sample data:
{df_head_str}

Requirements:
- Use matplotlib, seaborn, or plotly
- Include plt.show() or fig.show()
- Return only Python code
- Use pandas for data manipulation"""
                
                # Store results for all models
                all_results = {}
                
                # Show which models will be processed
                st.info(f"🔄 **Processing Models:** {', '.join(AVAILABLE_MODELS.keys())}")
                
                # Generate from all models simultaneously
                with st.spinner("Generating visualizations from all AI models..."):
                    for model_name, model_id in AVAILABLE_MODELS.items():
                        try:
                            st.write(f"🔄 Generating with {model_name}...")
                            
                            # OpenRouter API call
                            url = "https://openrouter.ai/api/v1/chat/completions"
                            headers = {
                                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "https://github.com/ra90x/PromptVix",
                                "X-Title": "PromptVix"
                            }
                            payload = {
                                "model": model_id,
                                "messages": [
                                    {"role": "system", "content": "You are a Python code generator. Return only executable Python code, no explanations."},
                                    {"role": "user", "content": prompt}
                                ],
                                "max_tokens": MAX_TOKENS,
                                "temperature": TEMPERATURE
                            }
                            
                            response = requests.post(url, headers=headers, json=payload)
                            
                            if response.status_code == 200:
                                response_data = response.json()
                                if 'choices' in response_data and response_data['choices']:
                                    code = response_data['choices'][0]['message']['content']
                                    # Clean the code
                                    code = re.sub(r"^```(?:python)?\s*", "", code.strip(), flags=re.IGNORECASE)
                                    code = re.sub(r"\s*```$", "", code, flags=re.IGNORECASE)
                                    
                                    if code and code.strip():
                                        all_results[model_name] = {
                                            'code': code,
                                            'model_id': model_id,
                                            'success': True,
                                            'prompt': prompt_to_use
                                        }
                                    else:
                                        all_results[model_name] = {
                                            'code': f"Error: {model_name} returned empty code",
                                            'model_id': model_id,
                                            'success': False,
                                            'prompt': prompt_to_use
                                        }
                                else:
                                    all_results[model_name] = {
                                        'code': f"Error: {model_name} returned no choices",
                                        'model_id': model_id,
                                        'success': False,
                                        'prompt': prompt_to_use
                                    }
                            else:
                                all_results[model_name] = {
                                    'code': f"API Error: {response.status_code}",
                                    'model_id': model_id,
                                    'success': False,
                                    'prompt': prompt_to_use
                                }
                        except Exception as e:
                            all_results[model_name] = {
                                'code': f"Exception: {str(e)}",
                                'model_id': model_id,
                                'success': False,
                                'prompt': prompt_to_use
                            }
                
                # Store results in session state for persistence
                st.session_state['all_results'] = all_results
                st.success("✅ All models have completed! Results are displayed below and will persist until cleared.")

        # Display results from session state (this will persist across reruns)
        if st.session_state['all_results']:
            st.markdown("---")
            st.subheader("📊 Generated Visualizations")
            st.info(f"**Current Prompt:** {st.session_state['current_prompt']}")
            
            # Display each model's results vertically
            for i, (model_name, result) in enumerate(st.session_state['all_results'].items()):
                # Add separator between models (except for the first one)
                if i > 0:
                    st.divider()
                
                # Create a container for each model's results
                with st.container():
                    st.markdown(f"## 🤖 {model_name}")
                    st.info(f"**Model ID:** {result['model_id']}")
                    
                    # Add a subtle background color to distinguish each model section
                    st.markdown("---")
                
                if result['success']:
                    # Display generated code
                    st.subheader("📝 Generated Python Code:")
                    st.code(result['code'], language="python")
                    
                    # Execute and display visualization
                    try:
                        plt.figure()
                        exec_code = result['code'].replace("plt.show()", "").replace("fig.show()", "")
                        
                        global_vars = {
                            'plt': plt,
                            'pd': pd,
                            'df': df,
                            'go': go
                        }
                        
                        exec(exec_code, global_vars, global_vars)
                        
                        st.subheader("🎨 Generated Visualization:")
                        if 'fig' in global_vars and isinstance(global_vars['fig'], go.Figure):
                            st.plotly_chart(global_vars['fig'])
                        else:
                            st.pyplot(plt.gcf())
                        
                        plt.close('all')
                        
                        # Feedback button that opens modal
                        st.subheader("⭐ Rate This Visualization:")
                        
                        # Show feedback count for this model
                        feedback_count_key = f"feedback_count_{model_name}"
                        if feedback_count_key not in st.session_state:
                            st.session_state[feedback_count_key] = 0
                        
                        if st.session_state[feedback_count_key] > 0:
                            st.success(f"📊 You have submitted {st.session_state[feedback_count_key]} feedback entries for {model_name}")
                        
                        # Button to open feedback modal
                        if st.button(f"📝 Submit Feedback for {model_name}", key=f"feedback_btn_{model_name}"):
                            st.session_state['feedback_modal_open'] = True
                            st.session_state['selected_model_for_feedback'] = model_name
                            st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error executing code from {model_name}: {e}")
                        plt.close('all')
                else:
                    st.error(f"❌ {result['code']}")
                    st.info("This model encountered an error. Please try again or check your API configuration.")

        # Feedback Modal using st.dialog (if available) or container
        if st.session_state.get('feedback_modal_open', False):
            selected_model = st.session_state.get('selected_model_for_feedback', '')
            if selected_model and selected_model in st.session_state['all_results']:
                result = st.session_state['all_results'][selected_model]
                
                # Create a modal-like experience
                st.markdown("---")
                st.markdown(f"### 📝 Feedback Form for {selected_model}")
                st.info("Please rate the visualization and provide your feedback below.")
                
                with st.container():
                    # Create the feedback form
                    with st.form(f"feedback_modal_{selected_model}"):
                        st.markdown(f"**Model:** {selected_model}")
                        st.markdown(f"**Prompt:** {result.get('prompt', st.session_state['current_prompt'])}")
                        
                        # Display problem information
                        selected_problem = st.session_state.get('selected_problem', '')
                        if selected_problem and selected_problem in business_problems:
                            problem_details = business_problems[selected_problem]
                            st.markdown(f"**Business Problem:** {selected_problem}")
                            st.markdown(f"**Problem ID:** {problem_details['ProblemID']}")
                            st.markdown(f"**Visualization Type:** {problem_details['Visualization Type']}")
                            st.markdown(f"**Complexity:** {problem_details['Complexity']}")
                        else:
                            st.warning("⚠️ No business problem selected")
                        
                        visual_accuracy = st.slider("Visual Accuracy - Was the visualization clear, easy to understand, and appropriately formatted (labels, chart type, colours)? (1=Poor, 5=Excellent)", 1, 5, 3)
                        visual_insightfulness = st.slider("Visual Insightfulness - Did the visualization help you gain useful insights or notice patterns in the data? (1=Low, 5=High)", 1, 5, 3)
                        business_relevance = st.slider("Business Relevance - How relevant is the visualization to the business problem? (1=Low, 5=High)", 1, 5, 3)
                        comment = st.text_area("Comment (optional - Suggestions or observations about what worked well or what could be improved.)", height=100)
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            submitted = st.form_submit_button("✅ Submit Feedback", use_container_width=True)
                        with col2:
                            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                        
                        if cancel:
                            st.session_state['feedback_modal_open'] = False
                            st.session_state['selected_model_for_feedback'] = ""
                            st.rerun()
                        
                        if submitted:
                            try:
                                # Get the problem_id from the selected business problem
                                selected_problem = st.session_state.get('selected_problem', '')
                                problem_id = business_problems[selected_problem]['ProblemID'] if selected_problem in business_problems else 0
                                
                                # Save feedback to Supabase
                                feedback_result = save_feedback_to_supabase(
                                    model_name=selected_model,
                                    prompt=result.get('prompt', st.session_state['current_prompt']),
                                    problem_id=problem_id,
                                    visual_accuracy=visual_accuracy,
                                    visual_insightfulness=visual_insightfulness,
                                    business_relevance=business_relevance,
                                    comment=comment,
                                    code=result['code']
                                )
                                
                                if feedback_result['success']:
                                    # Update feedback count for this model
                                    feedback_count_key = f"feedback_count_{selected_model}"
                                    st.session_state[feedback_count_key] = st.session_state.get(feedback_count_key, 0) + 1
                                    
                                    # Close modal
                                    st.session_state['feedback_modal_open'] = False
                                    st.session_state['selected_model_for_feedback'] = ""
                                    
                                    # Show success and refresh
                                    st.success(f"✅ Feedback for {selected_model} submitted successfully!")
                                    st.info("The page will refresh to show your updated feedback count.")
                                    st.rerun()
                                    
                                else:
                                    st.error(f"Error saving feedback: {feedback_result.get('error', 'Unknown error')}")
                                
                            except Exception as e:
                                st.error(f"Error saving feedback: {e}")
                                print(f"Supabase error: {e}")

    else:
        st.error("Dataset could not be loaded. Please check the file path or format.")