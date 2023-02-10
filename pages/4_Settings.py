import streamlit as st


def main():
    if st.session_state["logged_in"] is True:
        st.set_page_config(
            page_title="this is not called stodo · Settings",
            layout="centered",
            initial_sidebar_state="collapsed",
        )
        pass
    else:
        st.error("Log in please")


if __name__ == '__main__':
    main()
