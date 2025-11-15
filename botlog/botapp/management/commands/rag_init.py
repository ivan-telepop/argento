from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
# Docs processing
from langchain.agents import AgentState, create_agent
from langchain_community.document_loaders import WebBaseLoader
from langchain.messages import MessageLikeRepresentation
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embedings processing

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma

# envs and settings
import environ
from pathlib import Path
import os
from django.core.management.base import BaseCommand

# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# path to pdf files directory
pdf_files_directory = str(BASE_DIR) + '/pdf'


# PDF loader 
loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path=pdf_files_directory,
        glob="*.pdf",
    ),
    blob_parser=PyPDFParser(),
)
documents = loader.load()



# Data Processing 

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(documents)




# Embeding model
embeddings = OllamaEmbeddings(model="all-minilm") 

# ChromaDB
db = Chroma.from_documents(all_splits, embeddings, collection_name = "local-rag")

retriever = db.as_retriever()




template = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question:
If you don't know the answer, then answer from your own knowledge and dont give just one word answer, and dont tell the user that you are answering from your knowledge.
Use three sentences maximum and keep the answer concise.

Question: {question}
Context: {context}
Answer:

"""
prompt = ChatPromptTemplate.from_template(template)

local_model = "gemma3" # or llama3.2
llm = ChatOllama(model=local_model)

rag_chain = (
        {"context": retriever,  "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

# while True:
#     query = str(input("Enter Question: "))
#     print(rag_chain.invoke(query))








# running command
class Command(BaseCommand):
    help = 'Runs Contact RAG context  '
    print(len(documents))
    def handle(self, *args, **options):
        while True:
            query = str(input("Enter Question: "))
            print(rag_chain.invoke(query))