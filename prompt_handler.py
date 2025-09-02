import os
import re
import requests

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import (
    AVAILABLE_MODELS,
    DEFAULT_DATASET_PATH,
    MAX_TOKENS,
    OPENROUTER_API_KEY,
    TEMPERATURE
)
from prompt_scenarios import business_problems
from supabase_feedback import get_feedback_count, save_feedback_to_supabase

# Configure matplotlib for Streamlit compatibility
matplotlib.use('Agg')  # Use non-interactive backend for Streamlit

def get_model_background_color(model_name):
    """Return a subtle background color for each model.
    
    Args:
        model_name (str): Name of the model to get color for
        
    Returns:
        str: CSS rgba color string for the model
    """
    model_colors = {
        'DeepSeek': 'rgba(59, 130, 246, 0.1)',  # Subtle blue
        'OpenAI': 'rgba(16, 185, 129, 0.1)',    # Subtle green
        'Claude': 'rgba(139, 92, 246, 0.1)',    # Subtle purple
        'Gemini': 'rgba(249, 115, 22, 0.1)',    # Subtle orange
        'Llama': 'rgba(239, 68, 68, 0.1)',      # Subtle red
        'Mistral': 'rgba(236, 72, 153, 0.1)',   # Subtle pink
        'Qwen': 'rgba(34, 197, 94, 0.1)',       # Subtle emerald
        'Default': 'rgba(107, 114, 128, 0.1)'   # Subtle gray
    }
    
    # Find the model color by checking if model_name contains any key
    for key, color in model_colors.items():
        if key.lower() in model_name.lower():
            return color
    return model_colors['Default']

def get_model_border_color(model_name):
    """Return a subtle border color for each model.
    
    Args:
        model_name (str): Name of the model to get border color for
        
    Returns:
        str: CSS rgba color string for the model border
    """
    model_colors = {
        'DeepSeek': 'rgba(59, 130, 246, 0.3)',  # Blue border
        'OpenAI': 'rgba(16, 185, 129, 0.3)',    # Green border
        'Claude': 'rgba(139, 92, 246, 0.3)',    # Purple border
        'Gemini': 'rgba(249, 115, 22, 0.3)',    # Orange border
        'Llama': 'rgba(239, 68, 68, 0.3)',      # Red border
        'Mistral': 'rgba(236, 72, 153, 0.3)',   # Pink border
        'Qwen': 'rgba(34, 197, 94, 0.3)',       # Emerald border
        'Default': 'rgba(107, 114, 128, 0.3)'   # Gray border
    }
    
    # Find the model color by checking if model_name contains any key
    for key, color in model_colors.items():
        if key.lower() in model_name.lower():
            return color
    return model_colors['Default']


# Define positive and negative outcome lists for evaluation
POSITIVE_OUTCOMES = [
    "Correct and accurate",
    "Reveals new patterns or trends",
    "Useful for decision-making",
    "Clear and easy to understand",
    "Appropriate chart type",
    "Efficient and reliable code"
]

NEGATIVE_OUTCOMES = [
    "Hallucination (invented data, labels, or trends)",
    "Oversimplification or surface-level insight",
    "Misleading visual design (e.g., distorted scales)",
    "Incorrect data aggregation or logic",
    "Missing key variables or context",
    "Missing key visual elements (e.g., labels, titles, legends)",
    "Poor or inappropriate chart choice",
    "Prompt sensitivity (output changes drastically on minor edits)",
    "Code not executable or contains errors"
]

