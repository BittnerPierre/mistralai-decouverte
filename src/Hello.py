import streamlit as st
import sys
from utils.config_loader import load_config

config = load_config()

app_name = config['DEFAULT']['APP_NAME']

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


def main():
    st.title(f"""Welcome to {app_name} ! 👋""")

    st.markdown(
        """
        Mistral AI decouverte. Select a demo on side bar
    """
    )
    st.write(sys.version)


if __name__ == "__main__":
    main()
