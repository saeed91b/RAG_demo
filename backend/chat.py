from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from db import VectorStore


class Chat:
    def __init__(self):
        load_dotenv()
        self.vector_store = VectorStore()
        self.chat_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"))
        self.chat_model.streaming = True
        self.qa = RunnableLambda(self._qa)


    def set_db(self):
        self.vector_store.set_db()


    def _qa(self, question):
        prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context: {context} Question: {question}""")

        try:
            retriever = self.vector_store.get_db()
            docs = retriever.invoke(question)
            formatted = prompt.invoke({"context": docs, "question": question})
            return self.chat_model.invoke(formatted)
        
        except FileNotFoundError:
            return "PDF file not found. Please make sure the file exists in the './data/' directory."