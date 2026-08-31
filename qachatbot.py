"""
 Asimple Langchain Streamlit APP with groq
 A beginner-friendly version focusing on core concept
"""
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os

##page config
st.set_page_config(page_title="Simple Langchain chatbot with groq",page_icon="🚀")

# Title
st.title("🚀 simple langchain chat with groq")
st.markdown("Learn Langchain basic with groq's ultra fast interface!")

with st.sidebar:
    st.header("settings")

    ## API key
    # api_key= st.text_input("GROQ API KEY", type="password",help="GET Free API Key at console.groq.com")

    ## Model selection
    model_name= st.selectbox(
        "model",
        ["openai/gpt-oss-20b", "openai/gpt-oss-120b"],
        index=0
    )

    # clear button
    if st.button("clear chat"):
        st.session_state.message=[]
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages= []

# Get Groq API key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

## Initialize LLM
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
    
    ##  Initialize the groq model
    llm=ChatGroq(groq_api_key= api_key,
                 model_name=model_name,
                 temperature=0.7,
                 streaming=True)

    # Create prompt template
    prompt= ChatPromptTemplate.from_messages([
        ("system", "You are a helpfull assistant powerby groq. Answer questions clearly and concisely."),
        ("user", "{question}")
    ])

    ## create chain
    chain= prompt| llm| StrOutputParser()
    return chain

## get chain
chain= get_chain(api_key, model_name)

if not chain:
    st.error("Groq API key is not configured.")
else:
    ## Display the chat messages

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    ## chat input
    if question:=st.chat_input("Ask me anything!"):
        ## Add user message to session state
        st.session_state.messages.append({"role": "user", "content":question})
        with st.chat_message("user"):
            st.write(question)

        # generate response
        with st.chat_message("assistant"):
            message_placeholder= st.empty()
            full_response=""

            try:
                # Stream response from the groq model
                for chunk in chain.stream({"question": question}):
                    full_response+= chunk
                    message_placeholder.markdown(full_response + "")

                message_placeholder.markdown(full_response)

                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {str(e)}")

## Examples

st.markdown("---")
st.markdown("### Try these examples:")
col1, col2= st.columns(2)
with col1:
    st.markdown("- what is langchain?")
    st.markdown("- Explain Groq's LPU technology")
with col2:
    st.markdown("- How do i learn Programming?")
    st.markdown("- write a haiku about AI")

## Footer
st.markdown("---")
st.markdown("Built with langchain & groq | Experience the speed!")



