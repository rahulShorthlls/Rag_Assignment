import os
from langchain_chroma import Chroma
from dotenv import load_dotenv
from Split_data_in_chunk import SplitDataInChunkSaveChromaDB
load_dotenv()
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

class ChromaDBRetriever:
    def __init__(self, db_dir="../db", embedding_model="text-embedding-3-small"):
        """Initializes the ChromaDB retriever with the given persistent directory and embedding model."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.persistent_directory = os.path.join(current_dir, db_dir)
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

        # Load the existing vector store with the embedding function
        self.db = Chroma(persist_directory=self.persistent_directory,
                         embedding_function=self.embeddings)

    def retrieve_documents(self, query, k=5, score_threshold=0.3):
        """Retrieves relevant documents based on the query using similarity search."""
        retriever = self.db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": k, "score_threshold": score_threshold}
        )
        relevant_docs = retriever.invoke(query)

        return relevant_docs
    def check_db_size(self):
        """Check the number of stored documents in ChromaDB."""
        collection = self.db.get()
        print(f"Total documents in ChromaDB: {len(collection['ids'])}")

    def display_results(self, query):
        """Fetches and displays relevant results for the given query."""
        relevant_docs = self.retrieve_documents(query)

        print("\n--- Relevant Documents ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"Document {i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")
    
    
    

# if __name__ == "__main__":
#     query = "How did Mohammed Shami and Kuldeep Yadav perform in their comeback match against England?"
#     a = SplitDataInChunkSaveChromaDB()
#     a.save_chunks_into_chroma_db()
#     retriever = ChromaDBRetriever()
#     # retriever.display_results(query)
#     retriever.chatbot(query)
