from . import config
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from retrying import retry

# Set up logging
logging.basicConfig(filename=config.LOG_FILE, level=logging.ERROR)

# Define required environment variables
REQUIRED_VARS = [
    "BILLO_BASE_URL", "BILLO_API_KEY",
    "BILLO_USER_ID", "VERIFY_SSL_CERT"
]

# Load and validate environment variables
env_vars = config.load_and_validate_env_vars(REQUIRED_VARS)

# BILLO API details
BASE_URL = env_vars["BILLO_BASE_URL"]
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': env_vars["BILLO_API_KEY"],
}
EMBEDDING_MODEL = "azure-embeddings"
GPT_4_CONTEXT_WINDOW = 8000
VERIFY_SSL_CERT = env_vars["VERIFY_SSL_CERT"]

def get_content(response_full):
    return response_full['choices'][0]['text']

def get_token_usage(response_full):
    return response_full["usage"]["total_tokens"]

def get_endpoints():
    """
    Retrieves available endpoints from the BILLO API.

    Returns:
        list: List of available endpoints.

    Example:
        endpoints = get_endpoints()
        print(endpoints)
    """
    try:
        response = requests.post(BASE_URL + "/api/2.0/endpoints", headers=HEADERS, verify=VERIFY_SSL_CERT)
        response.raise_for_status()
        return [endpoint['name'] for endpoint in response.json()['endpoints'] if endpoint['name'] in ["gpt-4", "gpt-3.5", "claude-instant", "claude-2-1", "claude-2-0"]] # these are the only ones that appear to work
    except Exception as e:
        logging.error(f"Request failed for billo.get_endpoints: {e}")
        raise

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def query_rag(user_query, num_chunks, index_name):
    """
    Queries the RAG system with a user query.

    Args:
        user_query (str): The query to send to the RAG system.
        num_chunks (int): Number of chunks to retrieve.

    Returns:
        dict: The response from the RAG system.

    Example:
        response = query_rag("What is the capital of France?", 5)
        print(response)
    """
    json_data = {
        "index_name": index_name,
        "embedding_model": "azure-embeddings",
        "query": user_query,
        "num_neighbors": num_chunks
    }
    try:
        response = requests.post(BASE_URL + "/rag/query", headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Request failed for billo.query_rag: {e}")
        raise

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def query_llm(prompt, model_type="gpt-4", max_tokens=64, temperature=0.0):
    """
    Queries the LLM with a given prompt.

    Args:
        prompt (str): The prompt to send to the LLM.
        model_type (str, optional): The model type to use. Defaults to "gpt-4".
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 64.
        temperature (float, optional): The sampling temperature. Defaults to 0.0.

    Returns:
        dict: The response from the LLM.

    Example:
        response = query_llm("Tell me a joke.")
        print(response)
    """
    json_data = {
        "max_tokens": max_tokens,
        "n": 1,
        "prompt": prompt,
        "stop": ["END"],
        "temperature": temperature
    }
    try:
        response = requests.post(BASE_URL + f'/endpoints/{model_type}/invocations', headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Request failed for billo.query_llm: {e}")
        raise

def separate_for_indexing(processed_docs):
    """
    Prepares documents and metadata for indexing.

    Args:
        processed_docs (pd.DataFrame): DataFrame containing document data.

    Returns:
        tuple: Tuple containing lists of documents ids, and metadata.

    Example:
        documents, ids, metadata = separate_for_indexing(processed_docs)
        print(documents, ids, metadata)
    """
    documents = processed_docs[['Content']].apply(lambda x: ' '.join(x.dropna().values.tolist()), axis=1).tolist() 
    ids = processed_docs[['Chunk_ID']].apply(lambda x: ' '.join(x.dropna().values.tolist()), axis=1).tolist()
    metadata = processed_docs["Metadata"].tolist()
    return documents, ids, metadata

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def _index_rag(document, metadata, id, index_name):
   json_data = {
       "index_name": index_name,
       "embedding_model": EMBEDDING_MODEL,
       "texts": [document],
       "metadatas": [metadata]
   }
   try:
        response = requests.post(BASE_URL + "/rag/index", headers=HEADERS, json=json_data, verify=VERIFY_SSL_CERT)
        response.raise_for_status()
        return f"Indexed a chunk on page {metadata['Page']} of {metadata['Source']}"
   except Exception as e:
        logging.error(f"Request failed for document with id {id}: {e}")
        raise
   
def index_rag_multi_threaded(documents, metadata, ids, index_name, max_workers=8):
   print(f"Index name set to: {index_name}")
   index_name = [index_name] * len(documents)
   with ThreadPoolExecutor(max_workers=max_workers) as executor:
       for result in executor.map(_index_rag, documents, metadata, ids, index_name):
           if result:
               print(result)

def parse_log_file(log_file): 
    failed_chunks = [] 
    with open(log_file, 'r') as file: 
        for line in file: 
            if "Request failed for document with id" in line: 
                parts = line.split('id ')[1].split(': ') 
                id = parts[0] 
                failed_chunks.append(id) 
    return failed_chunks

def clear_log_file(log_file):
    open(log_file, 'w').close()

def resubmit_failed_chunks(log_file, documents, metadata, ids, index_name, max_workers=8): 
    failed_chunks = parse_log_file(log_file)
    # Map document IDs to documents and metadata
    id_to_document = {id: doc for id, doc in zip(ids, documents)} 
    id_to_metadata = {id: meta for id, meta in zip(ids, metadata)} 
    # Prepare lists for resubmission
    resubmit_documents = [] 
    resubmit_metadata = [] 
    resubmit_ids = [] 
    for id in failed_chunks: 
        if id in id_to_document and id in id_to_metadata: 
            resubmit_documents.append(id_to_document[id]) 
            resubmit_metadata.append(id_to_metadata[id]) 
            resubmit_ids.append(id)
    if len(resubmit_documents):
        clear_log_file(log_file)
        # Resubmit failed chunks
        print("Resubmitting failed chunks")
        index_rag_multi_threaded(resubmit_documents, resubmit_metadata, resubmit_ids, index_name, max_workers)
    else:
        print("Log file clean, no docs to resubmit!")
