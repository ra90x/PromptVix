import streamlit as st
import pandas as pd
from supabase_feedback import get_feedback_analysis


def load_feedback():
    """Load feedback data from Supabase and return as DataFrame."""
    try:
        feedback_data = get_feedback_analysis()
        if feedback_data:
            df = pd.DataFrame(feedback_data)
            # Sort by created_at in descending order
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df = df.sort_values('created_at', ascending=False)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading from Supabase: {e}")
        return pd.DataFrame()


def show_feedback_analysis():
    """Display feedback analysis interface."""
    st.title("PromptVix Feedback Viewer")
    st.subheader("📊 View Submitted Prompt Feedback from Supabase")
    
    refresh = st.button("Refresh Feedback Records")
    feedback_df = load_feedback()
    
    if feedback_df.empty:
        st.info("No feedback records found in Supabase.")
    else:
        st.success(f"{len(feedback_df)} feedback record(s) found.")
        st.dataframe(feedback_df, use_container_width=True)
        
        # Add export button
        csv = feedback_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='feedback_export.csv',
            mime='text/csv',
        )
