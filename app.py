import streamlit as st
import pypdf
from groq import Groq

st.title("📄 AI Document Q&A")
st.write("Upload a PDF and ask it anything")

groq_key = st.text_input("Enter your Groq API key", type="password")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and groq_key:
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    st.success("PDF loaded successfully!")
    
    question = st.text_input("Ask a question about your document")
    
    if question:
        client = Groq(api_key=groq_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Based on this document, answer the question.\n\nDocument:\n{text}\n\nQuestion: {question}"
                }
            ]
        )
        
        st.write("**Answer:**", response.choices[0].message.content)