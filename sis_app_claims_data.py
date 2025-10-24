import _snowflake
import json
import streamlit as st
import time
from snowflake.snowpark.context import get_active_session

# Aetna color scheme
AETNA_PURPLE = "#7B2CBF"
AETNA_LIGHT_PURPLE = "#A663CC"
AETNA_DARK_PURPLE = "#5A1A96"
AETNA_GRAY = "#F8F9FA"
AETNA_DARK_GRAY = "#6C757D"
AETNA_WHITE = "#FFFFFF"

DATABASE = "SYNTHEA"
SCHEMA = "SYNTHEA"
STAGE = "SYNTHEA"
#FILE = "CollegeDS_CortexAnalystHOL.yaml"

# Page configuration
st.set_page_config(
    page_title="Aetna Claims Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Aetna branding
def load_aetna_css():
    st.markdown(f"""
    <style>
    /* Import Aetna-like font */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
    
    /* Main app styling */
    .main {{
        background-color: {AETNA_WHITE};
        font-family: 'Source Sans Pro', sans-serif;
    }}
    
    /* Header styling */
    .aetna-header {{
        background: linear-gradient(135deg, {AETNA_PURPLE} 0%, {AETNA_LIGHT_PURPLE} 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(123, 44, 191, 0.3);
        text-align: center;
    }}
    
    .aetna-logo {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: {AETNA_WHITE};
        text-decoration: none;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
        display: block;
    }}
    
    .aetna-title {{
        color: {AETNA_WHITE};
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .aetna-subtitle {{
        color: {AETNA_WHITE};
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }}
    
    /* Chat styling */
    .stChatMessage {{
        background-color: {AETNA_GRAY};
        border-radius: 10px;
        border-left: 4px solid {AETNA_PURPLE};
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    
    .stChatMessage[data-testid="chat-message-user"] {{
        background-color: {AETNA_LIGHT_PURPLE};
        border-left: 4px solid {AETNA_PURPLE};
    }}
    
    .stChatMessage[data-testid="chat-message-user"] .stMarkdown p {{
        color: {AETNA_WHITE};
        font-weight: 500;
    }}
    
    .stChatMessage[data-testid="chat-message-assistant"] {{
        background-color: {AETNA_WHITE};
        border-left: 4px solid {AETNA_PURPLE};
        border: 1px solid #E9ECEF;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {AETNA_PURPLE};
        color: {AETNA_WHITE};
        border: none;
        border-radius: 8px;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(123, 44, 191, 0.2);
    }}
    
    .stButton > button:hover {{
        background-color: {AETNA_DARK_PURPLE};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(123, 44, 191, 0.3);
    }}
    
    /* Chat input styling */
    .stChatInput > div > div > input {{
        border: 2px solid {AETNA_PURPLE};
        border-radius: 25px;
        padding: 0.75rem 1rem;
        font-family: 'Source Sans Pro', sans-serif;
        background-color: {AETNA_WHITE};
    }}
    
    .stChatInput > div > div > input:focus {{
        border-color: {AETNA_DARK_PURPLE};
        box-shadow: 0 0 0 3px rgba(123, 44, 191, 0.1);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: {AETNA_GRAY};
        border: 1px solid {AETNA_PURPLE};
        border-radius: 8px;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        color: {AETNA_PURPLE};
    }}
    
    .streamlit-expanderContent {{
        background-color: {AETNA_WHITE};
        border: 1px solid #E9ECEF;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }}
    
    /* Tab styling */
    .stTabs > div > div > div > div {{
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 600;
        color: {AETNA_PURPLE};
    }}
    
    .stTabs > div > div > div > div[data-baseweb="tab-highlight"] {{
        background-color: {AETNA_PURPLE};
    }}
    
    /* Code block styling */
    .stCodeBlock {{
        background-color: {AETNA_GRAY};
        border-left: 4px solid {AETNA_PURPLE};
        border-radius: 5px;
    }}
    
    /* Info box styling */
    .info-container {{
        background: linear-gradient(135deg, {AETNA_GRAY} 0%, {AETNA_WHITE} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {AETNA_PURPLE};
        margin: 1.5rem 0;
        box-shadow: 0 3px 6px rgba(0,0,0,0.08);
    }}
    
    .info-container h3 {{
        color: {AETNA_PURPLE};
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
    }}
    
    .info-container p {{
        color: {AETNA_DARK_GRAY};
        font-family: 'Source Sans Pro', sans-serif;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }}
    
    .example-question {{
        background-color: {AETNA_WHITE};
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 3px solid {AETNA_LIGHT_PURPLE};
        margin: 0.5rem 0;
        font-family: 'Source Sans Pro', sans-serif;
        color: {AETNA_DARK_GRAY};
        font-style: italic;
    }}
    
    /* Spinner styling */
    .stSpinner {{
        color: {AETNA_PURPLE};
    }}
    
    /* Dataframe styling */
    .dataframe {{
        border: 1px solid {AETNA_PURPLE};
        border-radius: 8px;
    }}
    
    /* Chart styling */
    .stPlotlyChart {{
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    </style>
    """, unsafe_allow_html=True)

def create_aetna_header():
    """Create the Aetna branded header"""
    st.markdown(f"""
    <div class="aetna-header">
        <div class="aetna-logo">aetna</div>
        <h1 class="aetna-title">Claims Intelligence Portal</h1>
        <p class="aetna-subtitle">AI-Powered Healthcare Data Analytics with Snowflake Cortex</p>
    </div>
    """, unsafe_allow_html=True)

def send_message(prompt: str) -> dict:
    """Calls the REST API and returns the response."""
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
#        "semantic_model_file": f"@{DATABASE}.{SCHEMA}.{STAGE}/{FILE}",
        "semantic_view": "SYNTHEA.SYNTHEA.SYNTHEA_HEALTHCARE",
    }
    resp = _snowflake.send_snow_api_request(
        "POST",
        f"/api/v2/cortex/analyst/message",
        {},
        {},
        request_body,
        {},
        30000,
    )
    if resp["status"] < 400:
        return json.loads(resp["content"])
    else:
        raise Exception(
            f"Failed request with status {resp['status']}: {resp}"
        )

