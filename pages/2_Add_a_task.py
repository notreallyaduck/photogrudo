import streamlit as st
import time
import configparser


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state['logged_in'] is True:
        st.set_page_config(
            page_title="Photogrudo · Add Task",
            layout="centered",
            initial_sidebar_state="expanded",
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

        st.title("Add a task")

        col1, col2 = st.columns(2)

        with col1:
            col1.write(f"You currently have {len(st.session_state['tdl'])} priority and {len(st.session_state['tdfl'])} do soon tasks")
            new_task = st.text_input("Enter Task", key="nte", value="").strip()

        with col2:
            # add_type = st.selectbox('What type of task is this?', ('Select a type', 'Priority', 'Do soon'), key="select_type")
            st.write("What type of task is this?")
            add_priority = st.checkbox("Priority")
            add_some_point = st.checkbox("Do soon")

            if add_priority is True and add_some_point is False:
                add_type = "Priority"
            elif add_some_point is True and add_priority is False:
                add_type = "do soon"
            elif add_priority is False and add_some_point is False:
                add_type = ""
            elif add_some_point is True and add_priority is True:
                add_type = "both selected"

            st.multiselect("Tags:", options=("hello there", "this is a tag"))

            if new_task and add_type != "" and add_type != "both selected":
                add_button = st.button(f'Add "{new_task}" to: {add_type} tasks')

                if add_button is True:
                    add_task(add_type)
                    col1.success(f"Successfully added {new_task}.")
                    time.sleep(1)
                    st.experimental_rerun()

            elif add_type == "" and not new_task:
                col1.info("Type the name of your task and select the type of task you want to add")

            elif not new_task:
                col1.warning("Type your task")

            elif add_type == "":
                col1.warning("What type of task is this?")

            elif add_type == "both selected":
                col1.warning("Select one option")

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
    times_to_update = ""

    for i in st.session_state['tdl']:
        if i != "":
            tdl_to_update += i + "`"

    for i in st.session_state['tdfl']:
        if i != "":
            tdfl_to_update += i + "`"

    for i in st.session_state['cmpl']:
        if i != "":
            cmpl_to_update += i + "`"

    for i in st.session_state['ltcmpl']:
        if i != "":
            ltcmpl_to_update += i + "`"

    for i in st.session_state["times_to_complete"]:
        if i != "":
            times_to_update += str(i) + "`"

    config[user]["name"] = st.session_state["user"]
    config[user]['penguin'] = st.session_state["penguin"]
    config[user]["tdl"] = tdl_to_update
    # config.set(user, 'tdl', str(st.session_state["tdl"]))
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])
    config[user]["times_to_complete"] = times_to_update

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)


def add_task(task_type):
    task = st.session_state["nte"] + " · " + str(time.time())
    if task != "":
        if task_type == "Priority":
            st.session_state['tdl'].append(task)
        elif task_type == "do soon":
            st.session_state['tdfl'].append(task)


if __name__ == '__main__':
    main()
