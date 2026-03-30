import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

# --- UI Setup ---
st.set_page_config(page_title="XM Strategy Scout", page_icon="🎯", layout="wide")
st.title("🎯 XM Strategy Scout")
st.markdown("Identify C-Suite Experience Gaps & Executive Stakeholders")

with st.sidebar:
    st.header("Authentication")
    openai_key = st.text_input("OpenAI API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    st.info("This tool uses AI to research 10-Ks and earnings transcripts.")

company_name = st.text_input("Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    if not openai_key or not tavily_key:
        st.warning("Please enter your API keys in the sidebar.")
    else:
        with st.spinner(f"Agent is researching {company_name}..."):
            try:
                # Initialize Clients
                client = OpenAI(api_key=openai_key)
                tavily = TavilyClient(api_key=tavily_key)

                # 1. THE SEARCH: Get raw data from the web
                search_query = f"{company_name} latest 10-K annual report earnings transcript experience management customer employee experience"
                search_result = tavily.search(query=search_query, search_depth="advanced", max_results=5)
                
                # 2. THE SEARCH: Get Executives
                exec_query = f"list of C-suite and VP executives at {company_name} LinkedIn"
                exec_result = tavily.search(query=exec_query, search_depth="advanced", max_results=3)

                # 3. THE ANALYSIS: Pass data to OpenAI
                context = f"Search Results for XM: {search_result}\n\nSearch Results for Execs: {exec_result}"
                
                prompt = f"""
                You are a Strategic Business Analyst. Based on the provided context about {company_name}, create a report.
                
                1. Identify exactly TWO major C-Level business problems using an 'Experience Management' filter. 
                   - Ignore logistics, supply chain, or interest rates. 
                   - Focus on: Customer Experience (churn, digital friction) OR Employee Experience (turnover, productivity) OR Innovation (brand perception).
                
                2. List 10-15 key C-Suite and VP/Director level executives at {company_name}.
                
                Format:
                - Use a professional 'Executive Summary' tone.
                - Use a Table for the executives (Name, Title).
                - Use Bold headers.
                """

                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are a helpful business research assistant."},
                        {"role": "user", "content": f"Context: {context}\n\nTask: {prompt}"}
                    ]
                )

                # 4. OUTPUT
                st.markdown("---")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")
