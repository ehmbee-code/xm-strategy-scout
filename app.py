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

# Configure Gemini
genai.configure(api_key=gemini_key)

# We use the 'google_search' tool. 
# Using the specific 'gemini-1.5-flash' name which is most compatible with search.
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    tools=[{"google_search_retrieval": {}}]
)

company_name = st.text_input("Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner(f"Searching Google for {company_name} insights..."):
            try:
                # The prompt is designed to trigger the search grounding
                prompt = f"""
                You are a Strategic Business Analyst. Use Google Search to research {company_name}.
                
                1. RESEARCH: Find their most recent 10-K (Annual Report), the latest quarterly earnings transcript, and news from the last 6 months.
                
                2. XM FILTER: Identify exactly TWO major C-Level business problems. 
                   - Ignore logistics, supply chain, or interest rates. 
                   - Focus ONLY on: Customer Experience (churn, digital friction), Employee Experience (attrition, productivity), or Innovation (brand perception).
                
                3. EXECUTIVES: List 10-15 current C-Suite and VP/Director level executives at {company_name}.
                
                FORMAT:
                - Use a professional 'Executive Summary' tone.
                - Provide a clear Table for the executives.
                - Mention the source of the data (e.g., 'According to the 2023 10-K...').
                """

                # Run the request (using the beta configuration internally)
                response = model.generate_content(prompt)

                # Display the result
                st.markdown("---")
                if response.text:
                    st.markdown(response.text)
                else:
                    st.error("The model didn't return a text response. Try again.")

            except Exception as e:
                # Catching common Google Search permission issues
                if "403" in str(e):
                    st.error("Access Denied: Your API key might not have Search permissions or is in a restricted region.")
                else:
                    st.error(f"Something went wrong: {e}")
