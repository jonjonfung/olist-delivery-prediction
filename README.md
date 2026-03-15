# 🚚 Olist Delivery Time Predictor

[![Run Tests](https://github.com/jonjonfung/olist-delivery-prediction/actions/workflows/test.yml/badge.svg)](https://github.com/jonjonfung/olist-delivery-prediction/actions/workflows/test.yml)
[![Deploy ML Pipeline](https://github.com/jonjonfung/olist-delivery-prediction/actions/workflows/deploy.yml/badge.svg)](https://github.com/jonjonfung/olist-delivery-prediction/actions/workflows/deploy.yml)

A machine learning pipeline that predicts e-commerce delivery times for Brazilian orders.
Built using AWS Athena for data retrieval, Scikit-learn for model training, and Streamlit
for live predictions. This project is the second part of the
[Olist E-Commerce Pipeline](https://github.com/jonjonfung/olist-ecommerce-pipeline) project
and consumes the cleaned silver layer produced by that pipeline.

## 🌐 Live Demo
👉 [Try the Live App](https://olist-delivery-prediction-bulkpjycmxq7mtulcq2dre.streamlit.app/)

Enter your order details — customer state, number of items, price, freight value and 
purchase time — and instantly get a predicted delivery time in days with a traffic light 
indicator showing whether it's fast, average or slow.

## 📸 App Preview
![Image](https://github.com/user-attachments/assets/d8dd53cd-d0e9-4b81-a465-2b0c419c9f2f)

## 🏗️ Architecture
```
AWS Athena (silver layer — 96,469 rows)
  → Feature Engineering (Pandas)
    → Train/Test Split (80/20)
      → Random Forest Regressor (Scikit-learn)
        → Trained Model saved to AWS S3
          → Streamlit loads model from S3
            → Live predictions in browser
```

The pipeline starts by querying **96,469 delivered orders** from the cleaned silver layer
in AWS Athena. Features are engineered from order timestamps, customer location, pricing,
and freight data. A Random Forest Regressor is trained on 80% of the data and evaluated
on the remaining 20%. The trained model is saved to S3 as a `.pkl` file, then loaded
at runtime by the Streamlit app to serve live predictions without retraining.

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Data Source | AWS Athena | Query cleaned silver layer |
| Data Processing | Pandas + Python | Feature engineering |
| ML Model | Scikit-learn Random Forest | Predict delivery days |
| Model Storage | AWS S3 | Store and load trained model |
| Frontend | Streamlit | Live prediction interface |
| Notebook | Google Colab | Model training environment |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Secrets | Google Colab Secrets + Streamlit Secrets | Secure credential management |

## 📊 Model Performance

| Metric | Score | What it means |
|---|---|---|
| Mean Absolute Error | 4.82 days | Predictions are off by ~5 days on average |
| R2 Score | 0.329 | Model explains 33% of delivery time variance |
| Training samples | 76,935 | 80% of cleaned dataset |
| Test samples | 19,234 | 20% held out for honest evaluation |
| Target variable range | 1 - 60 days | Outliers above 60 days removed |

The R2 score of 0.329 is reasonable given the features available in this dataset.
Key drivers like carrier performance, exact road distance, warehouse location and
weather are not captured here — with those features the model would likely achieve
0.6-0.8. This is acknowledged as a future improvement opportunity.

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

Feature importance was extracted from the trained Random Forest model using
`model.feature_importances_` — showing which inputs the model relied on most
when making predictions across all 76,935 training samples.

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
- Freight value and customer state together account for **~69% of all variance** —
  suggesting a distance based feature would be the single biggest model improvement

## ⚙️ CI/CD Pipeline

This project uses **GitHub Actions** for automated testing and deployment:

| Workflow | Trigger | What it does |
|---|---|---|
| `test.yml` | Every push to any branch | Installs dependencies, tests imports, lints code |
| `deploy.yml` | Push to main branch only | Verifies model loads from S3, confirms deployment |

This ensures every code change is automatically validated before reaching production,
mimicking real world CI/CD practices used in data engineering teams.

## 📁 Project Structure
```
├── .github/
│   └── workflows/
│       ├── test.yml         # Runs on every branch push
│       └── deploy.yml       # Runs on main branch push
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
2. Add your AWS credentials to **Colab Secrets** (key icon in left sidebar):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
3. Run all cells — model saves automatically to S3 at `models/delivery_model.pkl`

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

### Run GitHub Actions locally (optional)
```bash
pip install act
act push
```

## 📦 Dataset
[Brazilian E-Commerce Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

- 100k+ orders from 2016 to 2018 across Brazil
- 9 CSV files covering orders, customers, products, sellers and reviews
- This project uses the **cleaned silver layer** from the Olist E-Commerce Pipeline
- Only delivered orders with valid timestamps are used for training (96,469 rows)
- Outliers above 60 delivery days removed to improve model stability

## 🔮 Future Improvements
- Add seller location as a feature for better distance estimation
- Experiment with **XGBoost or LightGBM** for improved R2 score
- Deploy model serving via **AWS Lambda with Docker container** for serverless predictions
- Add **confidence intervals** to predictions to communicate uncertainty
- Automate model retraining via **Apache Airflow** when new data arrives
- Add **data drift detection** to monitor when model performance degrades
- Expand to predict delivery time by **product category**

## 🔗 Related Project
This project is part of a two-part portfolio:
- 📦 [Olist E-Commerce Pipeline](https://github.com/jonjonfung/olist-ecommerce-pipeline) — AWS S3, Glue, Athena, Streamlit dashboard
- 🚚 **Olist Delivery Predictor** (this project) — ML model, S3, Streamlit, GitHub Actions
