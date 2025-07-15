import streamlit as st
import pandas as pd
import requests

# -------------------- Page Setup --------------------
st.set_page_config(page_title="🎯 CSAT Score Predictor", layout="centered")
st.title("📊 CSAT Score Predictor")

# -------------------- Load Options --------------------
@st.cache_data
def load_options():
    df = pd.read_csv("data/Preprocessed Data/Customer.csv")
    return {
        'channel_name': df['channel_name'].dropna().unique().tolist(),
        'category': df['category'].dropna().unique().tolist(),
        'Sub-category': df['Sub-category'].dropna().unique().tolist(),
        'Customer Remarks': df['Customer Remarks'].dropna().unique().tolist(),
        'Customer_City': df['Customer_City'].dropna().unique().tolist(),
        'Product_category': df['Product_category'].dropna().unique().tolist(),
        'Tenure Bucket': df['Tenure Bucket'].dropna().unique().tolist(),
        'Agent Shift': df['Agent Shift'].dropna().unique().tolist(),
        'Issue_reported_day_Name': df['Issue_reported_day_Name'].dropna().unique().tolist(),
        'Issue_reported_month': sorted(set(str(x) for x in df['Issue_reported_month'].dropna().unique())),
        'Survey_response_Day_Name': df['Survey_response_Day_Name'].dropna().unique().tolist(),
        'Survey_response_Date_month': sorted(set(str(x) for x in df['Survey_response_Date_month'].dropna().unique())),
        'Agent Experience Level': df['Agent Experience Level'].dropna().unique().tolist(),
        'Handling Bucket': df['Handling Bucket'].dropna().unique().tolist()
    }

options = load_options()

# -------------------- Sidebar Instructions --------------------
with st.sidebar:
    st.header("🔎 Instructions")
    st.markdown("""
    - Fill in customer and issue details below.
    - Click **Predict** to get the CSAT Score.
    - Use sliders for time fields (0–1440 min).
    - CSAT Score: 1 (Very Dissatisfied) to 5 (Very Satisfied).
    """)

# -------------------- Prediction Function --------------------
def get_prediction(input_dict):
    url = "http://127.0.0.1:8000/predict"  # Make sure this matches your FastAPI service

    try:
        response = requests.post(url, json=input_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# -------------------- Input Form --------------------
with st.form("csat_form"):
    st.subheader("📝 Customer Interaction Details")

    col1, col2 = st.columns(2)
    with col1:
        channel = st.selectbox("Channel Name", options['channel_name'])
        category = st.selectbox("Category", options['category'])
        sub_category = st.selectbox("Sub-category", options['Sub-category'])
        remarks = st.selectbox("Customer Remarks", options['Customer Remarks'])
        city = st.selectbox("Customer City", options['Customer_City'])
        product = st.selectbox("Product Category", options['Product_category'])
        tenure = st.selectbox("Tenure Bucket", options['Tenure Bucket'])

    with col2:
        shift = st.selectbox("Agent Shift", options['Agent Shift'])
        issue_day = st.selectbox("Issue Reported Day", options['Issue_reported_day_Name'])
        issue_month = st.selectbox("Issue Reported Month", options['Issue_reported_month'])
        survey_day = st.selectbox("Survey Response Day", options['Survey_response_Day_Name'])
        survey_month = st.selectbox("Survey Response Month", options['Survey_response_Date_month'])
        agent_exp = st.selectbox("Agent Experience Level", options['Agent Experience Level'])
        handle_bucket = st.selectbox("Handling Bucket", options['Handling Bucket'])

    st.subheader("⏱️ Time Metrics (in minutes)")
    issue_time = st.slider("Issue Reported Time", 0, 1440, 30)
    response_time = st.slider("Response Time", 0, 1440, 45)
    handling_time = st.slider("Handling Time", 0, 1440, 60)

    submit = st.form_submit_button("🚀 Predict CSAT Score")

# -------------------- Prediction Execution --------------------
if submit:
    input_dict = {
        "channel_name": channel,
        "category": category,
        "sub_category": sub_category,
        "remarks": remarks,
        "city": city,
        "product": product,
        "tenure": tenure,
        "shift": shift,
        "issue_reported_day": issue_day,
        "issue_reported_month": issue_month,
        "survey_response_day": survey_day,
        "survey_response_month": survey_month,
        "issue_time": int(issue_time),
        "response_time": int(response_time),
        "handling_time": int(handling_time),
        "agent_experience": agent_exp,
        "handle_bucket": handle_bucket
    }


    with st.spinner("⏳ Predicting CSAT score..."):
        result = get_prediction(input_dict)

    if "error" in result:
        st.error(f"❌ Prediction failed: {result['error']}")
    else:
        st.success("✅ Prediction successful!")
        st.metric(label="🎯 Predicted CSAT Score", value=result['satisfaction_prediction'])
        st.info(f"😊 Customer is likely: **{result['mood']}**")

        if "probabilities" in result and result["probabilities"]:
            st.subheader("🔍 Prediction Probabilities")
            st.json(result["probabilities"])
