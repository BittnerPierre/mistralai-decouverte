import mistralai
import streamlit as st

from utils.utilsllm import load_client
from utils.config_loader import load_config

from dotenv import load_dotenv, find_dotenv
from mistralai.models.chat_completion import ChatMessage

# read local .env file
_ = load_dotenv(find_dotenv())

# GLOBAL VARIABLES RETRIEVED WITH CONFIG
config = load_config()

app_name = config['DEFAULT']['APP_NAME']

database_source = config['DATABASE']['DATABASE_SOURCE']

MODEL = config['LLM']['LLM_MODEL']
CHAT_MODEL = config[MODEL]['CHAT_MODEL']

client = load_client()

st.title("Mistral assistant")

INIT1_PIRATE = """
You will be acting as an AI Pirate Assistant named Barbarossa.

Now to get started, please briefly introduce yourself and ask how you can help ?
"""

INIT2_PYTHON = """You are a python code assistant that will try to give correct and elegant solution.

Please adhere to the following guidelines in your responses:
1. Understand and analyze the questions or problems presented by the developer. 
2. Ask explanation if question is unclear or incomplete.
3. Identify the invariable input of the problem such as response produced by an external system or library.
4. Understand the outcome expected by the user.
5. Keep your solution as simple as possible without requiring installation of library or replacement of components.
6. Give an elegant solution in python code that can be applied by user in python.
7. Wrap your code with ``` block code markdown  
8. Separate variable declaration and function definition and example in different block code markdown for clarity.
9. Explain the problem you have identify and then the solution that you have apply.
10. List briefly potential alternatives in python that the user could investigate but do not develop.
"""

INIT2_PYTHON_ASSISTANT = """
s a Python code assistant, your role is to provide precise, efficient and secure Python solutions. 
Include brief code examples where relevant. 
Focus on:
1. Correct Python syntax and best practices.
2. Performance optimization and security.
3. Clarity and brevity, suitable for various skill levels.
4. Current Python trends and updates.

Assist with coding, debugging, algorithms, and library use, emphasizing Pythonic and ethical practices."""


if "messages" not in st.session_state.keys():
    st.session_state.messages_chatbot = [{"role": "system", "content": INIT1_PIRATE}]
    st.session_state.messages_chatbot.append({"role": "assistant", "content": "How can I help?"})

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages_chatbot.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages_chatbot:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages_chatbot[-1]["role"] != "assistant":
    # Call LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ""
            # old OPENAI API
            # r = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            # )
            # response += r.choices[0].message.content

            resp_container = st.empty()
            for chunk in client.chat_stream(
                    model=CHAT_MODEL,
                    messages=[ChatMessage(role=m["role"], content=m["content"]) for i, m in
                              enumerate(st.session_state.messages_chatbot)],
            ):
                if chunk.choices[0].delta.content is not None:
                    response += (chunk.choices[0].delta.content or "")
                    resp_container.markdown(response)

    # st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages_chatbot.append(message)
