import os
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=True)
def load_default_dataset():
    """Load the default dataset from the specified path.
    
    Returns:
        pd.DataFrame or None: Loaded dataset or None if error
    """
    default_path = r"C:\dataset.csv"
    if not os.path.exists(default_path):
        st.error(f"Default dataset not found at {default_path}")
        return None
    try:
        return pd.read_csv(default_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


def is_code_safe(code: str) -> bool:
    """Check if generated code contains unsafe patterns.
    
    Args:
        code (str): Code string to check for safety
        
    Returns:
        bool: True if code is safe, False otherwise
    """
    blacklist = [
        "os.", "sys.", "subprocess", "shutil", "open(", "eval(", "exec("
    ]
    return not any(term in code for term in blacklist)
