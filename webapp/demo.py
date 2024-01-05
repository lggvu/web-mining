from dotenv import load_dotenv
load_dotenv()

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
from agent import *
from streamlit_profiler import Profiler
from langsmith import Client


from SearchContext import *
from LLMModel import *
import embedding
import constants 

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

client = Client()

st.set_page_config(
    page_title="Laptop VA",
)

st.subheader("Virtual Assistant for Laptop Stores")


if "model" not in st.session_state:
    st.session_state.model = embedding.init_model()
    print("embedding model loaded!")
# if "chain" not in st.session_state:
#     st.session_state.chain = get_chain()
#     print("chain loaded!")

if "agent" not in st.session_state:
    st.session_state.agent = create_agent(st.session_state.model)
    print("agent loaded!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)
    # context = search(prompt, embedding_model=st.session_state.model, search_type="vector", threshold=.3)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        # llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
        # response = llm(st.session_state.messages)
        # agent_executor = create_agent()
        input_dict = {"input": prompt}
        # response = st.session_state.chain.run(input_dict)
        response = st.session_state.agent.invoke(input_dict)
        print(response)
        st.write(response["output"])

        st.session_state.messages.append(ChatMessage(role="assistant", content=response["output"]))