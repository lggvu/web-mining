from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.vectorstores import Chroma, Qdrant
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
import re
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)
from langchain.prompts import PromptTemplate

from langchain.prompts import MessagesPlaceholder
from langchain.agents import tool 
from langchain.chains import LLMChain
from langchain.tools import tool

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv(".env")
import os 

import requests
from langchain.tools import StructuredTool
from typing import Optional, Type

from SearchContext import *
from constants import *
from embedding import *

def create_agent(embedding_model):
    # qa_data = CSVLoader("../db_csv/full_qa.csv").load()
    product_data = CSVLoader("../db_csv/all_product_full_info.csv").load()

    product_vectorstore = Chroma.from_documents(documents=product_data, embedding=OpenAIEmbeddings())
    # qa_vectorstore = Chroma.from_documents(documents=qa_data, embedding=OpenAIEmbeddings())


    data_tool = create_retriever_tool(
        product_vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .7, "k": 2}),
        "production_information_retriever",
        "useful for when you need to answer questions about the price of the products."
    )


    @tool
    def search_elasticsearch(question: str):
        """Search for simple information of products, when the question is not related to prices."""
        contexts = search(question=question, embedding_model=embedding_model, search_type="hybrid", threshold=0.5)
        print("retrieved context: ", contexts)
        return transform(contexts)

    @tool
    def finish_llm(*kwargs):
        """useful when you need to end the conversation"""
        return "Ask the customer for their personal information to help them connect to a salesperson."

    tools = [data_tool, search_elasticsearch, finish_llm]
    llm = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0.4)

    message = SystemMessage(
        content=(
            "You are a helpful virtual advisor named Lily. You can help customers answer questions about laptops. Your final goal is to help customer buy a suitable laptop."
            "If you cannot decide a final product, feel free to ask follow up questions to narrow down the search."
            "If the user decide to end the conversation, ask for their personal information to help them connect to a salesperson."
            "The answer is given in Vietnamese. Always answer in Vietnamese language."
        )
    )
    memory = AgentTokenBufferMemory(llm=llm, memory_key="history", max_token_limit=200)
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name="history")],
    )
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
    )
    return agent_executor


if __name__ == "__main__":
    agent_executor = create_agent(init_model())
    while True:
        prompt = str(input("Nhập câu hỏi: \n"))
        # prompt = "xin chào"
        response = agent_executor.invoke({"input":prompt})
        print(response["output"])
