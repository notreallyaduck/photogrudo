import streamlit as st


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] is True:
        st.set_page_config(
            page_title="Photogrudo · Settings",
            layout="centered",
            initial_sidebar_state="collapsed",
        )

        if "cmpl" not in st.session_state:
            st.session_state['cmpl'] = []

        for i in st.session_state["tdl"]:
            if i == "":
                st.session_state["tdl"].remove(i)

        for i in st.session_state["tdfl"]:
            if i == "":
                st.session_state["tdfl"].remove(i)

        for i in st.session_state["cmpl"]:
            if i == "":
                st.session_state["cmpl"].remove(i)

        for i in st.session_state["ltcmpl"]:
            if i == "":
                st.session_state["ltcmpl"].remove(i)

        if "cmpl" not in st.session_state:
            st.session_state['cmpl'] = []

        st.title("Settings")
        st.write("The pinnacle of customisation")

    else:
        st.error("Log in please")


if __name__ == '__main__':
    main()
