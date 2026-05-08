import streamlit as st

st.set_page_config(
    page_title="Microscope Specimen Calculator",
    page_icon="🔬",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0a0a;
    color: #f0ede6;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
}

.main-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #c8f542;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

.sub-title {
    font-size: 0.95rem;
    color: #666;
    margin-bottom: 2.5rem;
    font-weight: 300;
}

.result-box {
    background: #111;
    border: 1px solid #c8f542;
    border-radius: 4px;
    padding: 2rem;
    margin-top: 1.5rem;
    text-align: center;
}

.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #666;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.result-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    color: #c8f542;
    line-height: 1;
}

.result-unit {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #888;
    margin-top: 0.4rem;
}

.formula-box {
    background: #111;
    border: 1px solid #222;
    border-radius: 4px;
    padding: 1rem 1.5rem;
    margin-top: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #555;
}

.stSelectbox label, .stNumberInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #888 !important;
}

div[data-baseweb="select"] > div {
    background: #111 !important;
    border-color: #333 !important;
    color: #f0ede6 !important;
    border-radius: 4px !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #c8f542 !important;
}

input[type="number"] {
    background: #111 !important;
    border-color: #333 !important;
    color: #f0ede6 !important;
    border-radius: 4px !important;
}

.stButton > button {
    background: #c8f542 !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    background: #d4f75c !important;
    transform: translateY(-1px);
}

.divider {
    border: none;
    border-top: 1px solid #1a1a1a;
    margin: 2rem 0;
}

.tip {
    font-size: 0.8rem;
    color: #444;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

UNITS = {
    "nm": 0.001,
    "µm": 1.0,
    "mm": 1000.0,
    "cm": 10000.0,
    "m": 1000000.0,
}

def calculate(magnification, image_size, image_unit, output_unit):
    size_in_um = image_size * UNITS[image_unit]
    real_um = size_in_um / magnification
    return real_um / UNITS[output_unit]

st.markdown('<div class="main-title">🔬 Specimen Size</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-life size calculator from microscope image data</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    magnification = st.number_input("Magnification power (×)", min_value=1.0, value=400.0, step=10.0)
with col2:
    st.markdown('<p class="tip" style="margin-top:2rem;">e.g. ×100, ×400, ×1000</p>', unsafe_allow_html=True)

col3, col4 = st.columns([2, 1])
with col3:
    image_size = st.number_input("Image specimen size", min_value=0.0001, value=5.0, step=0.1)
with col4:
    image_unit = st.selectbox("Image unit", list(UNITS.keys()), index=3)

output_unit = st.selectbox("Output unit (real-life size)", list(UNITS.keys()), index=1)

if st.button("CALCULATE"):
    if magnification > 0 and image_size > 0:
        result = calculate(magnification, image_size, image_unit, output_unit)

        if result < 0.001:
            display = f"{result:.2e}"
        elif result < 1:
            display = f"{result:.4f}"
        elif result < 1000:
            display = f"{result:.4g}"
        else:
            display = f"{result:,.2f}"

        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Real-life specimen size</div>
            <div class="result-value">{display}</div>
            <div class="result-unit">{output_unit}</div>
        </div>
        <div class="formula-box">
            real size = image size ÷ magnification &nbsp;→&nbsp;
            {image_size} {image_unit} ÷ ×{magnification:.0f} = {display} {output_unit}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please enter valid values greater than zero.")
