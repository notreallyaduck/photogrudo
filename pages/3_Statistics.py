import streamlit as st
import configparser


def main():
    if st.session_state['logged_in'] is True:
        st.set_page_config(
            page_title="this is not called stodo · Statistics",
            layout="centered",
            initial_sidebar_state="collapsed",
        )

        if st.session_state['num_complete'] == 0:
            st.title("YOU HAVE ACCOMPLISHED ABSOLUTELY NOTHING")
        elif st.session_state['num_complete'] == 1:
            st.title("YOU HAVE COMPLETED 1 (ONE) TASK")
        elif st.session_state['num_complete'] > 1:
            st.title(f"YOU HAVE COMPLETED {str(st.session_state['num_complete'])} TASKS")
            st.text("what you want a pat on the back?")

        if st.session_state['num_complete'] > 10:
            st.header("Stats")
            st.text("Average time taken to complete tasks")
            st.text("16000000934 days (make this)")  # TODO AVERAGE TIME TAKEN TO COMPLETE, rolling average, weekly average, monthly average
            st.header("Number of tasks today")
            st.text("0.000003")  # TODO NUM TASKS TODAY, compared to yesterday, compared to today last week
            st.header("Number of tasks completed per day")
            st.text("-92")  # TODO NUM TASKS DAILY AVERAGE, compared to last week, compared to last month

            st.header("All completed tasks")

            for i in st.session_state["ltcmpl"]:
                st.text(i)

        else:
            st.text("Stats will appear here after you've completed a couple tasks. Keep at it.")

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



if __name__ == '__main__':
    main()
