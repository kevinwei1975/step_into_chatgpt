from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.llms import OpenAI
from langchain_community.chat_models import  ChatTongyi
import streamlit as st
import os
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"
openai_api_key = st.sidebar.text_input('通义密钥')

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("请输入通义密钥再继续。")
        st.stop()
    llm = ChatTongyi(temperature=0.7, model="qwen-plus",dashscope_api_key=openai_api_key, streaming=True)
    # llm = ChatTongyi(
    #     dashscope_api_key="sk-7f890e8ea11d4855aa7ba9a0ddc88777",
    #     model="qwen-plus",
    #     temperature=0.7,
    # )
    tools = load_tools(["ddg-search"])
    # 创建 Agent
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        # 通过回调方式展示 LLM 思考和行为
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
