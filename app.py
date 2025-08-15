import streamlit as st
from utils import make_empty_grid, analyze_image, rule_based_reply, save_layout_json
import os

st.set_page_config(page_title='Agri-Sense', layout='wide', initial_sidebar_state='expanded',page_icon='🌿')

# --- Sidebar ---
st.sidebar.title("Agri‑Sense 🌱")
st.sidebar.markdown("Dual‑Mode Agri Assistant — Urban & Rural")
mode = st.sidebar.radio("Choose mode", ("Urban Mode", "Rural Mode"))

st.sidebar.markdown('---')
st.sidebar.subheader("Design")
theme = st.sidebar.selectbox("Theme", ["Fresh Green", "Earthy Beige", "Soft Monochrome"])
st.sidebar.caption("Tip: Use Upload to get plant/pest hints in Urban mode.")

# --- Theme colors dictionary (light, attractive) ---
theme_colors = {
    "Fresh Green": {
        "background": "#F0FFF4",
        "header": "#2E7D32",
        "button": "#66BB6A",
        "text": "#1B5E20"
    },
    "Earthy Beige": {
        "background": "#FFF8E1",
        "header": "#8D6E63",
        "button": "#A1887F",
        "text": "#5D4037"
    },
    "Soft Monochrome": {
        "background": "#FAFAFA",
        "header": "#424242",
        "button": "#9E9E9E",
        "text": "#212121"
    }
}

# --- Apply selected theme ---
colors = theme_colors[theme]

st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {colors['background']};
    }}
    h1, h2, h3 {{
        color: {colors['header']};
    }}
    .stButton>button {{
        background-color: {colors['button']};
        color: white;
    }}
    .stText, .stMarkdown {{
        color: {colors['text']};
    }}
    </style>
""", unsafe_allow_html=True)

# --- Session state init ---
if 'rows' not in st.session_state:
    st.session_state.rows = 4
if 'cols' not in st.session_state:
    st.session_state.cols = 4
if 'grid' not in st.session_state:
    st.session_state.grid = make_empty_grid(st.session_state.rows, st.session_state.cols)
if 'selected' not in st.session_state:
    st.session_state.selected = 'tomato'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Plant palette
PLANTS = [
    {"id":"tomato","label":"Tomato","emoji":"🍅"},
    {"id":"basil","label":"Basil","emoji":"🌿"},
    {"id":"marigold","label":"Marigold","emoji":"🌼"},
    {"id":"potato","label":"Potato","emoji":"🥔"},
    {"id":"empty","label":"Remove","emoji":"✖️"},
]

def set_selected(pid):
    st.session_state.selected = pid

# --- Layout ---
st.title("Agri‑Sense")
st.markdown("A simple, attractive dual‑mode assistant for urban gardeners and rural farmers.")

if mode == "Urban Mode":
    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader("Garden Planner (Visual)")
        cols_input, rows_input = st.columns(2)
        with cols_input:
            c = st.number_input("Columns", min_value=1, max_value=12, value=st.session_state.cols, key='cols_input')
        with rows_input:
            r = st.number_input("Rows", min_value=1, max_value=12, value=st.session_state.rows, key='rows_input')

        if r != st.session_state.rows or c != st.session_state.cols:
            st.session_state.rows = r
            st.session_state.cols = c
            st.session_state.grid = make_empty_grid(r, c)

        st.markdown("**Tap a cell to plant / remove.**")
        grid = st.session_state.grid
        for i in range(st.session_state.rows):
            cols = st.columns(st.session_state.cols)
            for j in range(st.session_state.cols):
                cell = grid[i][j]
                label = cell.get('plant') or '—'
                btn_label = label if label == '—' else next((p['emoji'] for p in PLANTS if p['id']==label), label)
                if cols[j].button(btn_label, key=f"cell-{i}-{j}"):
                    if st.session_state.selected == 'empty':
                        st.session_state.grid[i][j] = {'plant': None}
                    else:
                        st.session_state.grid[i][j] = {'plant': st.session_state.selected}
                    st.rerun()

        st.divider()
        st.download_button("Export layout (JSON)", data=save_layout_json(st.session_state.grid), file_name="garden-layout.json", mime="application/json")

    with col2:
        st.subheader("Palette & Tools")
        for p in PLANTS:
            if st.button(f"{p['emoji']}  {p['label']}", key=f"pal-{p['id']}", on_click=set_selected, args=(p['id'],)):
                pass
        st.markdown(f"**Selected:** {st.session_state.selected}")

        st.markdown('---')
        st.subheader("Identify (Image)")
        uploaded = st.file_uploader("Upload leaf / pest photo", type=['png','jpg','jpeg'])
        if uploaded:
            with st.spinner("Analyzing image..."):
                result = analyze_image(uploaded)
                st.success("Analysis ready")
                st.info(result)
else:
    # Rural Mode
    left, right = st.columns([1,2])
    with left:
        st.subheader("Toolkit")
        if st.button("Pest Solutions"):
            st.session_state.chat_messages = [{'role':'user','text': 'Pest issue: describe symptoms'}]
        if st.button("Fertilizer Advice"):
            st.session_state.chat_messages = [{'role':'user','text': 'Fertilizer schedule for small farm'}]
        if st.button("Seasonal Crops"):
            st.session_state.chat_messages = [{'role':'user','text': 'Best crops for this season'}]
        st.divider()
        st.subheader("Quick Tips")
        tips = ["Water early morning","Use neem spray for leaf pests","Rotate crops yearly"]
        st.info(tips[0])

    with right:
        st.subheader("AI Chat — Rural Toolkit")
        for msg in st.session_state.chat_messages:
            if msg['role']=='user':
                st.markdown(f"**You:** {msg['text']}")
            else:
                st.markdown(f"**Agri‑Sense:** {msg['text']}")
        prompt = st.text_input("Ask a question", key='chat_input')
        if st.button("Send"):
            if prompt:
                st.session_state.chat_messages.append({'role':'user','text':prompt})
                with st.spinner('Thinking...'):
                    reply = rule_based_reply(prompt)  # Offline response
                    st.session_state.chat_messages.append({'role':'assistant','text':reply})
                    st.rerun()

st.markdown('---')

