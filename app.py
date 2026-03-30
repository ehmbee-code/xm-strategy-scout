import streamlit as st
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

st.set_page_config(page_title="XM Strategy Scout", layout="wide")
st.title("🎯 XM Strategy Scout")

with st.sidebar:
    st.header("1. Authentication")
    openai_key = st.text_input("OpenAI API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.write("This tool researches 10-Ks and Transcripts to find Customer and Employee experience gaps.")

company_name = st.text_input("2. Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    if not openai_key or not tavily_key:
        st.warning("Please enter your API keys in the sidebar.")
    else:
        with st.spinner(f"Analyzing {company_name}... (may take 60s)"):
            try:
                llm = ChatOpenAI(model="gpt-4-turbo-preview", openai_api_key=openai_key, temperature=0)
                search = TavilySearchResults(tavily_api_key=tavily_key)
                
                agent = initialize_agent([search], llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)
                
                query = f"""
                Research {company_name}. 
                1. Find their latest 10-K and most recent earnings call transcript.
                2. Identify TWO major C-level business problems regarding Customer Experience, Employee Experience, or Market Innovation.
                3. Ignore purely operational issues like fuel costs or supply chain.
                4. List 10 specific C-Suite and VP-level executives.
                Format as a clean executive summary with a table for executives.
                """
                
                response = agent.run(query)
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error: {e}")
