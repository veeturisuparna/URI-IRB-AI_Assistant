from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

def delete_vector_store(vector_store_id: str):
    """
    Delete a specific vector store by its ID
    
    Args:
        vector_store_id (str): The ID of the vector store to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        client = OpenAI()
        
        # Delete the vector store
        client.vector_stores.delete(vector_store_id)
        print(f"Successfully deleted vector store with ID: {vector_store_id}")
        return True
        
    except Exception as e:
        print(f"Error deleting vector store: {e}")
        return False

if __name__ == "__main__":
    # Get vector store ID from user input
    store_id = input("Please enter the vector store ID to delete (e.g. vs_abc123): ")
    
    # Validate input has expected prefix
    if not store_id.startswith("vs_"):
        print("Error: Vector store ID must start with 'vs_'")
    else:
        delete_vector_store(store_id)
