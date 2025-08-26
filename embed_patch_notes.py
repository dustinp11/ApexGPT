import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import re
from typing import List, Dict

class PatchNotesRAG:
    def __init__(self, db_path: str = "my_chroma_db"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection_name = "patch_notes"
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Apex Legends patch notes for RAG"}
            )
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def embed_patch_notes(self, patch_file: str = "latest_patch_notes.txt"):
        if not os.path.exists(patch_file):
            return False
        
        with open(patch_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        chunks = self.chunk_text(content)
        
        if not chunks:
            return False
        
        embeddings = self.model.encode(chunks)
        
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": "patch_notes", "chunk_id": i} for i in range(len(chunks))]
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        return True
    
    def query(self, question: str, n_results: int = 3) -> str:
        query_embedding = self.model.encode([question])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant information found in patch notes."
        
        context = "\n\n".join(results['documents'][0])
        
        from gpt_bot import llm
        
        prompt = f"""Based on the following Apex Legends patch notes context, answer the user's question accurately and concisely. 
        If the information isn't in the context, say so clearly.
        
        Context from patch notes:
        {context}
        
        Question: {question}
        
        Answer:"""
        
        return llm([{"role": "user", "content": prompt}])
    
    def clear_collection(self):
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Apex Legends patch notes for RAG"}
            )
        except:
            pass

rag_system = PatchNotesRAG()

def main():
    print("Embedding patch notes into ChromaDB...")
    
    rag_system.clear_collection()
    
    success = rag_system.embed_patch_notes()
    
    if success:
        print("Embedded patch notes into ChromaDB!")
        print("You can now use the RAG system to answer questions about patch notes.")
    else:
        print("Failed to embed patch notes. Make sure latest_patch_notes.txt exists.")
        return False
    
    return True

if __name__ == "__main__":
    main()