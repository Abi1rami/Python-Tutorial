import os
os.environ["HF_TOKEN"] = "hf_your_token_here"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

texts = ["Hello world", "LangChain is great", "Embeddings are useful"]

# Create Chroma vectorstore
db = Chroma.from_texts(
    texts=texts,
    embedding=embed,
    persist_directory="./chroma_db"  
)
