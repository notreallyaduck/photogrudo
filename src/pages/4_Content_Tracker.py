import configparser
import time

import streamlit as st


def instructions():
    with st.expander("Instructions"):
        st.subheader("Content planner? Huh?")
        st.write("Congrats! You've made it this far")
        st.write('Now, you may be thinking something along the lines of "How on earth am I supposed to use this in a '
                 'way that benefits me without feeling like I am constantly being judged by this vast array of '
                 'condescending 🤨 emojis?"')
        st.write("Well, you're definitely reading the right thing")
        st.subheader("Using the planner")
        st.write('Add any additional subjects you might have using the "Add to the planner" section above')
        st.write("After that, add topics that are part of each subject (textbook chapter titles are a great place to "
                 "start)")
        st.write("As you progress through the year, ask yourself questions about how comfortable you are with each "
                 "topic")
        st.write("Adjust the stars accordingly, just remember to be honest with yourself")
        st.write("Aim for the stars, land among the sunglasses 😎")


def add_to_planner(subject_list):
    # interfaces to add to the content planner through text input fields in st.expanders

    with st.expander("Add to the planner"):
        what_to_add = st.selectbox("Add to the content planner", options=("Add subject", "Add topic"))

        if what_to_add == "Add subject":
            new_subject = st.text_input("Subject Name").split(",")
            add_subject = st.button("Add")
            st.info("Type the subject you want to add, separate them with commas to add multiple.")

            if add_subject is True:
                # look for each new item in the existing list to remove duplicates
                for j in new_subject:
                    if j.strip() in subject_list:
                        st.error(f"{j.strip()} is already in the content planner")
                        time.sleep(1)
                    else:
                        st.session_state["content_planner"].append(j.strip())
                st.experimental_rerun()

        elif what_to_add == "Add topic":
            # Similar to add subject but for topics, subject strings are modified and resaved to sessionstate
            subjects = []

            for i in st.session_state["content_planner"]:
                topics = i.split("*")
                subjects.append(topics[0])

            subject_to_add_topic = st.selectbox("Subject", options=subjects)
            new_topic = st.text_input("Topic to add").split(",")
            add_topic = st.button("Add")

            if add_topic is True and new_topic[0] != "":
                index_to_modify = 0
                for i in st.session_state["content_planner"]:
                    if i.startswith(subject_to_add_topic):
                        index_to_modify = st.session_state["content_planner"].index(i)

                added_topics = []
                did_not_add = ""

                for i in st.session_state["content_planner"][index_to_modify].split("*"):
                    added_topics.append(i.split("^")[0].strip())

                for i in new_topic:
                    if i != "" and i.strip() not in added_topics:
                        added_topics.append(i.strip())
                        st.session_state["content_planner"][index_to_modify] += "*" + i.strip() + "^" + "🤨"
                    elif i.strip() in added_topics:
                        did_not_add += i.strip() + " "

                if len(did_not_add) > 0:
                    st.warning(f"Did not add {did_not_add}")
                    time.sleep(2)
                st.experimental_rerun()

            elif new_topic[0] == "":
                # if no text input, display a help message
                st.info("Type the topics you want to add, separate them with commas to add multiple.")


def remove_from_planner(subjects, subject_list):
    # delete from planner by removing the indext of selected subject/modifying and saving the modified subject string
    with st.expander("Remove items from the planner"):
        selected_subject = st.selectbox("Subject to edit", options=subject_list)
        topic_list = ["Delete subject"]
        index_to_modify = 0

        for i in subjects:
            if i.startswith(selected_subject):
                index_to_modify = subjects.index(i)
                topics = i.split("*")
                topics.remove(selected_subject)

                for j in topics:
                    topic_name = j.split("^")
                    topic_list.append(f"{topic_name[0]}")

        item_to_remove = st.selectbox("What do you want to delete?", options=topic_list)
        confirm = st.button("🗑️ Delete")

        # proceed with deletion if confirm button is pressed
        if item_to_remove == "Delete subject" and confirm is True:
            del st.session_state["content_planner"][index_to_modify]
            st.experimental_rerun()

        elif confirm is True:
            for i in topics:
                if i.startswith(item_to_remove):
                    topic_to_remove = topics.index(i)
                    del topics[topic_to_remove]
            updated_subject = selected_subject

            for i in topics:
                updated_subject += "*" + i

            subjects[index_to_modify] = updated_subject  # store updated string in session state

            st.experimental_rerun()


