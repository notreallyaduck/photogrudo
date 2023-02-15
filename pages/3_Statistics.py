import datetime
import time

import streamlit as st
import configparser


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state['logged_in'] is True:
        st.set_page_config(
            page_title="Photogrudo · Statistics · THIS PAGE IS A WORK IN PROGRESS",
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

        if st.session_state['num_complete'] == 0:
            st.title("YOU HAVE ACCOMPLISHED ABSOLUTELY NOTHING")
        elif st.session_state['num_complete'] == 1:
            st.title("YOU HAVE COMPLETED 1 (ONE) TASK")
        elif st.session_state['num_complete'] > 1:
            st.title(f"YOU HAVE COMPLETED {str(st.session_state['num_complete'])} TASKS")
            st.write("what you want a pat on the back?")

        if st.session_state['num_complete'] >= 10:
            st.header("Stats")
            st.write("Average time taken to complete tasks")

            average_time_to_complete = 0

            for i in st.session_state["times_to_complete"]:
                if i != "":  # TODO properly fix this
                    average_time_to_complete += int(i)

            average_time_to_complete = average_time_to_complete/st.session_state["num_complete"]

            if average_time_to_complete < 60:
                average_time_to_complete = f"{round(average_time_to_complete)} seconds"
            elif 60 < average_time_to_complete < 3600:
                average_time_to_complete = f"{round(average_time_to_complete/60)} minutes"
            elif 3600 < average_time_to_complete < 86400:
                average_time_to_complete = f"{round(average_time_to_complete / 3600)} hours"
            elif 86400 < average_time_to_complete < 604800:
                average_time_to_complete = f"{round(average_time_to_complete / 86400)} days"
            elif 604800 < average_time_to_complete < 2629746:
                average_time_to_complete = f"{round(average_time_to_complete / 604800)} weeks"
            elif 2629746 < average_time_to_complete < 31536000:
                average_time_to_complete = f"{round(average_time_to_complete / 2629746)} months"
            elif average_time_to_complete >= 31536000:
                average_time_to_complete = f"{round(average_time_to_complete / 31536000)} years"

            st.write(average_time_to_complete) # Average time taken to complete tasks

            st.header("Number of tasks today")
            st.write("0.000003 (THIS WILL BE IMPLEMENTED SOON)")  # TODO NUM TASKS TODAY, compared to yesterday, compared to today last week
            st.header("Number of tasks completed per day")
            st.write("-92 (THIS WILL BE IMPLEMENTED SOON)")  # TODO NUM TASKS DAILY AVERAGE, compared to last week, compared to last month
            st.write(" ")

            with st.expander("All completed tasks"):

                for i in st.session_state["ltcmpl"]:
                    j = i.split(" · ")
                    date_due = j[2].split("-")

                    date_time = datetime.datetime(int(date_due[0]), int(date_due[1]), int(date_due[2]))

                    when_due = (time.time() - time.mktime(date_time.timetuple()))/86400

                    if when_due < 0:
                        st.write(f"{date_due[2]}/{date_due[1]}/{date_due[0]} · {j[0]} was due {abs(round(when_due))} days in the future")
                    elif when_due <= 1:
                        st.write(f"{date_due[2]}/{date_due[1]}/{date_due[0]} · {j[0]} was due yesterday")
                    elif when_due > 1:
                        st.write(f"{date_due[2]}/{date_due[1]}/{date_due[0]} · {j[0]} was due {round(when_due)} days ago")

        else:
            st.write("Stats will appear here after you've completed a couple tasks. Keep at it.")

            current_penguin = st.session_state['penguin']

            penguin_caption = ""

            if current_penguin == "Assets/motivation_penguin.gif":
                penguin_caption = "You got this"
            elif current_penguin == "Assets/pessimistic_penguin.gif":
                penguin_caption = "You don't got this"

            st.image(current_penguin, caption=penguin_caption, use_column_width="always")

            index = 0

            if st.session_state['penguin'] == "Assets/motivation_penguin.gif":
                index = 0
            elif st.session_state['penguin'] == "Assets/pessimistic_penguin.gif":
                index = 1

            penguin = st.radio("Switch to a different penguin!", options=["Motivational Penguin", "Pessimistic Penguin"], index=index)

            if penguin == "Motivational Penguin":
                st.session_state["penguin"] = "Assets/motivation_penguin.gif"
            elif penguin == "Pessimistic Penguin":
                st.session_state["penguin"] = "Assets/pessimistic_penguin.gif"

            if current_penguin != st.session_state['penguin']:
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
    # config.set(user, 'tdl', str(st.session_state["tdl"]))
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])
    config[user]["times_to_complete"] = times_to_update

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)



if __name__ == '__main__':
    main()
