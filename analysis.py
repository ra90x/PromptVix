import streamlit as st
import sqlite3
import pandas as pd


def load_feedback():
    try:
        conn = sqlite3.connect("prompt_feedback.db")
        df = pd.read_sql_query("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error reading from database: {e}")
        return pd.DataFrame()

def show_feedback_analysis():
    st.title("PromptVix Feedback Viewer")
    st.subheader("📊 View Submitted Prompt Feedback")
    refresh = st.button("Refresh Feedback Records")
    feedback_df = load_feedback()
    if feedback_df.empty:
        st.info("No feedback records found.")
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
