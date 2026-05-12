import asyncio

import streamlit as st

from .api_client import api_client


st.set_page_config(
    page_title="TailorTalk Drive Agent",
    layout="wide",
)

st.title("📂 TailorTalk Drive Agent")

st.caption("Search Google Drive using natural language")


message = st.chat_input(
    "Ask something about your files...",
)


if message:
    with st.chat_message("user"):
        st.write(message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(
                api_client.chat(
                    message,
                )
            )

        st.write(response["response"])

        st.divider()

        for file in response["files"]:
            st.markdown(
                f"""
                ### 📄 {file["name"]}

                - Type: `{file["mimeType"]}`
                """
            )
