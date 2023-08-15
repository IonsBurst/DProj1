import streamlit as st
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
    .stTextInput input[type="text"], .stTextInput input[type="password"] {
        background-color: #fff59d;
        color: #333;
    }
    .stTextInput input[type="text"]::placeholder, .stTextInput input[type="password"]::placeholder {
        color: #555;
    }
    .stMarkdown {
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
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
    # Add child id
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
        st.success(f"Logged in successfully as child: {st.session_state['child_id']}")


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
    st.header(f"Child ID: {st.session_state['child_id']}")  # displaying child_id at the top

    st.sidebar.image("TeddyLogo.png", width=100)
    st.sidebar.title("Navigation")

    options = st.sidebar.radio("Pages", options=["What would you like Teddy to teach you today?", "Graphs and Data"])

    if options == "What would you like Teddy to teach you today?":
        prompt_request()
    elif options == "Graphs and Data":
        graphs_and_data()


def prompt_request():
    st.header("What would you like Teddy to teach you today?")

    button_a = st.button("Practice naming the 4 nations in the United Kingdom.")
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
            file_ = open("C:\\Users\\jacki\\PycharmProjects\\pythonProject2\\teddyGif1.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="teddy gif">',
                unsafe_allow_html=True,
            )


def graphs_and_data():
    st.header("Graphs and Data")


if __name__ == "__main__":
    if 'child_id' in st.session_state and st.session_state.get('verified', False):
        main_page()
    else:
        login_page()
