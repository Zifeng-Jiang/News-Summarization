import streamlit as st
import transformers
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import re

access_token = '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'

st.title('📰News Summarization!')
st.subheader("Got no time to read those lengthy news articals?🧐")
st.write("Copy and paste your news article here and I will tell you what happened.😎")
model_name = st.selectbox("Pick a summarization model📊", ["T5 (Fast and small)", "PEGASUS(Large but slow)", "BART(Somewhere in between)"])
txt = st.text_area("📃News to summarize:", height=200)
submitted = st.button("🤖Generate summarization!")

def extract_first_n_words(text, n):
    
    tokens = re.findall(r'\b\w+\b|[,.!?;:"]|\s+', text)
    
    combined = []
    word_count = 0
    for token in tokens:
        if re.match(r'\b\w+\b', token):  
            if word_count == n: 
                break
            word_count += 1
        combined.append(token)
    return ''.join(combined)

def generate_response(txt, model_name):
    # Instantiate the LLM model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=access_token)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, token=access_token)
    # Text preprocessing
    n = 800
    text = extract_first_n_words(txt, n)
    news = 'summarize: '+ text
    # Text summarization
    summarizer = pipeline("summarization", model = model, tokenizer = tokenizer, max_length = 100)
    summary = summarizer(news)
    return summary[0]['summary_text']

if submitted:
    if txt:
        if model_name == "T5 (Fast and small)":
            summary = generate_response(txt, 'A-C-E/t5-news')
        if model_name == "PEGASUS(Large but slow)":
            summary = generate_response(txt, 'A-C-E/pegasus-news')
        if model_name == "BART(Somewhere in between)":
            summary = generate_response(txt, 'A-C-E/bart-news')
        if len(summary):
            st.info(summary)
            st.write("Disclaimer:")
            st.write("This app uses the AI Large Language Models to generate news summarization, the summarization is just for reference.")
            st.write("The app may generate misleading or inaccurate information, be careful!")
            st.write("The final right of interpretation belongs to the app owner.")
    else:
        st.warning("Please input some news!")  # must have text input