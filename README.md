# 🚚 Olist Delivery Time Predictor

A machine learning pipeline that predicts e-commerce delivery times for Brazilian orders. 
Built using AWS Athena for data retrieval, Scikit-learn for model training, and Streamlit 
for live predictions. This project is the second part of the 
[Olist E-Commerce Pipeline](https://github.com/jonjonfung/olist-ecommerce-pipeline) project.

## 🌐 Live Demo
👉 [Try the Live App](https://olist-delivery-prediction-bulkpjycmxq7mtulcq2dre.streamlit.app/)

Enter your order details and instantly get a predicted delivery time in days!

## 📸 App Preview
![Image](https://github.com/user-attachments/assets/d8dd53cd-d0e9-4b81-a465-2b0c419c9f2f)

## 🏗️ Architecture
```
Athena (silver layer)
  → Feature Engineering (Pandas)
    → Random Forest Model (Scikit-learn)
      → S3 (model storage)
        → Streamlit (live predictions)
```

The pipeline starts by querying **96,469 delivered orders** from the cleaned silver layer 
in AWS Athena. Features are engineered from order timestamps, customer location, pricing, 
and freight data. A Random Forest Regressor is trained and saved to S3, then loaded 
at runtime by the Streamlit app to serve live predictions.

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Data Source | AWS Athena | Query cleaned silver layer |
| Data Processing | Pandas + Python | Feature engineering |
| ML Model | Scikit-learn Random Forest | Predict delivery days |
| Model Storage | AWS S3 | Store and load trained model |
| Frontend | Streamlit | Live prediction interface |
| Notebook | Google Colab | Model training environment |

## 📊 Model Performance

| Metric | Score | What it means |
|---|---|---|
| Mean Absolute Error | 4.82 days | Predictions are off by ~5 days on average |
| R2 Score | 0.329 | Model explains 33% of delivery time variance |
| Training samples | 76,935 | 80% of cleaned dataset |
| Test samples | 19,234 | 20% held out for evaluation |

The R2 score of 0.329 is reasonable given the available features. Key drivers like 
carrier performance, road distance, and warehouse location are not available in this 
dataset — with those features the model would likely achieve 0.6-0.8.

## 🔍 Feature Importance

| Feature | Importance | Why it matters |
|---|---|---|
| Customer state | 49.1% | Location determines shipping distance |
| Purchase month | 20.4% | Seasonality affects carrier capacity |
| Freight value | 19.8% | Higher freight = longer distance |
| Total price | 4.8% | Higher value items may need special handling |
| Purchase hour | 2.4% | Late orders may miss same-day dispatch |
| Number of items | 1.8% | More items = longer packing time |
| Day of week | 1.6% | Weekend orders may be delayed |

## 💡 Key Insights

- Customer location accounts for **49% of delivery time variance** — where you live 
  is the single biggest factor in how fast your order arrives
- Geographic distance (measured via freight value) is the **second strongest predictor** 
  at 19.8% — confirming that shipping distance directly drives delivery time
- **Seasonality matters** — purchase month accounts for 20% of variance, suggesting 
  holiday periods and peak seasons significantly slow down deliveries
- Rural states like **AM (Amazonas) and RR (Roraima)** have significantly longer 
  delivery times than urban states like **SP (São Paulo)** due to geographic isolation
- Orders placed **late at night** tend to take slightly longer as they may miss 
  same-day warehouse processing

## 📁 Project Structure
```
├── notebooks/
│   └── train_model.ipynb    # Data pull, feature engineering, model training
├── dashboard/
│   └── app.py               # Streamlit prediction app
├── requirements.txt
└── README.md
```

## 🚀 How to Run

### Prerequisites
- AWS account with Athena and S3 access
- Olist silver layer tables set up (see [Pipeline project](https://github.com/jonjonfung/olist-ecommerce-pipeline))

### Train the model
1. Open `notebooks/train_model.ipynb` in Google Colab
2. Add your AWS credentials to Colab Secrets
3. Run all cells — model saves automatically to S3

### Run the dashboard locally
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Add your AWS credentials to `.streamlit/secrets.toml`:
```toml
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
```

## 📦 Dataset
[Brazilian E-Commerce Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

- 100k+ orders from 2016 to 2018
- This project uses the **cleaned silver layer** from the Olist E-Commerce Pipeline
- Only delivered orders with valid timestamps are used for training (96,469 rows)

## 🔮 Future Improvements
- Add seller location as a feature for better distance estimation
- Experiment with XGBoost or LightGBM for improved R2 score
- Deploy model serving via AWS Lambda with Docker container
- Add confidence intervals to predictions
- Retrain model automatically when new data arrives via Airflow
