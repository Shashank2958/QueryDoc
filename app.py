import streamlit as st
from dotenv import load_dotenv
 
from utils.pdf_reader import extract_text_from_pdf
from utils.chunker import split_text_into_chunks
from utils.embedder import load_embedding_model, get_embeddings
from utils.vector_store import (
    get_chroma_client,
    get_or_create_collection,
    store_chunks,
    retrieve_relevant_chunks,
)
from utils.llm import get_gemini_client, get_answer_from_gemini
 
load_dotenv()
 
st.title("QueryDoc")
 
# --- Resources load karna (cached, ek hi baar honge) ---
embedding_model = st.cache_resource(load_embedding_model)()
chroma_client = st.cache_resource(get_chroma_client)()
collection = get_or_create_collection(chroma_client)
gemini_client = st.cache_resource(get_gemini_client)()
 
# --- Chat History Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # yaha {"role": ..., "content": ...} pairs honge
 
# Ye track karta hai ki PDF process ho chuki hai ya nahi (taaki har
# rerun pe dobara process na ho, aur question box tabhi dikhe jab
# PDF ready ho)
if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False
 
# --- PDF Upload -- Sidebar mein, taaki main area sirf chat ke liye rahe ---
with st.sidebar:
    st.subheader("Upload your PDF")
    uploaded_file = st.file_uploader("choose your pdf", type="pdf", label_visibility="collapsed")
 
    if uploaded_file is not None and not st.session_state.pdf_ready:
        # Poora processing (extract -> chunk -> embed -> store) ek
        # spinner ke peeche chalta hai -- user ko chunk-count jaisi
        # technical details nahi dikhti, bas ek loading indicator.
        with st.spinner("PDF is processing..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            chunks = split_text_into_chunks(extracted_text)
            embeddings = get_embeddings(embedding_model, chunks)
            store_chunks(collection, chunks, embeddings)
 
        st.session_state.pdf_ready = True
        st.success("PDF uploaded successfully..")
 
    st.divider()
 
    # --- Chat History Sidebar: sirf titles, click karne pe khulte hain ---
    if st.session_state.chat_history:
        st.subheader("Chat History")
        # chat_history mein har 2 items (user + assistant) ek Q&A pair
        # banate hain -- isliye step=2 leke loop chalate hain
        for i in range(0, len(st.session_state.chat_history), 2):
            question_text = st.session_state.chat_history[i]["content"]
            title = question_text[:35]
            if len(question_text) > 35:
                title += "..."
            st.button(title, key=f"hist_{i}")
 
# --- Main Chat Area ---
if st.session_state.pdf_ready:
    # Ab tak ki saari history ko chat-bubble style mein dikhate hain.
    # st.chat_message(role) ek "bubble" banata hai -- role ke hisaab se
    # (user/assistant) Streamlit automatically alag icon aur alignment deta hai.
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
 
    # st.chat_input ek chhota box neeche fix rehta hai (jaise ChatGPT).
    # User Enter dabaye ya bheja hua icon click kare, dono se submit hota hai.
    user_input = st.chat_input("Ask your doubt or Question")
 
    if user_input:
        # User ka message turant ek bubble mein dikha dete hain
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
 
        # Jawab generate karte waqt, assistant ke bubble mein spinner dikhate hain
        with st.chat_message("assistant"):
            with st.spinner("Searching relevant Answer..."):
                input_embedding = get_embeddings(embedding_model, [user_input])
                retrieved_chunks = retrieve_relevant_chunks(
                    collection, input_embedding, n_results=4
                )
                answer = get_answer_from_gemini(
                    gemini_client, user_input, retrieved_chunks
                )
            st.markdown(answer)
 
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
else:
    st.info("Firstly upload the pdf and ask question..")
 
