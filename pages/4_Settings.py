import streamlit as st


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

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
