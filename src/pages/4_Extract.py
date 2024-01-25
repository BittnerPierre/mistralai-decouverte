import os

import streamlit as st
from langchain.output_parsers import PydanticOutputParser


from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from utils.utilsdoc import load_doc

from models.statutes import Societe

from utils.config_loader import load_config

config = load_config()

model = config['LLM']['LLM_MODEL']


_EXTRACTION_TEMPLATE = """Extract and save the relevant entities mentioned \
in the following passage together with their properties.

Only extract the properties mentioned between the information_extraction tags below.

<information_extraction>
{information_extraction}
</information_extraction>

If a property is not present and is not required in the information_extraction, do not include it in the output.

Passage:
{input}"""


def load_sidebar():
    with st.sidebar:
        st.header("Parameters")
        st.sidebar.checkbox("Mistral", model == "MISTRAL", disabled=True)


def main():
    st.title("📄Personne Morale Extractor 🤗")
    load_sidebar()

    model_name = st.sidebar.radio("Model", ["mistral-tiny", "mistral-small", "mistral-medium"], index=1)

    template = st.sidebar.text_area("Prompt", _EXTRACTION_TEMPLATE)

    option = "Extract KBIS"

    if option is not None:
        pdfs = st.file_uploader("Upload Doc", type='pdf', accept_multiple_files=True)

        if (pdfs is not None) and (len(pdfs)):
            docs = load_doc(pdfs)
            if option == 'Extract KBIS':

                # #client = load_model()
                # chain = create_extraction_chain_pydantic(pydantic_schema=Societe, llm=llm, verbose=verbose)
                # extracts = chain.run(docs)
                # societe: Societe = extracts[0]
                #
                # st.header("Societe")
                # st.subheader("Entreprise")
                # st.write(societe.enterprise)
                # # sp.pydantic_output(societe.enterprise)

                api_key = os.environ["MISTRAL_API_KEY"]
                client = MistralClient(api_key=api_key)

                pydantic_parser = PydanticOutputParser(pydantic_object=Societe)
                format_instructions = pydantic_parser.get_format_instructions()

                content = _EXTRACTION_TEMPLATE.format(information_extraction=format_instructions,
                                                               input=docs)

                chat_response = client.chat(
                    model=model_name,
                    messages=[ChatMessage(role="user", content=content)],
                )
                st.write(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
