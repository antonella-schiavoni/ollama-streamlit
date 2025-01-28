import ollama
import streamlit as st

st.title("Ollama Python Chatbot")

# Initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize model
if "model" not in st.session_state:
    st.session_state["model"] = ""

# List models
models = [model["model"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Choose your model", models)

def model_response_generator():
    """
    Generate model response. This function is a generator that yields chunks of the model response.
    """
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter prompt here.."):
    # Add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display model response
    with st.chat_message("assistant"):
        message = st.write_stream(model_response_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})
