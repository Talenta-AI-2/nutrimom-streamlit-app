import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv('.env')

# openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = os.getenv('OPENAPI_KEY')

st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")

def main():
    st.title("Chatbot")

    def get_response(user_query, chat_history):
        template = """
        Kamu adalah AI Assistant yang pintar dalam hal kesehatan, terutama Stunting. Jawab pertanyaan pengguna berikut ini

        Chat history: {chat_history}

        User question: {user_question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOpenAI(openai_api_key=openai_api_key)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({
            "chat_history": chat_history,
            "user_question": user_query,
        })

    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Halo, ada yang bisa saya bantu hari ini?"),
        ]

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.chat_history)
            st.write(response)

        st.session_state.chat_history.append(AIMessage(content=response))

if __name__ == "__main__":
    main()