def handle_prompt_tab():
    """Handle the main prompt tab functionality.
    
    This function manages the entire prompt interface including:
    - Dataset loading and display
    - Business problem selection
    - LLM model execution
    - Results display in tabs
    - Feedback collection
    """
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

    @st.cache_data(show_spinner=True)
    def load_data():
        """Load the default dataset or return an error if not found."""
        if not os.path.exists(DEFAULT_DATASET_PATH):
            st.error(f"Dataset file not found at: {DEFAULT_DATASET_PATH}")
            return None
        try:
            df = pd.read_csv(DEFAULT_DATASET_PATH, encoding='latin1')
            df.to_csv('Superstore_Dataset.csv', encoding='utf-8', index=False)
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
        st.subheader("Dataset Information:")
        if uploaded_file:
            st.info(f"📊 Using uploaded dataset: **{uploaded_file.name}**")
        else:
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
        st.info(
            f"**Visualization Type:** {details['Visualization Type']}\n"
            f"**Complexity:** {details['Complexity']}"
        )

        # Toggle for custom prompt input
        use_custom_prompt = st.checkbox("Write your own prompt instead", value=False)
        # Store the custom prompt state in session state
        st.session_state['use_custom_prompt'] = use_custom_prompt
        
        if use_custom_prompt:
            if 'user_request' not in st.session_state:
                st.session_state['user_request'] = (
                    selected_problem + " using " + details['Visualization Type']
                )
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
        st.info(
            "Click the button below to generate visualizations using all "
            "available AI models simultaneously."
        )
        
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
                                    {
                                        "role": "system", 
                                        "content": (
                                            "You are a Python code generator. "
                                            "Return only executable Python code, "
                                            "no explanations."
                                        )
                                    },
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
                                    code = re.sub(
                                        r"^```(?:python)?\s*", 
                                        "", 
                                        code.strip(), 
                                        flags=re.IGNORECASE
                                    )
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
                st.success(
                    "✅ All models have completed! Results are displayed below "
                    "and will persist until cleared."
                )

        # Display results from session state (this will persist across reruns)
        if st.session_state['all_results']:
            st.markdown("---")
            st.subheader("📊 Generated Visualizations")
            st.info(f"**Current Prompt:** {st.session_state['current_prompt']}")
            
            # Create tabs for each model with logos
            model_names = list(st.session_state['all_results'].keys())
            tab_labels = []
            for model_name in model_names:
                # Map model names to their logo files
                logo_map = {
                    'DeepSeek': 'deepseek.png',
                    'OpenAI': 'openai.png', 
                    'Claude': 'claude.png'
                }
                
                # Find matching logo
                logo_file = None
                for key, logo in logo_map.items():
                    if key.lower() in model_name.lower():
                        logo_file = logo
                        break
                
                if logo_file:
                    # Create tab label with logo
                    tab_labels.append(f"![{model_name}](public/{logo_file}) {model_name}")
                else:
                    # Fallback to emoji if no logo found
                    tab_labels.append(f"🤖 {model_name}")
            
            tabs = st.tabs(tab_labels)
            
            for i, (model_name, result) in enumerate(st.session_state['all_results'].items()):
                with tabs[i]:
                    # Get colors for this model
                    bg_color = get_model_background_color(model_name)
                    border_color = get_model_border_color(model_name)
                    
                    # Create a styled container with background color
                    st.markdown(f"""
                    <div style="
                        background-color: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0;
                    ">
                    """, unsafe_allow_html=True)
                    
                    # Model header with logo - FIXED CONSISTENT SIZING
                    # Map model names to their logo files
                    logo_map = {
                        'DeepSeek': 'deepseek.png',
                        'OpenAI': 'openai.png', 
                        'Claude': 'claude.png'
                    }
                    
                    # Find matching logo
                    logo_file = None
                    for key, logo in logo_map.items():
                        if key.lower() in model_name.lower():
                            logo_file = logo
                            break
                    
                    if logo_file:
                        # Create header with logo - consistent sizing for different logos
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            # Define consistent sizing for different logos
                            logo_sizes = {
                                'deepseek.png': 40,
                                'openai.png': 100,  # Slightly smaller for OpenAI
                                'claude.png': 100   # Medium size for Claude
                            }
                            logo_width = logo_sizes.get(logo_file, 100)  # Default to 60 if not specified
                            st.image(f"public/{logo_file}", width=logo_width)
                        with col2:
                            st.markdown(f"## {model_name}")
                    else:
                        # Fallback to emoji if no logo found
                        st.markdown(f"## 🤖 {model_name}")
                    
                    st.info(f"**Model ID:** {result['model_id']}")
                    
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
                            
                        except Exception as e:
                            st.error(f"Error executing code from {model_name}: {e}")
                            plt.close('all')
                    else:
                        # Show error message if the model failed
                        st.error(f"❌ {result['code']}")
                        st.info("This model encountered an error. Please try again or check your API configuration.")
                    
                    # Always show feedback section regardless of success/error
                    st.markdown("---")
                    st.subheader("⭐ Rate This Visualization:")
                    
                    # Show feedback count for this model
                    feedback_count_key = f"feedback_count_{model_name}"
                    if feedback_count_key not in st.session_state:
                        st.session_state[feedback_count_key] = 0
                    
                    if st.session_state[feedback_count_key] > 0:
                        st.success(f"📊 You have submitted {st.session_state[feedback_count_key]} feedback entries for {model_name}")
                    
                    # Inline feedback form (no modal needed)
                    with st.expander(f"📝 Submit Feedback for {model_name}", expanded=False):
                        # Create the feedback form
                        with st.form(f"feedback_form_{model_name}"):
                            st.markdown(f"**Model:** {model_name}")
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
                            
                            # New field: Iteration Count
                            iteration_count = st.number_input(
                                "Iteration Count - How many iterations did it take you to get the final outcome?",
                                min_value=1,
                                max_value=20,
                                value=1,
                                step=1,
                                help="Enter the number of attempts or refinements needed"
                            )
                            
                            # New field: Positive Outcomes (Multi-select)
                            positive_outcomes_selected = st.multiselect(
                                "Positive Outcomes - Select all that apply:",
                                options=POSITIVE_OUTCOMES,
                                help="Choose all positive aspects of this visualization"
                            )
                            
                            # New field: Negative Outcomes (Multi-select)
                            negative_outcomes_selected = st.multiselect(
                                "Negative Outcomes - Select all that apply:",
                                options=NEGATIVE_OUTCOMES,
                                help="Choose all negative aspects or issues with this visualization"
                            )
                            
                            comment = st.text_area("Comment (optional - Suggestions or observations about what worked well or what could be improved.)", height=100)
                            
                            submitted = st.form_submit_button("✅ Submit Feedback", use_container_width=True)
                            
                            if submitted:
                                try:
                                    # Get the problem_id based on whether user wrote their own prompt
                                    selected_problem = st.session_state.get('selected_problem', '')
                                    use_custom_prompt = st.session_state.get('use_custom_prompt', False)
                                    
                                    if use_custom_prompt:
                                        # If user wrote their own prompt, set problem_id to 0
                                        problem_id = 0
                                    else:
                                        # Use the selected business problem ID
                                        problem_id = business_problems[selected_problem]['ProblemID'] if selected_problem in business_problems else 0
                                    
                                    # Convert multi-select lists to comma-separated strings
                                    positive_outcomes_str = ", ".join(positive_outcomes_selected) if positive_outcomes_selected else ""
                                    negative_outcomes_str = ", ".join(negative_outcomes_selected) if negative_outcomes_selected else ""
                                    
                                    # Save feedback to Supabase
                                    feedback_result = save_feedback_to_supabase(
                                        model_name=model_name,
                                        prompt=result.get('prompt', st.session_state['current_prompt']),
                                        problem_id=problem_id,
                                        visual_accuracy=visual_accuracy,
                                        visual_insightfulness=visual_insightfulness,
                                        business_relevance=business_relevance,
                                        iteration_count=iteration_count,
                                        positive_outcomes=positive_outcomes_str,
                                        negative_outcomes=negative_outcomes_str,
                                        comment=comment,
                                        code=result['code']
                                    )
                                    
                                    if feedback_result['success']:
                                        # Update feedback count for this model
                                        feedback_count_key = f"feedback_count_{model_name}"
                                        st.session_state[feedback_count_key] = st.session_state.get(feedback_count_key, 0) + 1
                                        
                                        # Show success and refresh
                                        st.success(f"✅ Feedback for {model_name} submitted successfully!")
                                        st.info("The page will refresh to show your updated feedback count.")
                                        st.rerun()
                                        
                                    else:
                                        st.error(f"Error saving feedback: {feedback_result.get('error', 'Unknown error')}")
                                    
                                except Exception as e:
                                    st.error(f"Error saving feedback: {e}")
                                    print(f"Supabase error: {e}")
                    
                    # Close the styled div
                    st.markdown("</div>", unsafe_allow_html=True)



    else:
        st.error("Dataset could not be loaded. Please check the file path or format.")