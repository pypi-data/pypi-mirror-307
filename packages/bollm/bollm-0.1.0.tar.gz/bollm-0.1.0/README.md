# bollm

This is a Python package for helping with creating LLM-based Streamlit apps in Boehringer.

Contact Steven Brooks or Pietro Mascheroni for feedback/support.

## For Users

### Installation

Everything below assumes you have a python venv already created. If you dont, then run

```bash
python -m venv .venv
source .venv/bin/activate
```

To install the package run `pip install bollm`

### Other dependencies

You may need to install other dependencies depending on what kinds of documents you want to parse.

See the `unstructured` documentation here: https://pypi.org/project/unstructured/

In this package, we only install the minimal dependencies necessary.

### Configuration

This project requires certain environment variables to be set. These variables are used for connecting to external APIs and services.

1. Create a `.env` file in the root directory of the project.
2. Add the following content to the `.env` file, replacing placeholder values with your actual credentials:

```env
AZURE_BASE_URL=https://azure.example.com
AZURE_API_KEY=your_azure_api_key
AZURE_DEPLOYMENT_VERSION=v1
AZURE_DEPLOYMENT_NAME=model_name
APOLLO_CLIENT_ID=your_client_id
APOLLO_CLIENT_SECRET=your_client_secret
INDEX_NAME="" # Set this to your index name, see below for more details
```

### RAG Workflow

#### Step 1: Parse Documents

**Note:** This guide, and all following guides assume you've set up your environment properly. See above for instructions.

Before we can build the RAG, we need to parse the documents. This package provides functions to make that easier.

NOTE: PDF images will not be parsed.

We provide a basic chunking strategy, i.e., unstructured chunking. This means that meta-information such as the chapter or section level is missed when chunking the documents.

Two parameters control the chunking structure:

- CHUNK_SIZE: controls the maximum number of characters in one text chunk
- CHUNK_OVERLAP: controls the characters that overlap between following chunks.

The chunk size controls the granularity in which the text is divided: small chunks provide very specific, almost keyword based, matches to the query.
Larger chunks allow to grasp more context and subtle meaning of the text.

To start with, we suggest to go for CHUNK_SIZE = 2000, CHUNK_OVERLAP = 500. From our experiments, these values provide a good default for many situations.

The following is a simple example to setup a parsing strategy. Please follow these steps:

1. Store PDF documents in a folder named `./documents`
2. Create a script like the following:

```python
from bollm import parse_docs

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 500

filenames_df = parse_docs.get_filenames("./documents")
processed_docs = parse_docs.process_documents(filenames_df, CHUNK_SIZE, CHUNK_OVERLAP)
processed_docs["Metadata"] = processed_docs["Metadata"].apply(parse_docs.parse_metadata)
# Save file for the next step
processed_docs.to_parquet(f'my_docs_cs_{CHUNK_SIZE}_co_{CHUNK_OVERLAP}.parquet')
```

#### Step 2: Index the RAG Database

After we've parsed the documents in Step 1, we can index the RAG's vector database with the
document chunks and metadata.

1. Make sure to use the same CHUNK_SIZE and CHUNK_OVERLAP values from the previous step.
2. Make sure you have the `.parquet` file in your working directory.
3. The INDEX_NAME can have underscores, dashes, numbers and lower-case characters only.

**Note:** Its very important that you keep your index name a secret so others won't overwrite it with their documents. 
Consider using an environment variable for this, similar to how we treat an API Key. Another level of assurance that no one 
will overwrite your index with their documents would be to generate a unique index name, e.g., with

```python
import uuid
from bollm.apollo import Apollo
unique_id = str(uuid.uuid4()) # can only include lower case alpha-numeric, underscores, and dashes
apollo = Apollo()
iam = apollo.iam()
INDEX_NAME=f'{iam["id"]}_{unique_id}'
```
But then just remember to record this index name in your `.env` for use later on. If you call it `INDEX_NAME`, then
you can call on it with e.g., `os.getenv("INDEX_NAME")`

4. Index the RAG DB. This can be done following a similar script:

```python
from bollm.apollo import Apollo
from bollm.parse_docs import separate_for_indexing
from bollm import config
import pandas as pd
import os

# use the same values from Step 1
CHUNK_SIZE = 2000 
CHUNK_OVERLAP = 500
PARQUET_FILE = f'my_docs_cs_{CHUNK_SIZE}_co_{CHUNK_OVERLAP}.parquet'
INDEX_NAME = os.getenv("INDEX_NAME") # can only include lower case alpha-numeric, underscores, and dashes
EMBEDDING_MODEL = "openai-text-embedding-3-large" # you can see other embedding models with apollo.get_model_info()
processed_docs = pd.read_parquet(PARQUET_FILE, engine='pyarrow')
texts, ids, metadatas = separate_for_indexing(processed_docs)

# this can take a long time to run, depending on how many documents you have
apollo.index_multi_threaded(
    texts=texts, 
    metadatas=metadatas, 
    index_name=INDEX_NAME,
    embedding_model=EMBEDDING_MODEL,
    max_workers=8
)

# if there are any failures in indexing doc chunks, they will be written to a log file.
# You can resubmit those chunks using this method:

if os.path.exists(config.LOG_FILE):
    apollo.resubmit_failed_chunks(
        log_file=config.LOG_FILE, 
        texts=texts, 
        metadatas=metadatas, 
        ids=ids, 
        index_name=INDEX_NAME, 
        embedding_model=EMBEDDING_MODEL,
        max_workers=8
    )
```
After the indexing is completed, it is possible to query the RAG dataset with a test question.
This can be accomplished using the following script:

