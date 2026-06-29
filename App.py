import streamlit as st
import pandas as pd
import pickle as pkl
import os

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Car Price Prediction App",
    page_icon="🚗",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================
st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #2d3748;
}

.sub-title {
    text-align: center;
    font-size: 22px;
    color: gray;
    margin-bottom: 30px;
}

.block-container {
    padding-top: 2rem;
}

div[data-testid="stButton"] button {
    width: 100%;
    height: 55px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
}

.result-box {
    background-color: #d1fae5;
    color: #065f46;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-top: 20px;
}

.about-box {
    background-color: #dbeafe;
    padding: 20px;
    border-radius: 12px;
}

hr {
    margin-top: 25px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# SIDEBAR
# ==================================
with st.sidebar:

    st.markdown("## 📊 About")

    st.markdown("""
    <div class="about-box">

    This application predicts the resale value of a used car using a
    Machine Learning model.

    <br>

    <b>Features Used:</b>

    - Company
    - Car Name
    - Year
    - Kilometers Driven
    - Fuel Type

    </div>
    """, unsafe_allow_html=True)

# ==================================
# LOAD DATA
# ==================================
df = pd.read_csv("final.csv")

# ==================================
# LOAD MODEL
# ==================================
model_path = "model.pkl"

with open(model_path, "rb") as f:
    model = pkl.load(f)

# ==================================
# TITLE
# ==================================
st.markdown(
    '<div class="main-title">🚗 Car Price Prediction App</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Predict the resale value of your car instantly</div>',
    unsafe_allow_html=True
)

st.divider()

# ==================================
# FORM
# ==================================
col1, col2 = st.columns(2)

with col1:

    companies = sorted(df["company"].unique())

    company = st.selectbox(
        "🏢 Select Company",
        companies
    )

    names = sorted(
        df[df["company"] == company]["name"].unique()
    )

    name = st.selectbox(
        "🚘 Select Car Name",
        names
    )

    fuel_types = sorted(
        df["fuel_type"].dropna().unique()
    )

    fuel_type = st.selectbox(
        "⛽ Select Fuel Type",
        fuel_types
    )

with col2:

    year = st.number_input(
        "📅 Manufacturing Year",
        min_value=1995,
        max_value=2026,
        value=2015
    )

    kms_driven = st.number_input(
        "🛣️ Kilometers Driven",
        min_value=0,
        max_value=500000,
        value=50000
    )

st.divider()

# ==================================
# PREDICT BUTTON
# ==================================
if st.button("🔍 Predict Price"):

    try:

        myinput = pd.DataFrame(
            [[company, name, year, kms_driven, fuel_type]],
            columns=[
                "company",
                "name",
                "year",
                "kms_driven",
                "fuel_type"
            ]
        )

        prediction = model.predict(myinput)

        predicted_price = float(prediction[0][0])

        st.markdown(
            f"""
            <div class="result-box">
                💰 Estimated Price <br>
                ₹ {predicted_price:,.0f}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")

# python -m streamlit run App.py