from openai import OpenAI
import signal
import sys

""" OpenAI currently has issues where the list for the vector_stores doesn't included the latest uploaded files
    This is an incomplete program until their API is updated to include the latest files. 
"""

# Initialize the client
client = OpenAI()

def find_vector_store(search_term):
    """
    Find a specific vector store by searching through names and IDs.
    Returns a list of matching vector stores.
    """
    vector_stores = client.vector_stores.list()
    matches = []
    
    search_term = search_term.lower()
    for vs in vector_stores:
        # Search in both ID and name
        if (search_term in vs.id.lower() or 
            (vs.name and search_term in vs.name.lower())):
            matches.append({
                'id': vs.id,
                'name': vs.name,
                'file_count': vs.file_counts.total,
                'created_at': vs.created_at
            })
    
    if matches:
        print(f"\nFound {len(matches)} matching vector store(s):")
        for i, vs in enumerate(matches, 1):
            print(f"{i}. ID: {vs['id']}")
            print(f"   Name: {vs['name']}")
            print(f"   Files: {vs['file_count']}")
            print(f"   Created: {vs['created_at']}")
    else:
        print(f"\nNo vector stores found matching '{search_term}'")
        
    return matches


def list_vector_stores():
    vector_stores = client.vector_stores.list()
    print(f"The total number of vector stores is {len(vector_stores.data)}")
    print("Vector Stores:")
    for i, vs in enumerate(vector_stores, start=1):
        # Assuming each vector store has an 'id' and optional 'name'
        print(f"{i}. ID: {vs.id} - Name: {vs.name} - Size: {vs.file_counts.total}")
    return vector_stores

def delete_vector_store(vector_store_id):
    deleted_vs = client.vector_stores.delete(vector_store_id=vector_store_id)
    print(f"Deleted vector store: {deleted_vs}")

def list_vector_store_files(vector_store_id):
    files = client.vector_stores.files.list(vector_store_id=vector_store_id)
    print(f"Files in vector store '{vector_store_id}':")
    for i, file in enumerate(files, start=1):
        # Assuming each file has an 'id' and optional 'filename'
        print(f"{i}. ID: {file.id}")
    return files

def delete_vector_store_file(vector_store_id, file_id):
    deleted_file = client.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
    print(f"Deleted file: {deleted_file}")

def signal_handler(sig, frame):
    print('\nGracefully shutting down...')
    sys.exit(0)

def main():
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            print("\n=== Vector Store Manager ===")
            print("1. List vector stores")
            print("2. Search vector stores")
            print("3. Delete a vector store")
            print("4. List files in a vector store") 
            print("5. Delete a file from a vector store")
            print("6. Exit")
            
            try:
                choice = input("Enter your choice: ").strip()
            except EOFError:
                # Handle Ctrl+D
                print('\nGracefully shutting down...')
                break
                
            if choice == "1":
                list_vector_stores()
            elif choice == "2":
                search_term = input("Enter search term: ").strip().lower()
                find_vector_store(search_term)
            elif choice == "3":
                vs_id = input("Enter the vector store ID to delete: ").strip()
                delete_vector_store(vs_id)
            elif choice == "4":
                vs_id = input("Enter the vector store ID to view files: ").strip()
                list_vector_store_files(vs_id)
            elif choice == "5":
                vs_id = input("Enter the vector store ID: ").strip()
                file_id = input("Enter the file ID to delete: ").strip()
                delete_vector_store_file(vs_id, file_id)
            elif choice == "6":
                print("Exiting the manager.")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Shutting down...")
    finally:
        print("Thank you for using Vector Store Manager!")

if __name__ == "__main__":
    main()
