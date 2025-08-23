import os
from supabase import create_client, Client
from datetime import datetime, timezone
import uuid


def get_supabase_client() -> Client:
    """Initialize and return Supabase client."""
    url = os.getenv('SUPABASE_URL', 'https://nafxymsdbtdxkjknorvl.supabase.co')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"Debug: SUPABASE_URL = {url}")
    print(f"Debug: SUPABASE_ANON_KEY = {key[:20] if key else 'None'}...")
    
    if not key:
        raise ValueError("SUPABASE_ANON_KEY environment variable is not set")
    
    return create_client(url, key)


def get_formatted_timestamp() -> str:
    """
    Return current timestamp in UTC with the format '2025-08-23 08:29:30+00'.
    
    This matches the exact format specified for the created_at field.
    """
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime('%Y-%m-%d %H:%M:%S+00')


def save_feedback_to_supabase(
    model_name: str,
    prompt: str,
    problem_id: int,
    visual_accuracy: int,
    visual_insightfulness: int,
    business_relevance: int,
    comment: str = None,
    code: str = None
) -> dict:
    """
    Save feedback to Supabase feedback table.
    
    Args:
        model_name: Name of the LLM model
        prompt: The visualization prompt used
        problem_id: ID of the selected business problem
        visual_accuracy: Accuracy rating (1-5)
        visual_insightfulness: Insightfulness rating (1-5)
        business_relevance: Business relevance rating (1-5)
        comment: Optional comment
        code: Generated code
    
    Returns:
        dict: Response from Supabase
    """
    try:
        print(f"Debug: Attempting to save feedback for {model_name}")
        supabase = get_supabase_client()
        
        # Generate a unique session ID for this feedback session
        session_id = str(uuid.uuid4())
        
        # Generate properly formatted timestamp
        created_at = get_formatted_timestamp()
        print(f"Debug: Generated created_at timestamp: {created_at}")
        
        # Prepare feedback data
        feedback_data = {
            "model_name": model_name,
            "prompt": prompt,
            "problem_id": problem_id,
            "visual_accuracy": visual_accuracy,
            "visual_insightfulness": visual_insightfulness,
            "business_relevance": business_relevance,
            "comment": comment,
            "code": code,
            "session_id": session_id,
            "created_at": created_at
        }
        
        print(f"Debug: Feedback data prepared: {feedback_data}")
        
        # Insert into feedback table
        print("Debug: Executing insert query...")
        response = supabase.table("feedback").insert(feedback_data).execute()
        
        print(f"Debug: Insert response: {response}")
        print(f"Debug: Response data: {response.data}")
        
        return {
            "success": True,
            "data": response.data,
            "session_id": session_id,
            "created_at": created_at
        }
        
    except Exception as e:
        print(f"Debug: Exception in save_feedback_to_supabase: {e}")
        print(f"Debug: Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def get_feedback_count() -> int:
    """Get total count of feedback entries from Supabase."""
    try:
        supabase = get_supabase_client()
        response = supabase.table("feedback").select("id", count="exact").execute()
        return response.count if response.count is not None else 0
    except Exception as e:
        print(f"Error getting feedback count: {e}")
        return 0


def get_feedback_analysis():
    """Get feedback analysis data from Supabase."""
    try:
        supabase = get_supabase_client()
        
        # Get all feedback data
        response = supabase.table("feedback").select("*").execute()
        
        if response.data:
            return response.data
        else:
            return []
            
    except Exception as e:
        print(f"Error getting feedback analysis: {e}")
        return []


def test_timestamp_format():
    """Test function to verify the timestamp format is correct."""
    timestamp = get_formatted_timestamp()
    print(f"Generated timestamp: {timestamp}")
    expected_length = 22
    has_timezone = '+00' in timestamp
    print(f"Format matches '2025-08-23 08:29:30+00': "
          f"{len(timestamp) == expected_length and has_timezone}")
    return timestamp


if __name__ == "__main__":
    # Test the timestamp formatting when running the file directly
    test_timestamp_format()