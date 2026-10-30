import requests
import streamlit as st

API_UPLOAD_URL = "http://localhost:8000/upload"
API_ASK_URL = "http://localhost:8000/ask"
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


st.title("RAG Demo")

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

uploaded_file = st.file_uploader(
    "Choose a PDF file you want to ask questions about.",
    type=["pdf"],
)

if uploaded_file is not None:
    if uploaded_file.size >= MAX_UPLOAD_SIZE:
        st.error("The PDF must be smaller than 10 MB.")
    elif st.button("Upload"):
        try:
            with st.spinner("File is uploading!"):
                response = requests.post(
                    API_UPLOAD_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    },
                    timeout=(10, 300),
                )
            response.raise_for_status()
            st.session_state.pdf_uploaded = True
            st.session_state.chat_messages = []
            st.success(response.json().get("message", "PDF uploaded successfully."))
        except requests.HTTPError as exc:
            try:
                detail = response.json().get("detail", str(exc))
            except ValueError:
                detail = str(exc)
            st.error(f"Upload failed: {detail}")
        except requests.RequestException as exc:
            st.error(f"Could not connect to the API: {exc}")

if st.session_state.pdf_uploaded:
    with st.container():
        if question := st.chat_input("Enter you question here:"):
            st.session_state.chat_messages.append(
                {"role": "user", "content": question}
            )
            with st.spinner("Retrieving answer ..."):
                try:
                    response = requests.get(
                        API_ASK_URL,
                        params={"question": question},
                        timeout=(10, 300),
                    )
                    response.raise_for_status()
                    answer = response.json()["answer"]
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except requests.HTTPError as exc:
                    try:
                        detail = response.json().get("detail", str(exc))
                    except ValueError:
                        detail = str(exc)
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "content": detail, "error": True}
                    )
                except (requests.RequestException, KeyError, ValueError) as exc:
                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": f"Could not get an answer: {exc}",
                            "error": True,
                        }
                    )

        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                if message.get("error"):
                    st.error(message["content"])
                else:
                    st.markdown(message["content"])
