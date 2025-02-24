from langchain_upstage import UpstageEmbeddings;import os;from dotenv import load_dotenv;load_dotenv()
 
embeddings=UpstageEmbeddings(api_key=os.getenv("upstage"),model="embedding-query")
 
doc_result=embeddings.embed_documents(["Sam is a teacher.", "This is another document"]);print(f"doc result: {doc_result}")
 
query_result = embeddings.embed_query("What does Sam do?");print(f"query result: {query_result}")