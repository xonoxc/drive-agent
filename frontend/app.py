import asyncio

import streamlit as st

from api_client import api_client


st.set_page_config(
    page_title="Drive Agent",
    layout="wide",
)

st.title("TailorTalk Drive Agent")

st.caption("Search Google Drive using natural language")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("files"):
            for file in msg["files"]:
                st.markdown(
                    f"""
                    ### {file["name"]}

                    - Type: `{file["mimeType"]}`
                    """
                )


message = st.chat_input(
    "Ask something about your files...",
)


if message:
    st.session_state.messages.append({"role": "user", "content": message})

    with st.chat_message("user"):
        st.write(message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(
                api_client.chat(
                    message,
                    st.session_state.messages[:-1],
                )
            )

        st.write(response["response"])

        for file in response["files"]:
            st.markdown(
                f"""
                ### {file["name"]}

                - Type: `{file["mimeType"]}`
                """
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["response"],
            "files": response["files"],
        }
    )
