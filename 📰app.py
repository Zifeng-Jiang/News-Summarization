# Try this app at: https://newssummarizationapp-l4haoqf2uzuxjeuopdonql.streamlit.app/
import streamlit as st
import requests

API_TOKEN = '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'

st.title('📰News Summarization!')
st.subheader("Got no time to read those lengthy news articals?🧐")
st.write("Copy and paste your news article here and I will tell you what happened.😎")
model_name = st.selectbox("Pick a summarization model📊", ["BART", "PEGASUS", "T5"])
txt = st.text_area("📃News to summarize:", height=200)
submitted = st.button("🤖Generate summarization!")

def query(API_URL, headers, payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if submitted:
    if txt:
        if model_name == "T5":
            API_URL = "https://api-inference.huggingface.co/models/A-C-E/t5-news"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            summary = query(API_URL, headers, {"inputs": "summarize: "+ txt,
                                               "options": {"wait_for_model": True}})

        if model_name == "PEGASUS":
            API_URL = "https://api-inference.huggingface.co/models/A-C-E/pegasus-news"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            summary = query(API_URL, headers, {"inputs": "summarize: "+ txt,
                                               "options": {"wait_for_model": True},
                                               'parameters': {'truncation': 'only_first'}})
        if model_name == "BART":
            API_URL = "https://api-inference.huggingface.co/models/A-C-E/bart-news"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            summary = query(API_URL, headers, {"inputs": "summarize: "+ txt,
                                               "options": {"wait_for_model": True},
                                               'parameters': {'truncation': 'only_first'}})
        if len(summary):
            #st.info(summary)
            st.info(summary[0]['generated_text'])
            st.write("Disclaimer:")
            st.write("This app uses the AI Large Language Models to generate news summarization, the summarization is just for reference.")
            st.write("The app may generate misleading or inaccurate information, be careful!")
            st.write("The final right of interpretation belongs to the app owner.")
    else:
        st.warning("Please input some news!")  # must have text input
