import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
import base64


st.markdown(
    """
    <style>
    body {
        background-color: #ebe852;
    }
    .stButton button {
        background-color: #9c27b0;
        color: white;
    }
    .stApp{
        background-color: #e3cb2b !important;
    }
    .stTextInput input[type="text"],
    .stTextInput input[type="password"] {
        background-color: #fff59d;
        color: #333;
    }
    .stTextInput input[type="text"]::placeholder,
    .stTextInput input[type="password"]::placeholder {
        color: #555;
    }
    .stMarkdown {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

user_data = {
    'info@oiedu.co.uk': 'OI12345678',
}


def login_with_email_password(email, password):
    if email in user_data and user_data[email] == password:
        return True
    return False


def login_page():
    st.image('TeddyLogo.png', width=200)
    st.title("Login to your parents dashboard")
    if 'child_id' not in st.session_state or not st.session_state['child_id']:
        child_id = st.text_input("Child ID")
        child_id_submit = st.button('Submit Child ID')
        if child_id_submit:
            if len(child_id) == 6 and child_id.isdigit():
                st.success("Child ID accepted!")
                st.session_state['child_id'] = child_id
            else:
                st.error('Invalid Child ID. It should be a 6 digit number.')
    else:
        st.success(
            f"Logged in successfully as child: {st.session_state['child_id']}")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    email_password_login_button = st.button("Login with Email/Password")

    if email_password_login_button:
        if login_with_email_password(email, password):
            st.success("Login successful!")
            st.session_state.email = email
            st.session_state.verified = True
        else:
            st.error("Invalid email or password")
            st.session_state.verified = False

    google_login_button = st.button("Login with Google")


def main_page():
    st.title("Parents Dashboard")
    st.header(f"Child ID: {st.session_state['child_id']}")

    st.sidebar.image("TeddyLogo.png", width=100)
    st.sidebar.title("Navigation")

    options = st.sidebar.radio("Pages", options=[
                               "What would you like Teddy to teach you today?", "Graphs and Data"])

    if options == "What would you like Teddy to teach you today?":
        prompt_request()
    elif options == "Graphs and Data":
        graphs_and_data()


def prompt_request():
    st.header("What would you like Teddy to teach you today?")

    button_a = st.button(
        "Practice naming the 4 nations in the United Kingdom.")
    button_b = st.button("Practice the vowels.")
    button_c = st.button("What are the colours in the rainbow?")
    button_d = st.button("Play the game on alphabets")
    button_e = st.button("Spend 5 minutes on the globe.")
    button_f = st.button("Practice breathing exercises for 3 minutes.")

    prompt_mapping = {
        button_a: "Practice naming the 4 nations in the United Kingdom.",
        button_b: "Practice the vowels.",
        button_c: "What are the colours in the rainbow?",
        button_d: "Play the game on alphabets",
        button_e: "Spend 5 minutes on the globe.",
        button_f: "Practice breathing exercises for 3 minutes."
    }

    for button, prompt in prompt_mapping.items():
        if button:
            data = {"Args": prompt}
            with open("output.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            with open("teddyGif1.gif", "rb") as gif_file:
                gif_data = gif_file.read()
                st.image(gif_data)


def graphs_and_data():
    st.header("Graphs and Data")
    relative_json_file_path = "dummydata.json"

    try:
        with open(relative_json_file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        st.warning("Data file not found.")
        return

    highest_tca = 0
    highest_tqa = 0

    for timestamp, record in data.items():
        personal_records = record.get("personalRecords", {})

        tca_value = personal_records.get("TCA", 0)
        if tca_value > highest_tca:
            highest_tca = tca_value

        tqa_value = personal_records.get("TQA", 0)
        if tqa_value > highest_tqa:
            highest_tqa = tqa_value

    totalwrongquestion = highest_tqa - highest_tca

    labels = ["Correctly Answered", "Incorrectly Answered"]
    sizes = [highest_tca, totalwrongquestion]

    fig, ax = plt.subplots()
    colors = ['#B70ED6', '#B70ED6']
    ax.pie(sizes, labels=labels, autopct="%1.1f%%",
           startangle=90, colors=colors)
    ax.set_title("Percentage of Correct Answers")

    fig.patch.set_facecolor('#E3CB2B')
    ax.set_facecolor('#E3CB2B')

    st.pyplot(fig)

    highesterror1 = 0
    top1 = ""
    highesterror2 = 0
    top2 = ""
    highesterror3 = 0
    top3 = ""
    for timestamp, record in data.items():
        for question in record.get("questionsData", []):
            errorAttempts = question.get("errorAttempts")
            the_question = question.get("question")
            if errorAttempts != "":
                comma_count = errorAttempts.count(',')

                if comma_count > highesterror1:
                    highesterror1 = comma_count
                    top1 = question.get("question")
                elif comma_count > highesterror2:
                    highesterror2 = comma_count
                    top2 = question.get("question")
                elif comma_count > highesterror3:
                    highesterror3 = comma_count
                    top3 = question.get("question")

    st.write("1st Difficult Question: ", top1)
    st.write("2nd Difficult Question: ", top2)
    st.write("3rd Difficult Question: ", top3)

    alphabet_total = 0
    sports_total = 0
    restaurant_total = 0
    for timestamp, record in data.items():
        for question in record.get("questionsData", []):
            course = question.get("courseTitle")
            string_time = question.get("timeInverval")
            numeric_time = float(string_time[:-1])
            if course == "Alphabet":
                alphabet_total += numeric_time
            elif course == "Sports":
                sports_total += numeric_time
            elif course == "Restaurant":
                restaurant_total += numeric_time

    data = pd.DataFrame({
        'Variables': ['Alphabet', 'Sports', 'Restaurant'],
        'Values': [alphabet_total, sports_total, restaurant_total]
    })

    fig, ax = plt.subplots()
    bar_color = '#B70ED6'
    ax.bar(data['Variables'], data['Values'], color=bar_color)
    ax.set_ylabel('Seconds')
    ax.set_title('Time Spent on Categories')

    fig.patch.set_facecolor('#E3CB2B')
    ax.set_facecolor('#E3CB2B')

    st.pyplot(fig)


if __name__ == "__main__":
    if 'child_id' in st.session_state and st.session_state.get('verified', False):
        main_page()
    else:
        login_page()