def main():
    # initialise session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "total" not in st.session_state:
        st.session_state["total"] = 0

    if st.session_state["logged_in"] is True:
        ss_init()
        st.set_page_config(
            page_title="Photogrudo · Content Tracker",
            layout="centered",
            initial_sidebar_state="auto",
        )

        st.title("The photogrudo content tracker")
        st.write("Use this page to track progression through all your courses")
        total = 0

        if len(st.session_state["content_planner"]) > 0:
            subjects = st.session_state["content_planner"]
            subject_list = []

            for i in subjects:
                topics = i.split("*")
                subject_average = 0
                subject = topics[0]
                subject_list.append(subject)
                topic_num = 0

                index_to_modify = st.session_state["content_planner"].index(i)
                st.session_state["content_planner"][index_to_modify] = ""
                strings = i.split("*")

                st.header(subject)
                topics.remove(topics[0])

                expander_name = ""

                if len(topics) == 0:
                    st.write(f"Get started with {subject} by adding some topics!")
                elif len(topics) == 1:
                    expander_name = str(len(topics)) + " Topic"
                else:
                    expander_name = str(len(topics)) + " Topics"

                with st.expander(expander_name):
                    for j in topics:
                        topic_data = j.split("^")
                        topic_num += 1

                        # convert numbers in topic strings to emojis
                        if topic_data[1] == "0":
                            saved_value = "🤨"
                        elif topic_data[1] == "1":
                            saved_value = "⭐"
                        elif topic_data[1] == "2":
                            saved_value = "⭐⭐"
                        elif topic_data[1] == "3":
                            saved_value = "⭐⭐⭐"
                        elif topic_data[1] == "4":
                            saved_value = "⭐⭐⭐⭐"
                        elif topic_data[1] == "5":
                            saved_value = "⭐⭐⭐⭐⭐"
                        elif topic_data[1] == "6":
                            saved_value = "😎"
                        else:
                            saved_value = "🤨"

                        confidence = st.select_slider(topic_data[0],  options=["🤨", '⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', "😎"], value=saved_value, key=f"{subject}_{topic_num}")

                        # convert emojis to numbers to be saved in string
                        if confidence == "🤨":
                            subject_average += 0
                            total += 0
                            confidence_to_save = "0"
                        elif confidence == "⭐":
                            subject_average += 1
                            total += 1
                            confidence_to_save = "1"
                        elif confidence == "⭐⭐":
                            subject_average += 2
                            total += 2
                            confidence_to_save = "2"
                        elif confidence == "⭐⭐⭐":
                            subject_average += 3
                            total += 3
                            confidence_to_save = "3"
                        elif confidence == "⭐⭐⭐⭐":
                            subject_average += 4
                            total += 4
                            confidence_to_save = "4"
                        elif confidence == "⭐⭐⭐⭐⭐":
                            subject_average += 5
                            total += 5
                            confidence_to_save = "5"
                        elif confidence == "😎":
                            subject_average += 6
                            total += 6
                            confidence_to_save = "6"

                        for m in strings:
                            if m.startswith(topic_data[0]):
                                string_to_replace = strings.index(m)
                                strings.remove(m)
                                strings.insert(string_to_replace, f"{topic_data[0]}^{confidence_to_save}")

                    for m in strings:
                        if st.session_state["content_planner"][index_to_modify] == "":
                            st.session_state["content_planner"][index_to_modify] = subject
                        else:
                            st.session_state["content_planner"][index_to_modify] = st.session_state["content_planner"][index_to_modify] + "*" + m

                    if topic_num > 0:
                        subject_average = subject_average/topic_num

                        # Display progress bar and completion messages
                        st.progress(int(subject_average/6*100))

                        if subject_average == 6:
                            st.write(f"Congratulations {st.session_state['user']}, you're at 100 percent understanding of this subject")
                        elif subject_average > 3:
                            st.write(f"Congratulations {st.session_state['user']}, you're more than halfway there")
                        elif subject_average == 0:
                            st.write(f"Make a start on this subject {st.session_state['user']}")
                        else:
                            st.write(f"You've still got a ways to go, but you got this {st.session_state['user']}!")

            st.write("")

            add_to_planner(subject_list)

            remove_from_planner(subjects, subject_list)

            instructions()

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

            # display first time use instructions
            with st.expander("Instructions"):
                st.subheader("The Planner")
                st.write(
                    "Have you ever thought back on something you've learnt with absolutely no understanding of how you're progressing through it?")
                st.write("That's where the content planner comes in")
                st.subheader("Step One")
                st.write("Type your subjects or broad content areas in the field above this section")
                st.write("Enter them separated with commas to add them all at once. Input one item to add one subject.")

        if total != st.session_state["total"]:
            st.session_state["total"] = total
            st.experimental_rerun()

        update_config()

    else:
        st.error("Log in please")


def update_config():
    # Update config file by saving all relevant sessionstate data to user_data.photogrudo

    config = configparser.ConfigParser()
    config.sections()
    config.read('user_data.photogrudo')

    user = st.session_state["user"]

    content_to_update = ""

    for i in st.session_state["content_planner"]:
        if i != "":
            content_to_update += str(i) + "`"

    config[user]["content_planner"] = content_to_update

    with open('user_data.photogrudo', 'w') as configfile:
        config.write(configfile)


def ss_init():
    for i in st.session_state["content_planner"]:
        if i == "":
            st.session_state["content_planner"].remove(i)


if __name__ == '__main__':
    main()
