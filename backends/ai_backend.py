import hashlib
import os
from typing import Generator, Union, List, AsyncIterator, Dict, Any
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

def get_context(retriever, question):
    relevant_docs = retriever.invoke(question)
    return format_docs(relevant_docs)

def process_input(input_dict: Dict[str, Any], retriever) -> Dict[str, Any]:
    return {
        "context": get_context(retriever, input_dict["question"]),
        "question": input_dict["question"],
    }

class InputProcessor:
    def __init__(self, retriever):
        self.retriever = retriever

    def __call__(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        return process_input(input_dict, self.retriever)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def load_and_process_document(file_path: str):
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)

class ChatAI():
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "data.docx")

        self.vectorstore = None
        self.chunks = None

        self.llm = ChatGroq(
            groq_api_key=os.getenv('GROQ_API_KEY'),
            model="llama3-70b-8192",
        )
        self.embeddings_model = CohereEmbeddings(
            cohere_api_key=os.getenv('COHERE_API_KEY'),
            model="embed-english-v3.0",
        )

        self.prompt_template = """
            You are an AI assistant for the Computer Science Department of Akanu Ibiam Federal Polytechnic Unwana.

            Your role is to:
            1. Provide helpful, accurate information about the department using only the retrieved context
            2. Answer questions about courses, faculty, facilities, admission requirements, and other department-related matters
            3. Maintain a professional and friendly tone representing the department
            4. Clearly state when information is not available in your knowledge base

            Retrieved Context:
            {context}

            Question:
            {question}

            Instructions:
            - If the question relates to the Computer Science Department at Akanu Ibiam Federal Polytechnic Unwana, provide a direct, informative answer based solely on the context.
            - If the answer isn't found in the context, respond with: "Based on my information about the Computer Science Department at Akanu Ibiam Federal Polytechnic Unwana, I don't have specific details about that. You may want to contact the department directly for more information."
            - If the question is completely unrelated to the Computer Science Department or Akanu Ibiam Federal Polytechnic, respond with: "I'm specifically designed to answer questions about the Computer Science Department at Akanu Ibiam Federal Polytechnic Unwana. Your question appears to be outside that scope. Is there something specific about the department or institution I can help you with?"

            Please provide a helpful response based on these guidelines.
            """
        self.k = 5
        self.initialize_resources()

    def initialize_resources(self):
        """Initialize document chunks and vectorstore once at startup"""
        if self.chunks is None:
            self.chunks = load_and_process_document(self.file_path)
        
        if self.vectorstore is None:
            # Simple approach with persistent directory
            self.vectorstore = Chroma.from_documents(
                documents=self.chunks,
                embedding=self.embeddings_model,
                persist_directory="./chroma_db"
            )
            
    def create_vectorstore(self):
        # Just return the already initialized vectorstore
        return self.vectorstore
    
    def setup_qa_chain(self, vectorstore):
        retriever = vectorstore.as_retriever()

        template = self.prompt_template
        prompt = ChatPromptTemplate.from_template(template)

        model = self.llm

        input_processor = InputProcessor(retriever)
        return (
            RunnablePassthrough() |
            input_processor |
            prompt |
            model
        )

    def ask_question(self, query, stream=False):
        qa_chain = self.setup_qa_chain(self.vectorstore)

        if stream:
            return self._astream_response(qa_chain, query)
        else:
            return self._get_full_response(qa_chain, query)

    def _stream_response(self, chain, query) -> Generator[str, None, None]:
        answer = ""
        for chunk in chain.stream({"question": query}):
            yield chunk.content
            answer += chunk.content
        # self.save_message(query, answer)

    def _astream_response(self, chain, query) -> AsyncIterator[str]:
        return chain.astream({"question": query})

    def _get_full_response(self, chain, query: str) -> str:
        response = chain.invoke({"question": query})
        return response.content



# while True:
#     question = input("Enter a question: ")
#     full_response = ai.ask_question(question)
#     print(full_response)


# def process_message(message):
#     """Process a message and get AI response."""
#     return ai.ask_question(message)