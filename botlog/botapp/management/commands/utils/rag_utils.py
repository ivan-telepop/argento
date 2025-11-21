from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_community.document_loaders import PyPDFLoader
# Docs processing
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
# ollama 
from langchain_ollama.embeddings import OllamaEmbeddings 
from langchain_community.vectorstores import Chroma

# envs and settings
import environ
from pathlib import Path
import os

# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# path to pdf files directory
pdf_files_directory = Path('/home/ewan/Desktop/Dev/argento/botlog/pdf')  #os.path.join(BASE_DIR).join(['/pdf'])      #str(BASE_DIR) + '/pdf'





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
#prepared_docs = blob_load_pdf(pdf_files_directory=pdf_files_directory)

prepared_docs = load_pdf_docs(pdf_files_directory=pdf_files_directory)

print("Prepared Docs", prepared_docs)

def split_pdf_documents(documents, chunk_size=1000, chunk_overlap=20):
    text_split = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_split.split_documents(documents)
    return chunks


splat_chunks = split_pdf_documents(documents=prepared_docs)

print(splat_chunks,"Prepared Docs")

# print(f"Total number of chunks: {len(splat_chunks)}")
# # print("\n")






from langchain_core.documents import Document

# document_1 = Document(page_content="foo", metadata={"baz": "bar"})
# document_2 = Document(page_content="thud", metadata={"bar": "baz"})
# document_3 = Document(page_content="i will be deleted :(")

# documents = [document_1, document_2, document_3]
# ids = ["1", "2", "3"]
# vector_store.add_documents(documents=documents, ids=ids)





embeddings = OllamaEmbeddings(model="Gemma3") 

vector_store = Chroma.from_documents(splat_chunks, embeddings, collection_name = "local-rag")

retriever = vector_store.as_retriever()
    




