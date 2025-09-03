# 🦙📚 LlamaIndex - ChatGPT : Chat with the docs

Build a chatbot powered by LlamaIndex that augments GPT 3.5 with the contents of your own data.

![Untitled](https://github.com/Niez-Gharbi/ChatGPT-RAG-Chatbot/assets/57814219/9388d58e-30b3-4f4c-a1fa-b94d94cdb36a)

## Overview of the App

- Takes user queries via Streamlit's `st.chat_input` and displays both user queries and model responses with `st.chat_message`
- Uses LlamaIndex to load and index data and create a chat engine that will retrieve context from that data to respond to each user query

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llamaindex-chat-with-docs.streamlit.app/)

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Try out the app

Once the app is loaded, enter your question about the Streamlit library and wait for a response.
