from transformers import pipeline
import streamlit as st
from homework_db import *
import pandas as pd
import random


@st.cache(allow_output_mutation=True)
def load_model(model_name):
    nlp = pipeline('sentiment-analysis', model=model_name)
    return nlp


def load_fb_data():
    table = read_fb_data()
    df = pd.DataFrame(table, columns=['Sentence', 'Sentiment', 'Feedbacks', 'Timestamp'])
    return df


def load_data():
    table = read_data()
    df = pd.DataFrame(table, columns=['Sentence', 'Sentiment', 'Timestamp'])
    return df


def result(a, b):
    add_feedback_data(a, b + 1)
    st.success("Added to feedback database")


def main():
    st.title("Streamlit Exercise ")
    menu = ['Insert', 'Read', 'Update', 'Feedbacks']
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()
    create_table_withfb()

    if choice == 'Insert':                                      # To insert data into the database
        st.subheader('Lets check Sentiment')
        line = st.text_area("Enter the sentence")
        st.text("Sentiment")
        nlp = load_model("distilbert-base-uncased-finetuned-sst-2-english")

        if st.button("Add Task"):
            rslt = nlp(line)
            res = (rslt[0]['label'])

            if line is not None:
                st.write(res)
            a = add_data(line, res)
            add_feedbacks(a)
            st.success("Successfully added data in database 👍 ")
    elif choice == 'Read':                                      # To read from database and show sentence,sentiment with timestamp
        st.subheader('Datatable')
        if "page" not in st.session_state:
            st.session_state.page = 0

        def next_page():
            st.session_state.page += 1

        def prev_page():
            st.session_state.page -= 1

        col1, col2, col3, _ = st.columns([0.1, 0.17, 0.1, 0.63])
        total_pages = len(load_data()) // 10 + 1
        if st.session_state.page < (total_pages - 1):
            col3.button(">", on_click=next_page)
        else:
            col3.write("")

        if st.session_state.page > 0:
            col1.button("<", on_click=prev_page)
        else:
            col1.write("")

        col2.write(f"Page {1 + st.session_state.page} of {total_pages}")
        start = 10 * st.session_state.page
        end = start + 10
        st.write(load_data().iloc[start:end])

    elif choice == 'Update':                                       # To give feedbacks and update in feedback table
        st.subheader('Adding Feedback')
        if "entry" not in st.session_state:
            st.session_state.entry = 0

        def next_entry():
            st.session_state.entry += 1

        def prev_entry():
            st.session_state.entry -= 1

        def add_feedback(fb):
            result(fb, st.session_state.entry)

        def search_entry(n):
            st.session_state.entry = n - 1

        num = st.number_input("enter entry number", min_value=1, max_value=len(load_data()))
        if st.button("search"):
            search_entry(num)

        col1, col2, col3, _ = st.columns([0.1, 0.27, 0.1, 0.53])

        if st.session_state.entry < (len(load_data()) - 1):
            col3.button(">", on_click=next_entry)
        else:
            col3.write("")

        if st.session_state.entry > 0:
            col1.button("<", on_click=prev_entry)
        else:
            col1.write("")

        col2.write(f"Showing Entry no. {1 + st.session_state.entry} of {len(load_data())}")
        start = 1 * st.session_state.entry
        st.write("")
        st.write(load_data().loc[start])

        _, col1, col2 = st.columns([0.8, 0.1, 0.1])
        if col1.button("👍"):
            add_feedback("👍")
        if col2.button("👎"):
            add_feedback("👎")
    elif choice == 'Feedbacks':                                 # To show final feedback table along with responses
        st.subheader('Feedback Table')
        if "fbpage" not in st.session_state:
            st.session_state.fbpage = 0

        def next_page():
            st.session_state.fbpage += 1

        def prev_page():
            st.session_state.fbpage -= 1

        col1, col2, col3, _ = st.columns([0.1, 0.17, 0.1, 0.63])
        total_fbpages = len(load_fb_data()) // 10 + 1
        if st.session_state.fbpage < (total_fbpages - 1):
            col3.button(">", on_click=next_page)
        else:
            col3.write("")

        if st.session_state.fbpage > 0:
            col1.button("<", on_click=prev_page)
        else:
            col1.write("")

        col2.write(f"Page {1 + st.session_state.fbpage} of {total_fbpages}")
        start = 10 * st.session_state.fbpage
        end = start + 10
        st.write(load_fb_data().iloc[start:end])


main()
