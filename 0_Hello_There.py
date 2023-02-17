import streamlit as st
import configparser
import time


def main():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.stodo')

    st.set_page_config(
        page_title="Photogrudo · Hello",
        layout="centered",
        initial_sidebar_state="auto"
    )

    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "sign_in" not in st.session_state:
        st.session_state["sign_in"] = ""

    st.title("Photogrudo has moved to photogrudesh.zapto.org")
    st.write("photo-gru-doo")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()