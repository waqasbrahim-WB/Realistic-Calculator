import streamlit as st
from google import genai
from google.genai.errors import APIError

# Page setup
st.set_page_config(page_title="AI Smart Calculator", page_icon="🧮", layout="centered")

st.title("🧮 AI Smart Calculator")
st.write("Solve math problems using standard expressions or natural language via Gemini.")

# Sidebar for API Key input
st.sidebar.header("Configuration")
api_key_input = st.sidebar.text_input(
    "Enter Gemini API Key", 
    type="password", 
    help="Get your key from Google AI Studio"
)

# Priority: UI input > Streamlit Secrets
api_key = api_key_input or st.secrets.get("GEMINI_API_KEY", "")

# Initialize Gemini Client if API key is provided
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Failed to initialize client: {e}")

# Navigation tabs
tab1, tab2 = st.tabs(["🧮 Standard Calculator", "🤖 AI Math Solver"])

# TAB 1: Standard Calculator
with tab1:
    if "expression" not in st.session_state:
        st.session_state.expression = ""

    st.text_input("Display", value=st.session_state.expression, disabled=True, key="display")

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    def handle_click(char):
        if char == "C":
            st.session_state.expression = ""
        elif char == "=":
            try:
                # Safely evaluate numeric expressions
                st.session_state.expression = str(eval(st.session_state.expression))
            except Exception:
                st.session_state.expression = "Error"
        else:
            if st.session_state.expression == "Error":
                st.session_state.expression = ""
            st.session_state.expression += char

    for row in buttons:
        cols = st.columns(4)
        for idx, char in enumerate(row):
            cols[idx].button(
                char, 
                use_container_width=True, 
                on_click=handle_click, 
                args=(char,)
            )

# TAB 2: AI Math Solver
with tab2:
    st.subheader("Ask Gemini a Math Problem")
    user_prompt = st.text_area(
        "Enter problem statement or equation:",
        placeholder="e.g., What is the derivative of x^2 + 3x? or Calculate 15% tip on $85."
    )

    if st.button("Solve with AI", type="primary"):
        if not api_key:
            st.error("Please enter a valid Gemini API key in the sidebar or save it in Streamlit Secrets.")
        elif not user_prompt.strip():
            st.warning("Please enter a problem statement.")
        else:
            with st.spinner("Calculating..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"You are a helpful math assistant. Solve this step-by-step concisely: {user_prompt}"
                    )
                    st.markdown("### Solution")
                    st.write(response.text)
                except APIError as e:
                    st.error(f"Gemini API Error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
