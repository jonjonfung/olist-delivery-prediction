import streamlit as st
import boto3
import joblib
import numpy as np
import tempfile
import os

# AWS config
os.environ["AWS_ACCESS_KEY_ID"] = st.secrets["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = st.secrets["AWS_SECRET_ACCESS_KEY"]
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-2"

st.set_page_config(
    page_title="Olist Delivery Predictor",
    page_icon="🚚",
    layout="centered"
)

st.title("🚚 Delivery Time Predictor")
st.markdown("Predict how many days your order will take to deliver")

# Load model from S3
@st.cache_resource
def load_model():
    s3 = boto3.client('s3', region_name='ap-southeast-2')
    with tempfile.TemporaryDirectory() as tmp:
        model_path = os.path.join(tmp, 'delivery_model.pkl')
        encoder_path = os.path.join(tmp, 'label_encoder.pkl')
        s3.download_file('olist-ecommerce-pipeline-john', 'models/delivery_model.pkl', model_path)
        s3.download_file('olist-ecommerce-pipeline-john', 'models/label_encoder.pkl', encoder_path)
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
    return model, encoder

with st.spinner('Loading model from S3...'):
    model, encoder = load_model()

st.success("✅ Model loaded!")

# ---- INPUT FORM ----
st.subheader("Enter Order Details")

col1, col2 = st.columns(2)

with col1:
    customer_state = st.selectbox("Customer State", [
        'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO',
        'ES', 'PE', 'CE', 'PA', 'MT', 'MS', 'RN', 'MA',
        'PB', 'PI', 'AL', 'SE', 'RO', 'TO', 'AM', 'AC',
        'AP', 'RR', 'DF'
    ])
    num_items = st.slider("Number of items", 1, 10, 1)
    total_price = st.number_input("Total price (R$)", 10.0, 5000.0, 100.0)

with col2:
    total_freight = st.number_input("Freight value (R$)", 5.0, 500.0, 20.0)
    purchase_month = st.slider("Purchase month", 1, 12, 6)
    purchase_hour = st.slider("Purchase hour", 0, 23, 12)

purchase_dayofweek = st.selectbox(
    "Day of week",
    [0, 1, 2, 3, 4, 5, 6],
    format_func=lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]
)

# ---- PREDICTION ----
if st.button("🔮 Predict Delivery Time", type="primary"):
    try:
        state_encoded = encoder.transform([customer_state])[0]
        features = np.array([[
            state_encoded,
            num_items,
            total_price,
            total_freight,
            purchase_month,
            purchase_dayofweek,
            purchase_hour
        ]])
        prediction = model.predict(features)[0]

        st.markdown("---")
        st.metric(
            label="Estimated Delivery Time",
            value=f"{round(prediction, 1)} days"
        )

        if prediction <= 7:
            st.success("🟢 Fast delivery!")
        elif prediction <= 14:
            st.warning("🟡 Average delivery time")
        else:
            st.error("🔴 Longer than average delivery")

    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Built by Jonathan Fung | AWS S3 + Scikit-learn + Streamlit")
