# rag_system.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGSystem:
    def __init__(self):
        self.vector_store = None
        self.rag_chain = None

    def setup(self, file_path):
        # Load and split the PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        
        # Create vector store
        self.vector_store = Chroma.from_documents(pages, OpenAIEmbeddings())
        
        # Create retriever
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        
        # Create LLM
        llm = ChatOpenAI(model="gpt-4o-mini")
        
        # Create RAG chain
        prompt = hub.pull("rlm/rag-prompt")
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def answer_question(self, question):
        if not self.rag_chain:
            return "The RAG system hasn't been set up yet. Please upload a PDF first."
        return self.rag_chain.invoke(question)
    
    def is_ready(self):
        return self.rag_chain is not None