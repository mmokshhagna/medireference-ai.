from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma

app = FastAPI()

# Allow Streamlit to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Load the Database
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Setup Llama 3.2 1B
llm = ChatOllama(model="llama3.2:1b")

class Query(BaseModel):
    question: str

@app.post("/api/ask")
async def ask(data: Query):
    try:
        # --- THE DIRECT RAG PIPELINE (No 'chains' needed!) ---
        
        # Step A: Search the database for the 3 most relevant medical chunks
        docs = db.similarity_search(data.question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Step B: Build the strict prompt with our context injected
        prompt = f"""You are a clinical assistant. Answer the medical question based ONLY on the context below. 
        If the context does not contain the answer, say "I cannot find this in the provided documents."
        
        Context:
        {context}
        
        Question: {data.question}"""
        
        # Step C: Send directly to Llama 3.2
        response = llm.invoke(prompt)
        
        # Langchain ChatModels return an object, we just want the text (.content)
        return {"answer": response.content}
        
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
