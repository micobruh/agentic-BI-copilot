import streamlit as st

# Page configuration
st.set_page_config(page_title="BI Assistant", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("Question Answering")

# Show history of interactions
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Enter your question")

if query:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            # start_generation = time.time()     
            placeholder = st.empty()  # Placeholder to update the answer in real-time
            full_response = ""
            
            with st.spinner(f"Generating answer"):
                for chunk in rag_chain.stream({"query": query}):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")  # Show the answer with a cursor
                placeholder.markdown(full_response)  # Final answer without cursor
                # answer = rag_chain.invoke({"query": query, "context": context})
                # generation_time = time.time() - start_generation
                # st.write(answer)

            st.session_state.messages.append({"role": "assistant", "content": full_response})  # Save the assistant's response in session state

            # st.markdown("### Performance")
            # st.write(f"Retrieval time: {retrieval_time:.2f} seconds")
            # st.write(f"Generation time: {generation_time:.2f} seconds")

            # with st.expander("Reference Sources"):
            #     for ref in refs:
            #         st.markdown(f"- {ref}")

if st.button("Clear History"):
    st.session_state.messages = []
    st.rerun()  
