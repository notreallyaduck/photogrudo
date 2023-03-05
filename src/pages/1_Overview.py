import datetime
import random

import streamlit as st
import configparser
import time


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] is True:
        ss_init()

        st.set_page_config(
            page_title="Photogrudo · Overview",
            layout="centered",
            initial_sidebar_state="auto",
        )
        # Streamlit page setup

        complete = []
        complete_ids = []

        if st.session_state["sign_in"] == "return":
            st.title(f'Welcome back, {st.session_state["user"]}!')
        elif st.session_state["sign_in"] == "new":
            st.title(f'👋 Welcome to Photogrudo, {st.session_state["user"]}!')

        insert_corny_quote()
        st.write(" ")

        for i in st.session_state['tdl']:
            j = i.split(" · ")
            if j[2] != "No due date":
                h = j[2].split("-")

                date_time = datetime.datetime(int(h[0]), int(h[1]), int(h[2]))
                if 0 < time.mktime(date_time.timetuple()) + 86400 - time.time() < 86400:
                    due_message = "Due soon · " + j[0] + " · " + h[2] + "/" + h[1] + "/" + h[0]
                    st.markdown(f":blue[{due_message}]")

        for i in st.session_state['tdfl']:
            j = i.split(" · ")

            if j[2] != "No due date":
                h = j[2].split("-")
                date_time = datetime.datetime(int(h[0]), int(h[1]), int(h[2]))
                if 0 < time.mktime(date_time.timetuple()) - time.time() < 86400:
                    st.write(f"Due soon · {j[0]} · {h[2]}/{h[1]}/{h[0]}")

        checkbox_function = st.radio("Checkboxes should:", options=("✅ Mark tasks as complete", "🗑️ Delete tasks"))
        checkbox_deletes = True

        if checkbox_function == "✅ Mark tasks as complete":
            checkbox_deletes = False
        elif checkbox_function == "🗑️ Delete tasks":
            checkbox_deletes = True

        col1, col2, col3 = st.columns(3)

        with col3:
            st.header("Done")
            st.write("Completed tasks")

        with col1:
            st.header("Do now")
            st.write("Priority Tasks")

            for i in st.session_state['tdl']:
                create_checkbox(i, complete, complete_ids)

        with col2:
            st.header("Do soon")
            st.write("Do at some point")

            for i in st.session_state['tdfl']:
                create_checkbox(i, complete, complete_ids)

        completed_tasks(complete_ids, checkbox_deletes)

        with col3:
            for i in st.session_state["cmpl"]:
                j = i.split(" · ")

                task_type = ""

                if j[3] == "tdl":
                    task_type = "Do now"
                elif j[3] == "tdfl":
                    task_type = "Do soon"

                col3.write(f"{j[0]}: {task_type}")

            if len(st.session_state["cmpl"]) > 0:
                delete_tasks = st.button("🗑️ Delete completed tasks")
                if delete_tasks is True:
                    del st.session_state["cmpl"]
                    st.experimental_rerun()

        update_config()

    else:
        st.error("Log in please")


def completed_tasks(keys, delete):
    removed_something = False

    for i in keys:

        if delete is False:
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


def update_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

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
    config[user]["was_overdue"] = str(st.session_state['was_overdue'])
    config[user]["times_to_complete"] = times_to_update

    with open('user_data.photogrudo', 'w') as configfile:
        config.write(configfile)


def insert_corny_quote():
    chosen_quote = random.randrange(10)
    quote_to_display = ""

    if st.session_state["penguin"] == "Assets/motivation_penguin.gif":
        if chosen_quote == 0:
            quote_to_display = "Age is of no importance unless you're a cheese"
        elif chosen_quote == 1:
            quote_to_display = "Life always gives you a second chance, its called tomorrow"
        elif chosen_quote == 2:
            quote_to_display = "When nothing goes right, go left"
        elif chosen_quote == 3:
            quote_to_display = "The road to success is always under construction"
        elif chosen_quote == 4:
            quote_to_display = "Go easy on yourself. Whatever you do today, let it be enough"
        elif chosen_quote == 5:
            quote_to_display = "Believe you can and you're halfway there"
        elif chosen_quote == 6:
            quote_to_display = "I believe in you"
        elif chosen_quote == 7:
            quote_to_display = "I know this sounds like a cat poster"
        elif chosen_quote == 8:
            quote_to_display = "Be like a postage stamp, stick to a thing until you get there"
        elif chosen_quote == 9:
            quote_to_display = "When life gives you lemons, order the lobster tail"

    else:
        if chosen_quote == 0:
            quote_to_display = "It only gets worse"
        elif chosen_quote == 1:
            quote_to_display = "You are doing a terrible job"
        elif chosen_quote == 2:
            quote_to_display = "You haven't done enough"
        elif chosen_quote == 3:
            quote_to_display = "There are no words to describe your utter lack of productivity"
        elif chosen_quote == 4:
            quote_to_display = "Trying is the first step toward failure"
        elif chosen_quote == 5:
            quote_to_display = "Keep trying until you give up"
        elif chosen_quote == 6:
            quote_to_display = "Keep trying. eventually you will try"
        elif chosen_quote == 7:
            quote_to_display = "Only dead fish go with the flow"
        elif chosen_quote == 8:
            quote_to_display = "Enjoy the good times because something terrible is going to happen"
        elif chosen_quote == 9:
            quote_to_display = "You'll accomplish nothing today"

    st.subheader('"' + quote_to_display + '"')


def ss_init():
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

    for i in st.session_state["content_planner"]:
        if i == "":
            st.session_state["content_planner"].remove(i)

    if "cmpl" not in st.session_state:
        st.session_state['cmpl'] = []


def create_checkbox(task, complete, complete_ids):
    j = task.split(" · ")
    h = j[2].split("-")
    overdue = False

    if j[2] != "No due date":
        date_time = datetime.datetime(int(h[0]), int(h[1]), int(h[2]))
        if time.mktime(date_time.timetuple()) - time.time() + 86400 < 0:
            overdue = True

    if len(h) == 3:
        st.checkbox(f"{j[0]} · Due {h[2]}/{h[1]}/{h[0]}", key=task)
        if overdue:
            st.write(":red[This task is overdue ^]")
    else:
        st.checkbox(f"{j[0]} · No due date", key=task)

    if st.session_state[task] is True:
        if overdue:
            st.session_state["was_overdue"] += 1

        complete.append(j[0])
        complete_ids.append(task)
        st.session_state["times_to_complete"].append(round(time.time()) - int(float(j[1])))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
