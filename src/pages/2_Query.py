import re
import streamlit as st
from utils.utilsllm import load_client

from utils.prompts import get_system_prompt
from tools.factory import retriever_factory

from utils.config_loader import load_config

import sys
from dotenv import load_dotenv, find_dotenv
from mistralai.models.chat_completion import ChatMessage


_ = load_dotenv(find_dotenv()) # read local .env file

# GLOBAL VARIABLES RETRIEVED WITH CONFIG
config = load_config()

app_name = config['DEFAULT']['APP_NAME']

database_source = config['DATABASE']['DATABASE_SOURCE']
retriever = retriever_factory(database_source)

MODEL = config['LLM']['LLM_MODEL']
CHAT_MODEL = config[MODEL]['CHAT_MODEL']

client = load_client()

if 'key' not in st.session_state:
    st.session_state['key'] = True


def build_response(messages):
    _response = ""

    _messages = [
        ChatMessage(
            # role="user" if i == 0 and m["role"] == "system" else m["role"],
            role=m["role"],
            content=m["content"]
        )
        for i, m in enumerate(messages)
    ]
    for chunk in client.chat_stream(
            model=CHAT_MODEL,
            messages=_messages,
    ):
        if chunk.choices[0].delta.content is not None:
            _response += (chunk.choices[0].delta.content or "")

    print(_response)
    return _response


def correct_code_markdown(llm_output, incorrect='vbnet', correct='sql'):
    corrected_output = None
    # Check if llm_output is not None and doesn't already contain the correct language specifier.
    if llm_output and f"```{correct}" not in llm_output:
        corrected_output = llm_output.replace(f"```{incorrect}", f"```{correct}")
    else:
        # If it already contains the correct language specifier, just return the original output.
        corrected_output = llm_output
    return corrected_output


_INTRO = f"""To get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
Then provide 3 example questions WITHOUT the sql query using bullet points. 

If you haven't been asked, speak in french."""

st.title(app_name)



if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    system_prompt = get_system_prompt()
    st.session_state.messages_query = [{"role": "system", "content": system_prompt}]
    # for mistral send a initial user message to initiate conversation
    # not needed for GPT, can be assistant
    st.session_state.messages_query.append({"role": "user", "content": "How can you help?"})

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages_query.append({"role": "user", "content": prompt})

if len(st.session_state.messages_query) > 1:
    st.write(st.session_state.messages_query[1]["content"])

# display the existing chat messages
for message in st.session_state.messages_query[2:]:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        if "results" in message:
            if message["results"].empty:
                st.write("Votre demande a été prise en compte : Aucune donnée n'a été trouvée")
            else:
                st.dataframe(message["results"], hide_index=True)


# If last message is not from assistant, we need to generate a new response
if st.session_state.messages_query[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        response = build_response(st.session_state.messages_query)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        # was used while Mistral was returing vbnet markdown instead of sql.
        # some prompt engineering techniques make it works
        # response = correct_code_markdown(response)
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)

        exception = False
        if sql_match:
            sql = sql_match.group(1)
            try:
                result = retriever.run_query(sql)
            except Exception as e:
                print(f"Something went wrong... the error is:{e}")
                print(f"Query is {sql}")
                expander = st.expander("See explanation")
                expander.write(response)
                errorExpander = st.expander("**Sorry, an error occured**")
                errorExpander.write(f"Something went wrong... the error is:{e}")
                exception = True
                
            if exception is False:
                if result.empty:
                    st.write("No result.")
                else:
                    st.dataframe(result, hide_index=True)

                message["results"] = result
        st.session_state.messages_query.append(message)
        if st.session_state['key']:  # check if it is the first time
            st.session_state['key'] = False  # change the variable to false
            resp_container.markdown(response)
        else:
            if exception is False:
                expander = st.expander("See explanation")
                expander.write(response)

