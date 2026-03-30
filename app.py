import streamlit as st
import google.generativeai as genai

# --- UI Setup ---
st.set_page_config(page_title="XM Strategy Scout", page_icon="🎯", layout="wide")
st.title("🎯 XM Strategy Scout")
st.markdown("Powered by Google Gemini & Google Search")

# Check for secret
if "GEMINI_API_KEY" in st.secrets:
    gemini_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# Configure Gemini with Google Search tool
genai.configure(api_key=gemini_key)

# We use the 'google_search' tool to let Gemini browse the live web
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[{"google_search_retrieval": {}}] 
)

company_name = st.text_input("Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    with st.spinner(f"Searching Google for {company_name} insights..."):
        try:
            # The comprehensive prompt that handles search + analysis + executive lookup
            prompt = f"""
            Perform a search for the company '{company_name}' and provide a strategic report based on the following:

            1. FIND DATA: Search for their most recent 10-K (Annual Report), latest quarterly earnings transcript, and news from the last 6 months.
            
            2. APPLY EXPERIENCE MANAGEMENT FILTER: 
               - Identify exactly TWO major C-Level business problems. 
               - IGNORE purely operational issues (supply chain, raw material costs, inflation). 
               - FOCUS ONLY ON: Customer Experience (churn, digital adoption, NPS), Employee Experience (attrition, productivity, talent), or Market/Product Innovation (brand perception).
            
            3. EXECUTIVE MAPPING: Search for and identify 10-15 current C-Suite and VP/Director level executives at {company_name}.
            
            FORMAT:
            - Provide a 'Strategic Overview' section.
            - Provide a 'Top 2 C-Level Priorities' section with 3-4 sentences of explanation for each.
            - Provide a Markdown Table for the executives including: Name, Title, and Department.
            - Use a professional consultant's tone.
            """

            # Run the request
            response = model.generate_content(prompt)

            # Display the result
            st.markdown("---")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Check if your Gemini API key has 'Google Search' permissions enabled in AI Studio.")
