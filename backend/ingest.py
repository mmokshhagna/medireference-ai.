import os
# We use these specific paths because LangChain 2026 is modular
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def build_vector_db():
    data_path = "../data"
    persist_dir = "./chroma_db"
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print(f"Created {data_path} folder. Put PDFs there!")
        return

    print("Checking for PDFs...")
    loader = PyPDFDirectoryLoader(data_path)
    docs = loader.load()
    
    if not docs:
        print("Error: No PDFs found in the 'data' folder. Please add one.")
        return

    print(f"Splitting {len(docs)} pages into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print("Initializing embeddings (this may take a moment)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Building ChromaDB...")
    Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    print("\n✅ Success! Your clinical database is ready.")

if __name__ == "__main__":
    build_vector_db()
