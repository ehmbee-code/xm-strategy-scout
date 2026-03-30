import streamlit as st
from google import genai
from google.genai import types

# --- UI Setup ---
st.set_page_config(page_title="XM Strategy Scout", page_icon="🎯", layout="wide")
st.title("🎯 XM Strategy Scout")
st.markdown("Powered by Gemini 2.5 & Google Search Grounding")

# Check for secret
if "GEMINI_API_KEY" in st.secrets:
    gemini_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# Initialize the new Google GenAI Client
client = genai.Client(api_key=gemini_key)

company_name = st.text_input("Enter Company Name:", placeholder="e.g. Delta Airlines")

if st.button("Generate Strategy Report"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner(f"Searching Google for {company_name} insights..."):
            try:
                # The prompt for the research
                prompt_text = f"""
                Research the company '{company_name}' and provide a strategic report.
                
                1. FIND DATA: Search for their most recent Annual Report (10-K), the latest quarterly earnings transcript, and recent news.
                
                2. XM FILTER: Identify exactly TWO major C-Level business problems. 
                   - Ignore logistics, supply chain, or interest rates. 
                   - Focus ONLY on: Customer Experience (churn, digital friction), Employee Experience (attrition, productivity), or Market/Product Innovation (brand perception).
                
                3. EXECUTIVES: List 10-15 current C-Suite and VP/Director level executives at {company_name}.
                
                FORMAT:
                - Use a professional 'Executive Summary' tone.
                - Provide a clear Table for the executives.
                - Use Bold headers and citation links where possible.
                """

                # Run the request using Gemini 2.5 Flash and Google Search tool
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_text,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )

                # Display the result
                st.markdown("---")
                if response.text:
                    st.markdown(response.text)
                    
                    # Optional: Show search suggestions if available
                    if hasattr(response, 'candidates') and response.candidates[0].grounding_metadata:
                        st.caption("Sources found via Google Search Grounding.")
                else:
                    st.error("The model didn't return a text response. Please try again.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.info("Ensure your API key is active in Google AI Studio.")
