import streamlit as st
import requests

# Function to call the API endpoint
def search_documents(query):
    url = "http://localhost:8000/search"
    payload = {"query": query}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch response from API"}

# Streamlit app UI
def main():
    st.title("Policy QA Chat")
    st.write("Welcome to the Policy QA Chat!")

    # Initialize chat history if not present in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input field for user query
    query = st.text_input("You:", key="input_field")

    # "Send" button
    if st.button("Send"):
        if query:
            # Call the API endpoint
            response = search_documents(query)
            
            # Display response
            if "error" in response:
                st.error("Failed to fetch response from API")
            else:
                # Append user query and system response to chat history
                st.session_state.chat_history.insert(0, f"You: {query}")
                st.session_state.chat_history.insert(1, f"Policy QA Service: {response['answer']}")
                source_documents = ', '.join([x.split("/")[-1] for x in response["sources"]])
                st.session_state.chat_history.insert(2, f"Source : {source_documents}") 
                st.session_state.chat_history.insert(3, "")
                st.text("")  # Add empty space between chat entries
        

    # Display chat history
    for entry in st.session_state.chat_history:
        if entry.startswith("You:"):
            st.write(f"<div style='color: blue;'>{entry}</div>", unsafe_allow_html=True)
        elif entry.startswith("Policy QA Service:"):
            st.write(f"<div style='color: green;'>{entry}</div>", unsafe_allow_html=True)
        elif entry.startswith("Source :"):
            st.write(f"<div style='color: red;'>{entry}</div>", unsafe_allow_html=True)
        else:
            st.write(entry)

# Run the Streamlit app
if __name__ == "__main__":
    main()
