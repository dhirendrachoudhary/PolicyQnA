import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_elasticsearch import ElasticsearchStore
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings import OpenAIEmbeddings

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_chunk_persist_pdf():
    # path to the PDF folder
    pdf_folder_path = "pdfs"
    
    # Load PDF documents from the pdf folder
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    
    # Split the loaded documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    
    # Initialize ElasticsearchStore with chunked documents
    db = ElasticsearchStore.from_documents(
        chunked_documents,
        OpenAIEmbeddings(),
        es_url="http://elasticsearch:9200",
        index_name="policy-qa",
    )
    return db

def create_agent_chain():
    # Initialize ChatOpenAI with the key
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    
    # Load the QA chain
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def get_llm_response(query, db):
    # Create a ChatOpenAI instance
    chain = create_agent_chain()
    
    # Search for similar documents in Elasticsearch
    matching_docs = db.similarity_search(query)
    
    # Run the QA chain on the matching documents
    answer = chain.run(input_documents=matching_docs, question=query)
    
    # Extract sources from matching documents' metadata
    sources = set(doc.metadata.get('source', '') for doc in matching_docs)
    
    # Return answer and sources
    return [answer, sources]
