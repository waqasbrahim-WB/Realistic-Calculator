import streamlit as st

st.set_page_config(page_title="Calculator App", page_icon="🧮", layout="centered")

st.title("🧮 Simple Calculator")

# Initialize session state for calculation history and input expression
if "expression" not in st.cookies and "expression" not in st.session_state:
    st.session_state.expression = ""

# Display screen
st.text_input("Display", value=st.session_state.expression, disabled=True, key="display")

# Define button grid layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

# Callback to handle button clicks
def handle_click(char):
    if char == "C":
        st.session_state.expression = ""
    elif char == "=":
        try:
            # Safely evaluate mathematical expressions
            st.session_state.expression = str(eval(st.session_state.expression))
        except Exception:
            st.session_state.expression = "Error"
    else:
        if st.session_state.expression == "Error":
            st.session_state.expression = ""
        st.session_state.expression += char

# Render calculator buttons
for row in buttons:
    cols = st.columns(4)
    for idx, char in enumerate(row):
        cols[idx].button(
            char, 
            use_container_width=True, 
            on_click=handle_click, 
            args=(char,)
        )