```python
apollo.query_index(
    user_query="YOUR QUERY HERE",
    num_chunks=5,
    index_name=INDEX_NAME,
    embedding_model=EMBEDDING_MODEL
)
```

#### Step 3: Build a Streamlit App

Now that we have indexed our documents in the RAG database, we can build a Streamlit
app to let users 'chat' with the document store.

To create the app, follow these steps:

1. Make sure you have the INDEX_NAME from the previous step
2. Create a file called `app.py` and use the following template. Make sure to change the custom prompt below if needed!
Changing the prompt is a crucial step to assure that the generation phase of the RAG conforms to your specific use case.
Invest some time in prompt engineering, to get the best out of the LLM used to generate the answers to the user queries.

```python
import streamlit as st
import pandas as pd
from bollm import azure, billo, utils

INDEX_NAME = os.getenv("INDEX_NAME")
azure_client = azure.load_azure_client()

st.title("Chat with Docs")

# Define Session State
if "messages" not in st.session_state:
   st.session_state.messages = []

if "used_tokens" not in st.session_state:
   st.session_state.used_tokens = 0

for message in st.session_state.messages:
   with st.chat_message(message["role"]):
      st.markdown(message["content"])

# Define Sidebar
with st.sidebar:
   model_type = st.selectbox("Select LLM:", ["GPT-4o", "GPT-4"])
   if model_type == "GPT-4":
      api = "billo"
      CONTEXT_WINDOW = billo.GPT_4_CONTEXT_WINDOW
   elif model_type == "GPT-4o":
      api = "azure"
      CONTEXT_WINDOW = azure.GPT_4o_CONTEXT_WINDOW
   else:
      st.warning("Selected model's context window unknown!")
   token_display = st.empty()
   with token_display.container():
      st.progress(st.session_state.used_tokens/CONTEXT_WINDOW, text = f"Context window used ({st.session_state.used_tokens} out of {CONTEXT_WINDOW})")
   temperature = st.slider("Select model creativity (temperature)", min_value=0.0, max_value=1.0, value = 0.0)
   chunk_num = st.slider("Select number of chunks", min_value=1, max_value=8, value=4)

# User Input
if user_query := st.chat_input("Ask a question"):
   st.session_state.messages.append({"role": "user", "content": user_query})
   with st.chat_message("user"):
      st.markdown(user_query)
   # RAG Output
   with st.chat_message("assistant"):
      context = billo.query_rag(user_query, chunk_num, INDEX_NAME)
	  #### ADAPT THE FOLLOWING PROMPT TO YOUR SPECIFIC NEEDS ####
      prompt = f"""\
         Use the following CONTEXT delimited by triple backticks to answer the QUESTION at the end. Additional context of the
         conversation between you and the user is provided by CHAT_HISTORY.
         
         If you don't know the answer, just say that you don't know.
         
         Use three to five sentences and keep the answer as concise as possible.
         
         You are also a language expert, and so can translate your responses to other languages upon request.
         
         CONTEXT: ```
         {context['docs']}
         ```

         QUESTION: ```
         {user_query}
         ```

         CHAT_HISTORY: ```
         {[{'role': m['role'], 'content': m['content']} for m in st.session_state.messages]}
         ```

         Helpful Answer:"""
      
      if api == "azure":
         response_full = azure.query_llm(
            client=azure_client,
            prompt=prompt,
            model_type=model_type,
            max_tokens=4096,
            temperature=temperature,
            seed=42,
            top_p = 0.1
         )
         response = azure.get_content(response_full)
         st.session_state.used_tokens = azure.get_token_usage(response_full)
      elif api == "billo":
         response_full = billo.query_llm(
            prompt=prompt, 
            model_type=model_type.lower(), 
            max_tokens=4096, 
            temperature=temperature,
         )
         response = billo.get_content(response_full)
         st.session_state.used_tokens = billo.get_token_usage(response_full)
      else:
         st.stop("Selected model type not yet implemented!")

      st.write(response)
      
      with st.sidebar:
         with token_display.container():
            st.progress(st.session_state.used_tokens/CONTEXT_WINDOW, text = f"Context window used ({st.session_state.used_tokens} out of {CONTEXT_WINDOW})")
         sources, titles = utils.extract_source(context)
         st.header("Sources:")
         st.table(pd.DataFrame({"Documents referenced": titles}))
         st.markdown(sources, unsafe_allow_html=True)
         
   st.session_state.messages.append({"role": "assistant", "content": response})
```

Then run `streamlit run app.py` to see if it works!

## For Developers

### Testing

```bash
pip install -e .
```

The `-e` flag in `pip install -e .` installs the package in "editable" mode, which means:
- Changes you make to the source code will be reflected immediately without reinstalling
- The package will be available in your Python environment just like a normal installed package
- You can import it with `import bollm` in your scripts

For unit testing, we'll use the `pytest` framework.

```bash
source .venv/bin/activate
pytest tests/
```

### Build

```bash
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade build wheel bumpversion
bumpversion patch # or major or minor
rm -rf dist
python setup.py sdist bdist_wheel
```

### Upload to PyPI

Requires a PyPI API Token. Get one at https://pypi.org

Set the token in your environment as `TWINE_PASSWORD`

```bash
source .venv/bin/activate
pip install --upgrade twine
twine upload --repository pypi dist/*
```
