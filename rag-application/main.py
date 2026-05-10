import os

from dotenv import load_dotenv
from langchain_core import embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

print("Initializing...")

# embeddings = OpenAIEmbeddings()
# llm = ChatOpenAI()

# vectorstore = PineconeVectorStore(index=os.environ("INDEX_NAME"), embedding=embeddings)