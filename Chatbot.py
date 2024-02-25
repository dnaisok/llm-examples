import requests
import streamlit as st

# 自定义的OpenAI API请求地址
custom_openai_api_url = "Https://one.789ai.top/v1/chat/completions"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": "你好"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"  # 使用OpenAI API密钥
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": st.session_state.messages
    }

    # 发送POST请求到自定义的OpenAI API地址
    response = requests.post(custom_openai_api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        msg = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    else:
        st.error(f"Error: {response.text}")
