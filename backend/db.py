from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from pathlib import Path

DATA_DIR = Path("./data")
FILE_DIR = DATA_DIR / "file.pdf"


class VectorStore:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.db = None


    def set_db(self):
        raw_documents = PyPDFLoader(FILE_DIR).load()
        documents = self.text_splitter.split_documents(raw_documents)
        self.db = InMemoryVectorStore.from_documents(documents, self.embedding_model)


    def get_db(self):
        if self.db is None:
            if not FILE_DIR.is_file():
                raise FileNotFoundError("PDF file not found")

            self.set_db()

        return self.db.as_retriever()

