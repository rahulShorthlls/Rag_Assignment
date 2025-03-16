from chromaDBRetriber import ChromaDBRetriever
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from Split_data_in_chunk import SplitDataInChunkSaveChromaDB
load_dotenv()
class RAG_CHABOT:
    def __init__(self):
        pass
    def chatbot(self,query):
        chromaRe = ChromaDBRetriever()

        relevant_docs = chromaRe.retrieve_documents(query)
        combined_input = (
            # "Who are the three uncapped players in Pakistan's squad for the 1st T20I against New Zealand? "
            query
            + query
            + "\n\nRelevant Documents:\n"
            + "\n\n".join([doc.page_content for doc in relevant_docs])
            + "\n\nPlease provide a rough answer with meta deta based only on the provided documents. If the answer is not found in the documents, respond with 'I'm not sure'."
        )

        # Create a ChatOpenAI model
        model = ChatOpenAI(model="gpt-4o")

        # Define the messages for the model
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=combined_input),
        ]

        # Invoke the model with the combined input
        result = model.invoke(messages)

    
        
        # print(result.content)
        return result.content
    
# if __name__ == "__main__":
#     query = "How did Mohammed Shami and Kuldeep Yadav perform in their comeback match against England?"
#     a = SplitDataInChunkSaveChromaDB()
#     a.save_chunks_into_chroma_db()
#     rag = RAG_CHABOT()
#     print(rag.chatbot(query))