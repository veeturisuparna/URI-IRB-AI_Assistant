from openai import OpenAI
from tqdm import tqdm
import concurrent
import os
from dotenv import load_dotenv

# Use tkinter for file selection dialog
import tkinter as tk
from tkinter import filedialog

# Create and hide root window
root = tk.Tk()
root.withdraw()

#This loads the .env file into the environment variables
#but ensures any changes to the .env file are reflected immediately
load_dotenv(override=True)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Open file selection dialog
print("\nPlease select files to process...")
selected_files = filedialog.askopenfilenames(
    title='Select files to process',
    filetypes=[
        ('Supported Files', '*.pdf;*.txt;*.docx;*.doc;*.rtf'),
        ('PDF Files', '*.pdf'),
        ('Text Files', '*.txt'),
        ('Word Documents', '*.docx;*.doc'),
        ('RTF Files', '*.rtf'),
        ('All Files', '*.*')
    ]
)

# Supported file types for vector store
SUPPORTED_FILE_TYPES = {'.pdf', '.txt', '.docx', '.doc', '.rtf'}

def validate_file_type(filename: str) -> bool:
    """Check if file type is supported for vector store"""
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in SUPPORTED_FILE_TYPES

def get_valid_files(filepaths: list) -> list:
    """Get list of supported files from selected files"""
    valid_files = []
    invalid_files = []
    print(filepaths)
    for f in filepaths:
        print(f"Validating file: {f}")
        if validate_file_type(f):
            valid_files.append(f)
        else:
            invalid_files.append(f)
            
    if invalid_files:
        print("\nWarning: The following files are not supported and will be skipped:")
        for f in invalid_files:
            print(f"- {os.path.basename(f)}")
            
    return valid_files

# Get list of valid files from selection
files = get_valid_files(selected_files)

if files:
    print(f"\nSelected {len(files)} valid files:")
    for f in files:
        print(f"- {os.path.basename(f)}")
    
    proceed = input("\nProceed with these files? (y/n): ").lower()
    if proceed != 'y':
        print("Operation cancelled.")
        files = []
else:
    print("\nNo valid files selected. Please try again.")
    files = []
    
    
    
"""
Creating Vector Store with our files
------------------------------------
We will create a Vector Store on OpenAI API and upload our files to the Vector Store. 
OpenAI will read those PDFs, separate the content into multiple chunks of text, 
run embeddings on those and store those embeddings and the text in the Vector Store. 
It will enable us to query this Vector Store to return relevant content based on a query.
"""

def upload_single_file(file_path: str, vector_store_id: str):
    file_name = os.path.basename(file_path)
    try:
        file_response = client.files.create(file=open(file_path, 'rb'), purpose="assistants")
        attach_response = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_response.id
        )
        return {"file": file_name, "status": "success", "upload_status": attach_response.status}
    except Exception as e:
        print(f"Error with {file_name}: {str(e)}")
        return {"file": file_name, "status": "failed", "error": str(e)}

def upload_files_to_vector_store(vector_store_id: str, files: list):
    stats = {"total_files": len(files), "successful_uploads": 0, "failed_uploads": 0, "errors": []}
    
    print(f"{len(files)} files to process. Uploading in parallel...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(upload_single_file, file_path, vector_store_id): file_path for file_path in files}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(files)):
            result = future.result()
            if result["status"] == "success":
                stats["successful_uploads"] += 1
                print(f"Uploaded {result['file']} with status {result['upload_status']}")
            else:
                stats["failed_uploads"] += 1
                stats["errors"].append(result)
                print(f"Failed to upload {result['file']}: {result['error']}")

    return stats

def create_vector_store(store_name: str) -> dict:
    try:
        vector_store = client.vector_stores.create(name=store_name)
        details = {
            "id": vector_store.id,
            "name": vector_store.name,
            "created_at": vector_store.created_at,
            "file_count": vector_store.file_counts.completed
        }
        print("Vector store created:", details)
        return details
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return {}

def save_vector_store_id(store_name: str, vector_id: str):
    """Save vector store ID to file with store name as variable"""
    filename = "utils/vector_store_ids_list.txt"
    store_name = store_name.replace(" ", "_").lower()
    entry = f"{store_name}_vector_id = '{vector_id}'\n"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Append to file if it exists, create if it doesn't
    with open(filename, 'a') as f:
        f.write(entry)
    
def setup_vector_store(valid_files):
    print("\n" + "="*80)
    print("WARNING: Vector file storage costs $0.10 per GB per hour.")
    print("Files uploaded will incur storage costs based on their size.")
    print("="*80 + "\n")

    while True:
        store_name = input("\nEnter a name for your vector store (or 'cancel' to abort): ").strip()
        
        if store_name.lower() == 'cancel':
            print("Vector store creation cancelled.")
            return None
            
        if store_name:
            proceed = input(f"\nCreate vector store '{store_name}' with {len(valid_files)} files? (y/n): ").lower()
            
            if proceed == 'y':
                # Create the vector store
                vector_store_details = create_vector_store(store_name)
                
                if vector_store_details:
                    # Upload the files
                    upload_stats = upload_files_to_vector_store(vector_store_details["id"], valid_files)
                    
                    print("\nVector Store Creation Summary:")
                    print(f"Store Name: {store_name}")
                    print(f"Store ID: {vector_store_details['id']}")
                    print(f"Files Uploaded Successfully: {upload_stats['successful_uploads']}")
                    print(f"Failed Uploads: {upload_stats['failed_uploads']}")
                    
                    if upload_stats['errors']:
                        print("\nErrors encountered:")
                        for error in upload_stats['errors']:
                            print(f"- {error['file']}: {error['error']}")
                    
                    # Save vector store ID to file
                    save_vector_store_id(store_name, vector_store_details["id"])
                    print(f"\nVector store ID saved to utils/vector_store_ids_list.txt")
                            
                    return vector_store_details
                    
                return None
                
            print("Vector store creation cancelled.")
            return None
            
        print("Please enter a valid store name.")

setup_vector_store(files)