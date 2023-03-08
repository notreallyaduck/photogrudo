import streamlit as st
import time
import configparser


def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state['logged_in'] is True:
        ss_init()

        st.set_page_config(
            page_title="Photogrudo · Add Task",
            layout="centered",
            initial_sidebar_state="auto",
        )

        st.title("Add a task")

        add_type = ""

        st.write(f"You currently have {len(st.session_state['tdl'])} priority and {len(st.session_state['tdfl'])} do soon tasks")
        new_task = st.text_input("📝 Enter Task", key="nte", value="").strip()

        st.write("What type of task is this?")

        add_priority = st.checkbox("❗️❗️Do now")
        add_some_point = st.checkbox("❗️ Do soon")

        if add_priority is True and add_some_point is False:
            add_type = "do now"
        elif add_some_point is True and add_priority is False:
            add_type = "do soon"
        elif add_priority is False and add_some_point is False:
            add_type = ""
        elif add_some_point is True and add_priority is True:
            add_type = "both selected"

        st.write("")

        due = st.radio("📅 Is this task due?", options=("Task is due", "Task is not due"))
        due_date = "No due date"

        if due == "Task is due":
            due_date = st.date_input("Date due")

        if new_task and add_type != "" and add_type != "both selected":
            add_button = st.button(f'✅ Add "{new_task}" to: {add_type} tasks')

            if add_button is True:
                add_task(new_task, add_type, due_date)
                st.success(f"Successfully added {new_task}.")
                time.sleep(1)
                st.experimental_rerun()

        elif add_type == "" and not new_task:
            st.info("Type the name of your task and select the type of task you want to add")

        elif not new_task:
            st.warning("Type your task")

        elif add_type == "":
            st.warning("What type of task is this?")

        elif add_type == "both selected":
            st.warning("Select one option")

        update_config()

    else:
        st.error("Log in please")


def add_task(task, task_type, due_date):
    if task != "":
        if task_type == "do now":
            task = st.session_state["nte"] + " · " + str(time.time()) + " · " + str(due_date) + " · " + "tdl"
            st.session_state['tdl'].append(task)

        elif task_type == "do soon":
            task = st.session_state["nte"] + " · " + str(time.time()) + " · " + str(due_date) + " · " + "tdfl"
            st.session_state['tdfl'].append(task)


def ss_init():
    for i in st.session_state["tdl"]:
        if i == "":
            st.session_state["tdl"].remove(i)

    for i in st.session_state["tdfl"]:
        if i == "":
            st.session_state["tdfl"].remove(i)


def update_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    user = st.session_state["user"]

    tdl_to_update = ""
    tdfl_to_update = ""

    for i in st.session_state['tdl']:
        if i != "":
            tdl_to_update += i + "`"

    for i in st.session_state['tdfl']:
        if i != "":
            tdfl_to_update += i + "`"

    config[user]["tdl"] = tdl_to_update
    config[user]["tdfl"] = tdfl_to_update

    with open('user_data.photogrudo', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    main()
