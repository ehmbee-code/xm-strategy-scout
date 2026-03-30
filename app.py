import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub

# --- UI Setup ---
st.set_page_config(page_title="XM Strategy Scout", layout="wide")
st.title("🎯 XM Strategy Scout")

with st.sidebar:
    st.header("1. Authentication")
    openai_key = st.text_input("OpenAI API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    st.info("Get a Tavily key at tavily.com and OpenAI key at platform.openai.com")

company_name = st.text_input("2. Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    if not openai_key or not tavily_key:
        st.warning("Please enter both API keys in the sidebar.")
    else:
        with st.spinner(f"Researching {company_name}..."):
            try:
                # 1. Setup Tools and LLM
                llm = ChatOpenAI(model="gpt-4-turbo-preview", api_key=openai_key, temperature=0)
                search = TavilySearchResults(tavily_api_key=tavily_key)
                tools = [search]

                # 2. Get the prompt template from LangChain Hub
                prompt = hub.pull("hwchase17/openai-functions-agent")

                # 3. Construct the Agent
                agent = create_openai_functions_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

                # 4. The Specific XM Instruction
                task = f"""
                Research {company_name} and provide a report.
                
                PHASE 1: FIND DATA
                Search for the most recent 10-K (Annual Report) and the latest quarterly earnings transcript.
                
                PHASE 2: ANALYZE XM GAPS
                Identify exactly TWO major C-Level business problems. 
                Use an 'Experience Management' filter: ignore logistics/supply chain. 
                Focus on: Customer Experience (churn, digital adoption) OR Employee Experience (attrition, productivity) OR Innovation (brand perception).
                
                PHASE 3: EXECUTIVES
                Identify 10-15 C-Suite and VP-level executives at {company_name} with their titles.
                
                FORMAT: Present as a professional Executive Summary with a Table for the executives.
                """

                # 5. Run
                response = agent_executor.invoke({{"input": task}})
                st.markdown("---")
                st.markdown(response["output"])
                
            except Exception as e:
                st.error(f"An error occurred: {{e}}")
