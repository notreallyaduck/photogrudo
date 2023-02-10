import streamlit as st
from datetime import datetime
import configparser


def main():
    if st.session_state['logged_in'] is True:
        config = configparser.ConfigParser()
        config.sections()
        config.read('user_data.stodo')

        st.set_page_config(
            page_title="this is not called stodo · Add Task",
            layout="centered",
            initial_sidebar_state="collapsed",
        )

        st.title("Add a task")
        new_task = st.text_input("Enter Task", key="nte")

        if new_task:
            add_type = st.radio("Type of task", options=["Priority", "At some point"])
            add_button = st.button(f'Add "{new_task}" to: {add_type} tasks')

            if add_button is True:
                add_task(add_type)

        else:
            st.warning("Type your task")

        st.text(f"Currently added priority tasks: {st.session_state['tdl']}")
        st.text(f"Currently added at some point tasks: {st.session_state['tdfl']}")
        update_config()

    else:
        st.error("Log in please")


def update_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.stodo')

    user = st.session_state["user"]

    tdl_to_update = ""
    tdfl_to_update = ""
    cmpl_to_update = ""
    ltcmpl_to_update = ""

    for i in st.session_state['tdl']:
        tdl_to_update += "`" + i

    for i in st.session_state['tdfl']:
        tdfl_to_update += "`" + i

    for i in st.session_state['cmpl']:
        cmpl_to_update += "`" + i

    for i in st.session_state['ltcmpl']:
        ltcmpl_to_update += "`" + i

    config[user]["name"] = st.session_state["user"]
    config[user]['penguin'] = st.session_state["penguin"]
    config[user]["tdl"] = tdl_to_update
    # config.set(user, 'tdl', str(st.session_state["tdl"]))
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)



def add_task(task_type):
    task = st.session_state["nte"] + " [" + str(datetime.now()) + "]"
    if task != "":
        if task_type == "Priority":
            st.session_state['tdl'].append(task)
        elif task_type == "At some point":
            st.session_state['tdfl'].append(task)


if __name__ == '__main__':
    main()
