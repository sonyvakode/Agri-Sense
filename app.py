import streamlit as st
import json

# ---- Page config ----
st.set_page_config(layout="wide")

# ---- Styles for mobile responsiveness ----
st.markdown("""
<style>
/* Keep main columns side-by-side */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 10px !important;
    }
    [data-testid="column"] {
        min-width: 250px !important;
        flex: 0 0 auto !important;
    }
}

/* Smaller garden grid buttons on mobile */
@media (max-width: 768px) {
    button[kind="secondary"] {
        padding: 4px 6px !important;
        font-size: 0.8rem !important;
        min-width: 40px !important;
    }
}

/* Horizontal scroll for palette section */
@media (max-width: 768px) {
    .palette-scroll {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 6px !important;
    }
    .palette-scroll button {
        flex: 0 0 auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---- Plant palette ----
PLANTS = [
    {"id": "carrot", "label": "Carrot 🥕"},
    {"id": "tomato", "label": "Tomato 🍅"},
    {"id": "lettuce", "label": "Lettuce 🥬"},
    {"id": "pepper", "label": "Pepper 🌶️"},
]

# ---- State initialization ----
if "garden" not in st.session_state:
    st.session_state.garden = {}
if "selected" not in st.session_state:
    st.session_state.selected = None
if "rows" not in st.session_state:
    st.session_state.rows = 4
if "cols" not in st.session_state:
    st.session_state.cols = 4

# ---- Functions ----
def set_selected(pid):
    st.session_state.selected = pid

def toggle_cell(r, c):
    key = f"{r}-{c}"
    if key in st.session_state.garden:
        del st.session_state.garden[key]
    else:
        if st.session_state.selected:
            st.session_state.garden[key] = st.session_state.selected

# ---- Layout ----
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Garden Planner (Visual)")
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("−", key="row_minus") and st.session_state.rows > 1:
            st.session_state.rows -= 1
    with c2:
        if st.button("+", key="row_plus"):
            st.session_state.rows += 1
    st.write("Rows:", st.session_state.rows)

    # Garden grid
    for r in range(st.session_state.rows):
        cols = st.columns(st.session_state.cols)
        for c in range(st.session_state.cols):
            key = f"{r}-{c}"
            label = "−"
            if key in st.session_state.garden:
                pid = st.session_state.garden[key]
                plant = next((p for p in PLANTS if p["id"] == pid), None)
                if plant:
                    label = plant["label"].split()[1]  # emoji only
            cols[c].button(label, key=f"cell-{r}-{c}", on_click=toggle_cell, args=(r, c))

    if st.button("Export layout (JSON)"):
        st.download_button(
            label="Download Garden JSON",
            data=json.dumps(st.session_state.garden),
            file_name="garden.json",
            mime="application/json"
        )

with col2:
    st.subheader("Palette & Tools")
    st.markdown('<div class="palette-scroll">', unsafe_allow_html=True)
    for p in PLANTS:
        st.button(p["label"], key=f"pal-{p['id']}", on_click=set_selected, args=(p["id"],))
    st.markdown('</div>', unsafe_allow_html=True)
