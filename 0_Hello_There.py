import streamlit as st
import configparser


def main():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.stodo')

    st.set_page_config(
        page_title="this is not called stodo · Hello",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    st.title("stodo")

    if st.session_state["logged_in"] is True:
        st.image("Assets/jasraj.png")
        st.text(f"You're logged in as {st.session_state['user']}")
    else:

        user = st.text_input("Username")

        try:
            if config[user]:
                password = st.text_input("Password")

                if password == config[user]["password"] == password:
                    st.session_state['logged_in'] = True
                    st.session_state["user"] = config[user]["name"]
                    st.session_state["penguin"] = config[user]['penguin']
                    st.session_state['tdl'] = config[user]["tdl"].split("`")
                    st.session_state['tdfl'] = config[user]["tdfl"].split("`")
                    st.session_state['cmpl'] = config[user]["cmpl"].split("`")
                    st.session_state['ltcmpl'] = config[user]["ltcmpl"].split("`")
                    st.session_state['num_complete'] = int(config[user]["num_complete"])

                    with open('user_data.stodo', 'w') as configfile:
                        config.write(configfile)

                    st.experimental_rerun()

        except KeyError:
            st.text("Enter your credentials")
            if user is not "" and user not in config:
                config.add_section(user)
                config[user]["name"] = user
                config[user]['penguin'] = "Assets/motivation_penguin.gif"
                config[user]["tdl"] = ""
                config[user]["tdfl"] = ""
                config[user]["cmpl"] = ""
                config[user]["ltcmpl"] = ""
                config[user]['num_complete'] = "0"

                st.session_state["user"] = user
                st.session_state["penguin"] = "Assets/motivation_penguin.gif"
                st.session_state['tdl'] = []
                st.session_state['tdfl'] = []
                st.session_state['cmpl'] = []
                st.session_state['ltcmpl'] = []
                st.session_state['num_complete'] = 0
                password = st.text_input("Set a password", type="password")
                st.text("do NOT use a password you care about. I beg of you, I do not want access to your passwords. DO NOT GIVE THEM TO ME.")
                set_password = st.button("Save new password")

                if set_password is True and password is not "":
                    config[user]["password"] = password

                    with open('user_data.stodo', 'w') as configfile:
                        config.write(configfile)
                        st.session_state['logged_in'] = True

                    st.experimental_rerun()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
