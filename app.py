"""Main application entry point for PromptVix."""

import streamlit as st
from dotenv import load_dotenv

from analysis import show_feedback_analysis
from prompt_handler import handle_prompt_tab

# Load environment variables
load_dotenv()


def main():
    """Main application entry point."""
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", 
        ["📈 PromptVix", "📊 Feedback Analysis"]
    )

    # Add watermark at the bottom of the sidebar
    st.sidebar.markdown("""
        <div style='position: fixed; bottom: 30px; left: 16px; 
             width: 220px; font-size: 12px; color: #888; opacity: 0.8;'>
            University of Liverpool | Student: Ramz A.
        </div>
    """, unsafe_allow_html=True)

    if page == "📈 PromptVix":
        handle_prompt_tab()
    elif page == "📊 Feedback Analysis":
        show_feedback_analysis()


if __name__ == "__main__":
    main()
