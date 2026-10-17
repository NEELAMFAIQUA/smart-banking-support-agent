import streamlit as st

from assistant import answer

st.set_page_config(page_title="Banking Support Guide", page_icon="🏦")
st.title("Banking Support Guide")
st.warning(
    "General education only—not personalized financial advice. "
    "No account access or transactions. Never enter account credentials or codes."
)
st.caption("Answers are retrieved from the bundled FAQ; no external service is used.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a general banking question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    response, references = answer(question)
    with st.chat_message("assistant"):
        st.markdown(response)
        if references:
            with st.expander("Sources and related topics"):
                for article in references:
                    st.markdown(f"- **{article['title']}** — {article['text']}")
    st.session_state.messages.append({"role": "assistant", "content": response})
