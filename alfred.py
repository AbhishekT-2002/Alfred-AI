import openai
import streamlit as st
import spacy
import pandas as pd
import json
import base64
import pdfplumber
import re
from textblob import TextBlob

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("Spacy model not found. Please run 'python -m spacy download en_core_web_sm' to install it.")
    st.stop()

# Initialize session state variables
if 'message_list' not in st.session_state:
    st.session_state.message_list = [
        {"role": "system", "content": "You are a helpful assistant named Alfred AI."}
    ]
if 'pdf_message_list' not in st.session_state:
    st.session_state.pdf_message_list = [
        {"role": "system", "content": "You are a helpful assistant named Alfred AI. Your task is to answer questions based on the provided PDF content."}
    ]
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'response_tone' not in st.session_state:
    st.session_state.response_tone = "Neutral"
if 'interaction_count' not in st.session_state:
    st.session_state.interaction_count = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "welcome"

class Conversation:
    client = openai.OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
    )

    def __init__(self):
        pass

    def message(self, question, context=""):
        st.session_state.interaction_count += 1
        context_question = f"{context}\n\nUser's question: {question}" if context else question

        tone_instruction = self.get_tone_instruction()

        messages = [
            {"role": "system", "content": f"You are a helpful assistant named Alfred AI. {tone_instruction}"},
            {"role": "user", "content": context_question}
        ]

        try:
            response = self.client.chat.completions.create(
                model="qwen2:0.5b",
                messages=messages
            )

            assistant_response = {"role": "assistant", "content": response.choices[0].message.content}
            return assistant_response["content"]
        except Exception as e:
            st.error(f"An error occurred while processing your request: {str(e)}")
            return None

    def get_tone_instruction(self):
        tone_map = {
            "Neutral": "Respond in a neutral and balanced tone.",
            "Friendly": "Respond in a warm and friendly tone, as if talking to a close friend.",
            "Formal": "Respond in a formal and professional tone, suitable for business communication.",
            "Casual": "Respond in a casual and relaxed tone, using informal language."
        }
        return tone_map.get(st.session_state.response_tone, "")

# ... (keep all the helper functions like clean_text, extract_text_from_pdf, etc.)
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += clean_text(page_text)
        return text
    except Exception as e:
        st.error(f"An error occurred while extracting text from the PDF: {str(e)}")
        return None

def extract_entities(text):
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        st.error(f"An error occurred while extracting entities: {str(e)}")
        return None

def format_entities_for_display(entities):
    df = pd.DataFrame(entities, columns=['Entity', 'Type'])
    color_map = {
        "PERSON": "orange",
        "CARDINAL": "lightblue",
        "ORG": "blue",
        "GPE": "darkgreen",
        "DATE": "pink",
        "TIME": "brown",
        "MONEY": "green",
        "LOC": "cyan",
        "PRODUCT": "yellow",
        "LANGUAGE": "purple",
        "WORK_OF_ART": "gold"
    }
    df['Color'] = df['Type'].map(color_map).fillna('black')
    return df

def apply_color_map(df):
    def color_map(row):
        return ['background-color: {}'.format(color) for color in row]

    return df.style.apply(color_map, subset=['Color'], axis=1)

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="named_entities.csv">Download CSV file</a>'

def export_conversation():
    conversation_data = json.dumps(st.session_state.message_list, indent=2)
    b64 = base64.b64encode(conversation_data.encode()).decode()
    return f'<a href="data:file/json;base64,{b64}" download="conversation_history.json">Download Conversation History</a>'

def search_text(text, query):
    return [match.start() for match in re.finditer(re.escape(query), text, re.IGNORECASE)]

def display_search_results(text, query):
    indices = search_text(text, query)
    if indices:
        for index in indices:
            snippet = text[max(0, index - 30):index + 30]
            st.write(f"...{snippet}...")
    else:
        st.write("No results found.")

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment
def main():
    st.set_page_config(page_title="Alfred AI", layout="wide")
    st.title('Alfred AI')

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "General Chat", "PDF Analysis", "Settings"])

    if page == "Welcome":
        welcome_page()
    elif page == "General Chat":
        chat_page()
    elif page == "PDF Analysis":
        pdf_analysis_page()
    elif page == "Settings":
        settings_page()