def process_message(prompt: str) -> None:
    """Processes a message and adds the response to the chat."""
    st.session_state.messages.append(
        {"role": "user", "content": [{"type": "text", "text": prompt}]}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing your request..."):
            response = send_message(prompt=prompt)
            content = response["message"]["content"]
            display_content(content=content)
    st.session_state.messages.append({"role": "assistant", "content": content})

def display_content(content: list, message_index: int = None) -> None:
    """Displays a content item for a message."""
    message_index = message_index or len(st.session_state.messages)
    for item in content:
        if item["type"] == "text":
            st.markdown(item["text"])
        elif item["type"] == "suggestions":
            with st.expander("💡 Suggested Follow-up Questions", expanded=True):
                for suggestion_index, suggestion in enumerate(item["suggestions"]):
                    if st.button(suggestion, key=f"{message_index}_{suggestion_index}"):
                        st.session_state.active_suggestion = suggestion
        elif item["type"] == "sql":
            with st.expander("🔧 SQL Query", expanded=False):
                st.code(item["statement"], language="sql")
            with st.expander("📊 Analysis Results", expanded=True):
                with st.spinner("🏃‍♂️ Executing query..."):
                    session = get_active_session()
                    df = session.sql(item["statement"]).to_pandas()
                    if len(df.index) > 1:
                        data_tab, line_tab, bar_tab = st.tabs(
                            ["📋 Data Table", "📈 Line Chart", "📊 Bar Chart"]
                        )
                        data_tab.dataframe(df, use_container_width=True)
                        if len(df.columns) > 1:
                            df_chart = df.set_index(df.columns[0])
                        else:
                            df_chart = df
                        with line_tab:
                            try:
                                st.line_chart(df_chart, use_container_width=True)
                            except Exception as e:
                                st.warning("⚠️ Cannot be graphed as a line chart")
                        with bar_tab:
                            try:
                                st.bar_chart(df_chart, use_container_width=True)
                            except Exception as e:
                                st.warning("⚠️ Cannot be graphed as a bar chart")
                    else:
                        st.dataframe(df, use_container_width=True)

def main():
    # Load Aetna CSS
    load_aetna_css()
    
    # Create header
    create_aetna_header()
    
    # Information section
    st.markdown("""
    <div class="info-container">
        <h3>🏥 Healthcare Data Intelligence</h3>
        <p><strong>Ask questions about your healthcare data and get instant insights powered by AI.</strong></p>
        <p>Our Cortex Analyst can help you explore:</p>
        <p>🔹 <strong>Claims Analysis</strong> - Processing patterns, costs, and trends</p>
        <p>🔹 <strong>Patient Insights</strong> - Demographics, diagnoses, and outcomes</p>
        <p>🔹 <strong>Provider Analytics</strong> - Performance metrics and patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Example questions
    st.markdown("""
    <div class="info-container">
        <h3>💭 Example Questions to Get Started</h3>
        <div class="example-question">
            "What is the total number of claims processed by city in the year 2024?"
        </div>
        <div class="example-question">
            "How many patients in Boston have a diagnosis description with 'heart' in it?"
        </div>
        <div class="example-question">
            "Show me the top 5 most expensive claim types by average cost"
        </div>
        <div class="example-question">
            "What are the monthly trends for emergency room visits?"
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.suggestions = []
        st.session_state.active_suggestion = None
    
    # Display chat history
    for message_index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            display_content(content=message["content"], message_index=message_index)
    
    # Chat input
    if user_input := st.chat_input("🔍 Ask your healthcare data question here..."):
        process_message(prompt=user_input)
    
    # Process active suggestion
    if st.session_state.active_suggestion:
        process_message(prompt=st.session_state.active_suggestion)
        st.session_state.active_suggestion = None
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: {AETNA_DARK_GRAY}; font-family: 'Source Sans Pro', sans-serif; margin-top: 2rem;">
            <p>🏥 <strong>Aetna Claims Intelligence Portal</strong> | Powered by Snowflake Cortex AI</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Transforming healthcare data into actionable insights</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

