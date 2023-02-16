import datetime

import streamlit as st
import configparser
import time


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] is True:
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

        st.set_page_config(
            page_title="Photogrudo · Overview",
            layout="centered",
            initial_sidebar_state="auto",
        )

        complete = []
        complete_ids = []

        if st.session_state["sign_in"] == "return":
            st.title(f'Welcome back, {st.session_state["user"]}!')
        elif st.session_state["sign_in"] == "new":
            st.title(f'Welcome to Photogrudo, {st.session_state["user"]}!')

        for i in st.session_state['tdl']:
            j = i.split(" · ")
            if j[2] != "No due date":
                h = j[2].split("-")

                date_time = datetime.datetime(int(h[0]), int(h[1]), int(h[2]))
                if 0 < time.mktime(date_time.timetuple()) - time.time() < 86400:
                    st.write(f"[{j[0]}] is due soon · {h[2]}/{h[1]}/{h[0]}")

        for i in st.session_state['tdfl']:
            j = i.split(" · ")
            h = j[2].split("-")

            try:
                date_time = datetime.datetime(int(h[0]), int(h[1]), int(h[2]))
                if 0 < time.mktime(date_time.timetuple()) - time.time() < 86400:
                    st.write(f"{j[0]} is due soon · {h[2]}/{h[1]}/{h[0]} · Get to it")
            except IndexError:
                pass

        col1, col2, col3 = st.columns(3)

        with col3:
            st.header("Done")
            st.write("Completed tasks")

        with col1:
            st.header("Do now")
            st.write("Priority Tasks")

            for i in st.session_state['tdl']:
                j = i.split(" · ")
                st.checkbox(j[0], key=i)
                if st.session_state[i] is True:
                    complete.append(j[0])
                    complete_ids.append(i)
                    st.session_state["times_to_complete"].append(round(time.time()) - int(float(j[1])))

        with col2:
            st.header("Do soon")
            st.write("Do at some point")

            for i in st.session_state['tdfl']:
                j = i.split(" · ")
                st.checkbox(j[0], key=i)
                if st.session_state[i] is True:
                    complete.append(j[0])
                    complete_ids.append(i)
                    st.session_state["times_to_complete"].append(round(time.time()) - int(float(j[1])))

        completed_tasks(complete_ids)

        with col3:
            for i in st.session_state["cmpl"]:
                j = i.split(" · ")

                task_type = ""

                if j[3] == "tdl":
                    task_type = "Priority"
                elif j[3] == "tdfl":
                    task_type = "At some point"

                col3.write(f"{j[0]}: {task_type}")

            if len(st.session_state["cmpl"]) > 0:
                delete_tasks = st.button("Delete completed tasks")
                if delete_tasks is True:
                    del st.session_state["cmpl"]
                    st.experimental_rerun()

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
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])
    config[user]["times_to_complete"] = times_to_update

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)


def completed_tasks(keys):
    removed_something = False

    for i in keys:
        # add to complete and long term complete list in session_state
        st.session_state["cmpl"].append(i)
        st.session_state["ltcmpl"].append(i)
        st.session_state['num_complete'] += 1

        # remove keys of completed tasks from respective lists in session_state
        if i in st.session_state["tdl"]:
            st.session_state["tdl"].remove(i)
            removed_something = True
        if i in st.session_state["tdfl"]:
            st.session_state["tdfl"].remove(i)
            removed_something = True

        if i in st.session_state:
            del st.session_state[i]
            removed_something = True

    # rerun streamlit to update lists in overview
    if removed_something is True:
        st.experimental_rerun()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