def welcome_page():
    st.header("Welcome to Alfred AI")
    if st.session_state.user_name == "":
        st.write("Please enter your name to continue.")
        user_name = st.text_input("Enter your name:")
        if st.button("Continue"):
            if user_name:
                st.session_state.user_name = user_name
                st.success(f"Welcome, {user_name}! Please use the sidebar to navigate.")
            else:
                st.error("Name cannot be empty.")
    else:
        st.write(f"Welcome back, {st.session_state.user_name}!")
        st.write("Use the sidebar to navigate through different features of Alfred AI.")

def chat_page():
    st.header("General Chat with Alfred AI")
    
    conversation = Conversation()

    for message in st.session_state.message_list:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(f"{st.session_state.user_name}: {message['content']}")
        elif message['role'] == 'assistant':
            with st.chat_message("assistant"):
                st.write(f"Alfred AI: {message['content']}")

    prompt = st.chat_input("Type your message here")
    if prompt:
        with st.spinner('Thinking...'):
            answer = conversation.message(prompt)
            if answer:
                st.session_state.message_list.append({"role": "user", "content": prompt})
                st.session_state.message_list.append({"role": "assistant", "content": answer})
                st.experimental_rerun()

    if st.button('Clear Chat'):
        if st.checkbox('Are you sure you want to clear the chat?'):
            st.session_state.message_list = [
                {"role": "system", "content": "You are a helpful assistant named Alfred AI."}
            ]
            st.session_state.interaction_count = 0
            st.success("Chat cleared!")
            st.experimental_rerun()

def pdf_analysis_page():
    st.header("PDF Analysis")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text:
            st.session_state.pdf_text = pdf_text
            st.success("PDF text extracted successfully!")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Named Entities", "Extracted Text", "Search", "Sentiment Analysis", "Chat with PDF"])
            
            with tab1:
                entities = extract_entities(st.session_state.pdf_text)
                if entities:
                    entity_df = format_entities_for_display(entities)
                    st.dataframe(apply_color_map(entity_df))
                    st.markdown(get_table_download_link(entity_df), unsafe_allow_html=True)
                else:
                    st.write("No named entities found.")

            with tab2:
                st.text_area("Extracted PDF Text", st.session_state.pdf_text, height=300)

            with tab3:
                search_query = st.text_input("Enter a keyword or phrase to search:")
                if search_query:
                    display_search_results(st.session_state.pdf_text, search_query)

            with tab4:
                if st.button("Analyze Sentiment"):
                    sentiment = analyze_sentiment(st.session_state.pdf_text)
                    st.write(f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")

            with tab5:
                st.subheader("Chat about the PDF")
                conversation = Conversation()

                for message in st.session_state.pdf_message_list:
                    if message['role'] == 'user':
                        with st.chat_message("user"):
                            st.write(f"{st.session_state.user_name}: {message['content']}")
                    elif message['role'] == 'assistant':
                        with st.chat_message("assistant"):
                            st.write(f"Alfred AI: {message['content']}")

                pdf_prompt = st.chat_input("Ask a question about the PDF")
                if pdf_prompt:
                    with st.spinner('Analyzing PDF and generating response...'):
                        pdf_answer = conversation.message(pdf_prompt, context=st.session_state.pdf_text)
                        if pdf_answer:
                            st.session_state.pdf_message_list.append({"role": "user", "content": pdf_prompt})
                            st.session_state.pdf_message_list.append({"role": "assistant", "content": pdf_answer})
                            st.experimental_rerun()

                if st.button('Clear PDF Chat'):
                    if st.checkbox('Are you sure you want to clear the PDF chat?'):
                        st.session_state.pdf_message_list = [
                            {"role": "system", "content": "You are a helpful assistant named Alfred AI. Your task is to answer questions based on the provided PDF content."}
                        ]
                        st.success("PDF chat cleared!")
                        st.experimental_rerun()

def settings_page():
    st.header("Settings")

    st.subheader("Response Tone")
    st.session_state.response_tone = st.selectbox(
        "Select Alfred AI's response tone:",
        ["Neutral", "Friendly", "Formal", "Casual"]
    )

    st.subheader("Export Conversation")
    st.markdown(export_conversation(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()