import configparser
import time

import streamlit as st


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] is True:
        st.set_page_config(
            page_title="Photogrudo · Content Tracker",
            layout="centered",
            initial_sidebar_state="auto",
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

        for i in st.session_state["content_planner"]:
            if i == "":
                st.session_state["content_planner"].remove(i)

        if "cmpl" not in st.session_state:
            st.session_state['cmpl'] = []

        st.title("The photogrudo content tracker")
        st.write("Use this page to track progression through all your courses")

        if len(st.session_state["content_planner"]) > 0:
            subjects = st.session_state["content_planner"]

            for i in subjects:
                topics = i.split("*")
                subject_average = 0
                subject = topics[0]
                topic_num = 0

                index_to_modify = st.session_state["content_planner"].index(i)
                st.session_state["content_planner"][index_to_modify] = ""
                strings = i.split("*")

                st.header(subject)
                topics.remove(topics[0])

                with st.expander("Topics"):

                    for j in topics:
                        topic_data = j.split("^")
                        topic_num += 1

                        confidence = st.select_slider(topic_data[0],  options=["🤨", '⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'], value=topic_data[1], key=f"{subject}_{topic_num}")

                        if confidence == "🤨":
                            subject_average += 0
                        elif confidence == "⭐":
                            subject_average += 1
                        elif confidence == "⭐⭐":
                            subject_average += 2
                        elif confidence == "⭐⭐⭐":
                            subject_average += 3
                        elif confidence == "⭐⭐⭐⭐":
                            subject_average += 4
                        elif confidence == "⭐⭐⭐⭐⭐":
                            subject_average += 5

                        for m in strings:
                            if m.startswith(topic_data[0]):
                                string_to_replace = strings.index(m)
                                strings.remove(m)
                                strings.insert(string_to_replace, f"{topic_data[0]}^{confidence}")

                    for m in strings:
                        if st.session_state["content_planner"][index_to_modify] == "":
                            st.session_state["content_planner"][index_to_modify] = subject
                        else:
                            st.session_state["content_planner"][index_to_modify] = st.session_state["content_planner"][index_to_modify] + "*" + m


                    if topic_num > 0:
                        subject_average = subject_average/topic_num

                        if subject_average == 5:
                            st.write("Congratulations, you're at 100 percent understanding of this subject")
                        elif subject_average > 2.5:
                            st.write("Congratulations, you're more than halfway there")
                        elif subject_average == 0:
                            st.write("Make a start on this subject")
                        else:
                            st.write("You've still got a ways to go, but you got this!")

            st.write("")

            with st.expander("Add to the planner"):
                what_to_add = st.selectbox("Add to the content planner", options=("Add subject", "Add topic"))

                if what_to_add == "Add subject":
                    new_subject = st.text_input("Subject Name").strip()
                    add_subject = st.button("Add")

                    if add_subject is True:
                        for i in subjects:
                            if i.startswith(new_subject):
                                st.error("Subject already exists")
                                time.sleep(2)
                                st.experimental_rerun()

                        st.session_state["content_planner"].append(new_subject.strip())
                        st.experimental_rerun()

                elif what_to_add == "Add topic":
                    subjects = []

                    for i in st.session_state["content_planner"]:
                        topics = i.split("*")
                        subjects.append(topics[0])

                    subject_to_add_topic = st.selectbox("Subject", options=subjects)
                    new_topic = st.text_input("Topic to add").split(",")
                    add_topic = st.button("Add")

                    if add_topic is True and new_topic[0] is not "":
                        index_to_modify = 0
                        for i in st.session_state["content_planner"]:
                            if i.startswith(subject_to_add_topic):
                                index_to_modify = st.session_state["content_planner"].index(i)

                        added_topics = []

                        for i in st.session_state["content_planner"][index_to_modify].split("*"):
                            added_topics.append(i.split("^")[0].strip())

                        for i in new_topic:
                            if i != "" and i.strip() not in added_topics:
                                added_topics.append(i.strip())
                                st.session_state["content_planner"][index_to_modify] += "*" + i.strip() + "^" + "🤨"
                            elif i.strip() in added_topics:
                                st.error(f"Not adding {i}, it's already in this subject")
                                time.sleep(1.5)

                        st.experimental_rerun()
                    elif new_topic[0] is "":
                        st.info("Type the topics you want to add, separate them with commas to add multiple.")

        else:
            new_subject = st.text_input("Add a subject (separate subjects with commas to add several at once)")
            st.write()

            if new_subject != "":
                subjects_to_add = new_subject.split(",")
                add_subjects = st.button(f"Add to the content planner")

                if add_subjects is True:
                    for i in subjects_to_add:
                        st.session_state["content_planner"].append(i.strip())

                    st.experimental_rerun()

            else:
                st.info("Type the subjects you want to add")
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
    content_to_update = ""

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

    for i in st.session_state["content_planner"]:
        if i != "":
            content_to_update += i + "`"

    config[user]["name"] = st.session_state["user"]
    config[user]['penguin'] = st.session_state["penguin"]
    config[user]["tdl"] = tdl_to_update
    # config.set(user, 'tdl', str(st.session_state["tdl"]))
    config[user]["tdfl"] = tdfl_to_update
    config[user]["cmpl"] = cmpl_to_update
    config[user]["ltcmpl"] = ltcmpl_to_update
    config[user]["num_complete"] = str(st.session_state['num_complete'])
    config[user]["times_to_complete"] = times_to_update
    config[user]["content_planner"] = content_to_update

    with open('user_data.stodo', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    main()
