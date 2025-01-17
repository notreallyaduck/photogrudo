import time

import streamlit as st
import configparser


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state['logged_in'] is True:
        ss_init()
        st.set_page_config(
            page_title="Photogrudo · Statistics",
            layout="centered",
            initial_sidebar_state="auto",
        )

        # Display title message depending on the number of tasks completed
        if st.session_state['num_complete'] == 0:
            st.title("YOU HAVE ACCOMPLISHED ABSOLUTELY NOTHING")
        elif st.session_state['num_complete'] == 1:
            st.title("YOU HAVE COMPLETED 1 (ONE) TASK")
        elif st.session_state['num_complete'] > 1:
            st.title(f"YOU HAVE COMPLETED {str(st.session_state['num_complete'])} TASKS")
            st.write("what you want a pat on the back?")

        if st.session_state['num_complete'] >= 10:
            st.header("⏱️ Average time taken to complete tasks")

            # Calculate average time for completion and display
            average_time_to_complete = 0

            for i in st.session_state["times_to_complete"]:
                if i != "":
                    average_time_to_complete += int(i)

            st.write("On average, you take " + average(average_time_to_complete) + " to complete a task")  # Average
            # time taken to complete tasks
            st.write("")

            st.header("👍👎 Overdue/On time task ratio")

            # If there is at least one task completed on time, calculate ratio of overdue to due tasks, else show a
            # different message
            if st.session_state["num_complete"] != st.session_state["was_overdue"]:
                od_ot_ratio = round(st.session_state["was_overdue"]/(st.session_state["num_complete"] - st.session_state["was_overdue"]), 2)
                od_percent = round(st.session_state["was_overdue"]/(st.session_state["num_complete"])*100)
                st.write(f"On average, you complete {od_ot_ratio} tasks after the due date per task completed on time.")
                st.write(f"{od_percent}% of tasks are overdue on completion")
                st.write(' ')

            else:
                st.write(":red[You have only ever completed tasks after the due date. What is wrong with you.]")

            # display a list of completed tasks with due dates and age of task
            with st.expander("All completed tasks"):

                for i in st.session_state["ltcmpl"]:
                    j = i.split(" · ")

                    when_made = round((time.time() - int(float(j[1]))) / 86400)

                    if j[2] != "No due date":
                        date_due = j[2].split("-")

                        if when_made <= 1:
                            st.write(f"{j[0]} · Was due {date_due[2]}/{date_due[1]}/{date_due[0]} · Created recently")
                        elif when_made > 1:
                            st.write(f"{j[0]} · Was due {date_due[2]}/{date_due[1]}/{date_due[0]} · Created {when_made} days ago")
                    else:
                        if when_made <= 1:
                            st.write(f"{j[0]} · No due date · Created recently")
                        elif when_made > 1:
                            st.write(f"{j[0]} · No due date · Created {when_made} days ago")

        else:
            st.write("Stats will appear here after you've completed a couple tasks. Keep at it.")

        # Display penguin based on saved user preferences, defaults to motivational penguin because we could all use
        # some motivation in life
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
        st.write("This will reflect in the incredibly motivational quotes on the overview page.")

        if penguin == "Motivational Penguin":
            st.session_state["penguin"] = "Assets/motivation_penguin.gif"
        elif penguin == "Pessimistic Penguin":
            st.session_state["penguin"] = "Assets/pessimistic_penguin.gif"

        if current_penguin != st.session_state['penguin']:
            st.experimental_rerun()
        update_config()
    else:
        st.error("Log in please")


def average(average_time_to_complete):
    # calculate and return average time to complete tasks 
    average_time_to_complete = average_time_to_complete / st.session_state["num_complete"]
    if average_time_to_complete < 60:
        average_time_to_complete = f"{round(average_time_to_complete)} second(s)"
    elif 60 < average_time_to_complete < 3600:
        average_time_to_complete = f"{round(average_time_to_complete / 60)} minute(s)"
    elif 3600 < average_time_to_complete < 86400:
        average_time_to_complete = f"{round(average_time_to_complete / 3600)} hour(s)"
    elif 86400 < average_time_to_complete < 604800:
        average_time_to_complete = f"{round(average_time_to_complete / 86400)} day(s)"
    elif 604800 < average_time_to_complete < 2629746:
        average_time_to_complete = f"{round(average_time_to_complete / 604800)} week(s)"
    elif 2629746 < average_time_to_complete < 31536000:
        average_time_to_complete = f"{round(average_time_to_complete / 2629746)} month(s)"
    elif average_time_to_complete >= 31536000:
        average_time_to_complete = f"{round(average_time_to_complete / 31536000)} year(s)"

    return average_time_to_complete


def update_config():
    # Update config file by saving all relevant sessionstate data to user_data.photogrudo

    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    user = st.session_state["user"]
    ltcmpl_to_update = ""

    for i in st.session_state['ltcmpl']:
        if i != "":
            ltcmpl_to_update += i + "`"

    config[user]['penguin'] = st.session_state["penguin"]
    config[user]["ltcmpl"] = ltcmpl_to_update

    with open('user_data.photogrudo', 'w') as configfile:
        config.write(configfile)


def ss_init():
    for i in st.session_state["ltcmpl"]:
        if i == "":
            st.session_state["ltcmpl"].remove(i)


if __name__ == '__main__':
    main()
