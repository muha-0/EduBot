import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_pinecone import PineconeVectorStore


def load_docs(dir):
    docs = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        txtLoader = TextLoader(file_path=filepath)
        docs.append(txtLoader.load()[0])
    return docs


documents = load_docs(r'C:\Users\Aurora\Desktop\bot')


def split_docs(documents, chunk_size=500, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs


docs = split_docs(documents)
print(len(docs))

embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
print(len(embeddings.embed_query("Hello world")))

os.environ['PINECONE_API_KEY'] = 'd735e8ad-5744-4ccf-9c71-6ad3a09cf818'

index_name = "eui"
index = PineconeVectorStore.from_documents(
    docs,
    index_name=index_name,
    embedding=embeddings
)
