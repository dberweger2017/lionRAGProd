import streamlit as st
import requests

st.set_page_config(page_title="BG Gallus", page_icon="🏫")

def n8n_chat(prompt, url="https://lionlaal.app.n8n.cloud/webhook/chat"):
    payload = {
        "chatInput": f"{prompt}",
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("output", str(data))
    except requests.exceptions.RequestException as e:
        error_text = ""
        if hasattr(e, 'response') and e.response is not None:
            error_text = e.response.text
            st.error(f"Server Error Details: {error_text}")
        return f"Fehler bei der Anfrage: {e} {error_text}"
    except Exception as e:
        st.error(f"Unerwarteter Fehler: {e}")
        return f"Fehler: {e}"

def n8n_files(file_obj, url="https://lionlaal.app.n8n.cloud/webhook/files"):
    files = {"file": file_obj}
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return "Datei erfolgreich an n8n gesendet."
    except requests.exceptions.RequestException as e:
        error_text = ""
        if hasattr(e, 'response') and e.response is not None:
            error_text = e.response.text
            st.error(f"Upload Fehler Details: {error_text}")
        return f"Fehler beim Hochladen: {e} {error_text}"
    except Exception as e:
        st.error(f"Unerwarteter Upload Fehler: {e}")
        return f"Fehler beim Hochladen: {e}"

#st.title("BG Gallus Assistent")
st.image("assets/5855183e-2ee5-4e13-b999-f9cc67b4b153.JPG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for file upload and logo
with st.sidebar:
    st.image("assets/5855183e-2ee5-4e13-b999-f9cc67b4b153.JPG")
    
    file = st.file_uploader("Datei hochladen", type=["pdf", "csv"])
    if file:
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != file.name:
            with st.spinner("Lade Datei hoch..."):
                msg = n8n_files(file)
                st.session_state.last_uploaded = file.name
                st.session_state.messages.append({"role": "assistant", "content": f"📎 {file.name}: {msg}"})

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("N"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("G"):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Schreiben Sie etwas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("N"):
        st.markdown(f"{prompt}")

    with st.chat_message("G"):
        with st.spinner("Denke nach..."):
            response = n8n_chat(prompt)
            st.markdown(f"{response}")
    
    st.session_state.messages.append({"role": "assistant", "content": response})