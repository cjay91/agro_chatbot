import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat

from answer import *

openai.api_key = st.secrets["OPENAI_API_KEY"]
# Sidebar contents
# with st.sidebar:
#     st.title('')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')


# User input
# Function for taking user provided prompt as input
user_input = st.chat_input("Ask Something")

# def get_text():
#     input_text = st.chat_input("Ask Something")
#     return input_text


# Applying the user input box
# with input_container:
#     user_input = get_text()

# Response output
# Function for taking user prompt as input followed by producing AI generated responses

def generate_response(user_input):
    for i in range(len(st.session_state['past'])):
        try:
            prev_history.append(
                {"user": st.session_state['past'][i], "ai": st.session_state["generated"][i]})
        except:
            prev_history.append(
                {"user": st.session_state['past'][i], "ai": "null"})

    answer = get_answer_using_function_call(user_input, prev_history)

    return answer

template = '''
User:
You are an expert in your domain. Please provide your expert and user-friendly response based on the context provided. You should aim to provide a clear, concise, and accurate response including contact details. If the question is not taken from the given context, do not respond with general knowledge, and only leave a polite message. Polite message should be this - Thank you for your inquiry. Please note that the information provided by this program is restricted to Agroworld Company information. If you have inquiries related to Agroworld or need assistance on a different topic within the defined scope, feel free to ask. I'm here to help!

Modified Instructions:

1. Craft responses that are clear, concise, and accurate based on the given context.

2. Include contact details in your responses where applicable.

3. If a question is not taken from the given context, politely inform the user about the scope limitation. Use the predefined message provided below.

4. Ensure that your responses align with the user's request for expert and user-friendly information within the defined domain.

5. If the user does a greeting respond with an appropritate greeting.

Modified Instructions:

Thank you for your inquiry. Please note that the information provided by this program is restricted to Agroworld Company information. If you have inquiries related to Agroworld or need assistance on a different topic within the defined scope, feel free to ask. I'm here to help!

'''
context = get_context(user_input, 10)
myMessages = []
myMessages.append(
    {"role": "system", "content":template })

myMessages.append(
    {"role": "user", "content": "context:\n\n{}.\n\n Answer the following user query according to the given context.:\nuser_input: {}".format(context, user_input)})

if user_input:
    # st.session_state.messages.append({"role": "user", "content": "context:\n\n{}.\n\n Answer the following user query according to the given context:\nuser_input: {}".format(context, user_input)})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-4",
            messages=myMessages,
            stream=True,
        ):
            if "delta" in response["choices"][0] and "content" in response["choices"][0]["delta"]:
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "user", "content": user_input})
st.session_state.messages.append({"role": "assistant", "content": full_response})