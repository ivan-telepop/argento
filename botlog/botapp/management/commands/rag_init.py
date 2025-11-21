from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
# Docs processing
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_core.output_parsers.string import StrOutputParser

# Embedings processing
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

# prompts
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough




# envs and settings
import environ
from pathlib import Path
import os
from django.core.management.base import BaseCommand

# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# path to pdf files directory - test path
pdf_files_directory = '/home/ewan/Desktop/Dev/argento/botlog/pdf/Grant_Bank_01.pdf'#Path(os.path.join(BASE_DIR).join(['/pdf/']) )     #str(BASE_DIR) + '/pdf'


print(pdf_files_directory)


# PDF loader 
def load_pdf_docs(pdf_files_directory: str):
    """ Method that gets file path string then returns loaded docs
    Args:
        pdf_files_directory (str): directory or url with PDF files 
    Returns:
        _type_: Loaded docs
    """
    print(pdf_files_directory,": The path is")
    try:
        
        loader = PyPDFLoader(pdf_files_directory)
        docs = loader.load()
        return docs
    except Exception as e:
        print(e)
    


# Blob loader of PDF

def blob_load_pdf(pdf_files_directory):
    """Method loads blob or directory of files
    Args:
        pdf_files_directory (_type_): _description_
    Returns:
        _type_: _description_
    """
    loader = GenericLoader(
        blob_loader=FileSystemBlobLoader(path=pdf_files_directory,glob="*.pdf",),
        blob_parser=PyPDFParser(),)
    documents = loader.load()
    return documents 
    
    
    
# Blob Loading files    


prepared_docs = load_pdf_docs(pdf_files_directory=pdf_files_directory)



def split_pdf_documents(documents, chunk_size=1000, chunk_overlap=20):
    text_split = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_split.split_documents(documents)
    return chunks


splat_chunks = split_pdf_documents(documents=prepared_docs)


embeddings = OllamaEmbeddings(model="all-minilm") 

vector_store = Chroma.from_documents(splat_chunks, embeddings, collection_name = "local-rag")

retriever = vector_store.as_retriever()
    




chat_template = """
Отвечай на русском языке, в контектсе загруженных документов.
В начале чата всегда приветствуй, отвечай четко по существу.
Отвечая на вопросы добавляй свои рассуждения и мысли практично.
Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(chat_template)
llm = ChatOllama(model="llama3.2")

rag_chain = (
        {"context": retriever,  "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)
# running command
class Command(BaseCommand):
    help = 'Runs Contact RAG context  '
    print(len(pdf_files_directory))
    def handle(self, *args, **options):
        while True:
            query = str(input("Enter Question: "))
            print(rag_chain.invoke(query))