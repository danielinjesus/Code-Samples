from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_simple_rag():
    # 1. Load your documents
    loader = TextLoader("sample.txt")
    documents = loader.load()
    
    # 2. Split documents into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # 3. Create embeddings and store them
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    
    # 4. Create a retriever
    retriever = db.as_retriever()
    
    # 5. Create a chain
    llm = ChatOpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    return qa_chain

def main():
    # Create a sample text file
    with open("sample.txt", "w") as f:
        f.write("""
        LangChain is a framework for developing applications powered by language models.
        It enables applications that are context-aware and reason about their responses.
        RAG (Retrieval Augmented Generation) is a technique that combines retrieval of relevant documents
        with generation of responses using language models.
        """)
    
    # Create and use the RAG chain
    qa_chain = create_simple_rag()
    
    # Ask a question
    query = "What is LangChain and RAG?"
    result = qa_chain.invoke({"query": query})
    print(f"Question: {query}")
    print(f"Answer: {result['result']}")

if __name__ == "__main__":
    main() 