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
        initial_sidebar_state="expanded",
    )

    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "sign_in" not in st.session_state:
        st.session_state["sign_in"] = ""

    st.title("Photogrudo")

    if st.session_state["logged_in"] is True:
        # st.image(f"Profile Pictures/{st.session_state['user']}")
        st.write(f"You're logged in as {st.session_state['user']}")
        st.write("Go to the overview page in the sidebar for your to do list. (Press the little arrow to expand the sidebar)")
        st.write("I'm still making this thing, information may be subject to deletion.")
        log_out = st.button("Log out of photogrudo")
        if log_out is True:
            del st.session_state["user"]
            del st.session_state["penguin"]
            del st.session_state['tdl']
            del st.session_state['tdfl']
            del st.session_state['cmpl']
            del st.session_state['ltcmpl']
            del st.session_state['num_complete']
            del st.session_state["times_to_complete"]
            del st.session_state["logged_in"]
            del st.session_state["sign_in"]
            st.experimental_rerun()
    else:
        if st.session_state["sign_in"] == "":
            st.write("Let's get started")

            new_user = st.button("Make an account!")
            returning_user = st.button("Sign in")

            if new_user is True:
                st.session_state["sign_in"] = "new"
                st.experimental_rerun()
            elif returning_user is True:
                st.session_state["sign_in"] = "return"
                st.experimental_rerun()

        if st.session_state["sign_in"] == "return":
            user = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if user != "":
                try:
                    login = st.button(f"Log in to {config[user]['name']}")
                    if password == config[user]["password"] and login is True:
                        st.session_state['logged_in'] = True
                        st.session_state["user"] = config[user]["name"]
                        st.session_state["penguin"] = config[user]['penguin']
                        st.session_state['tdl'] = config[user]["tdl"].split("`")
                        st.session_state['tdfl'] = config[user]["tdfl"].split("`")
                        st.session_state['cmpl'] = config[user]["cmpl"].split("`")
                        st.session_state['ltcmpl'] = config[user]["ltcmpl"].split("`")
                        st.session_state['num_complete'] = int(config[user]["num_complete"])
                        st.session_state["times_to_complete"] = config[user]["times_to_complete"].split("`")

                        with open('user_data.stodo', 'w') as configfile:
                            config.write(configfile)

                        st.experimental_rerun()
                    elif password != config[user]["password"] and password != "" and login is True:
                        st.error("Username and password do not match")
                        time.sleep(3)
                except KeyError:
                    st.error("Looks like that username does not exist. Do you have an account? Check if you've spelled it wrong.")
                    if st.button("Go back") is True:
                        st.session_state["sign_in"] = ""
                        st.experimental_rerun()

        elif st.session_state["sign_in"] == "new":
            user = st.text_input("Make a username for your new account")

            if user != "" and user not in config:
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
                st.session_state["times_to_complete"] = []
                password = st.text_input(f"Set a password for {user}", type="password")
                st.write("do NOT use a password you care about. I beg of you, I do not want access to your passwords. DO NOT GIVE THEM TO ME.")
                set_password = st.button("Save new password")

                if set_password is True and password != "":
                    config[user]["password"] = password

                    with open('user_data.stodo', 'w') as configfile:
                        config.write(configfile)
                        st.session_state['logged_in'] = True

                    st.experimental_rerun()
            elif user in config:
                st.error("Looks like that username is taken! Press the sign in button to log in or choose a different username.")
                retry_new_account = st.button(f"Alright! I'll try to sign in to {user} or make a new account that isn't called {user}.")
                if retry_new_account:
                    st.session_state["sign_in"] = ""
                    st.experimental_rerun()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
