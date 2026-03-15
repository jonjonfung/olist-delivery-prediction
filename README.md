# 🚚 Olist Delivery Time Predictor

A machine learning pipeline that predicts e-commerce delivery times using AWS and Scikit-learn.

## 🌐 Live Demo
👉 [Try the Live App](your_streamlit_url_here)

## 📸 App Preview

![App](your_screenshot_url_here)

## 🏗️ Architecture
```
Athena (silver layer)
  → Feature Engineering (Pandas)
    → Random Forest Model (Scikit-learn)
      → S3 (model storage)
        → Streamlit (live predictions)
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Source | AWS Athena (silver layer) |
| Feature Engineering | Pandas + Python |
| ML Model | Scikit-learn Random Forest |
| Model Storage | AWS S3 |
| Frontend | Streamlit |

## 📊 Model Performance

| Metric | Score |
|---|---|
| Mean Absolute Error | 4.82 days |
| R2 Score | 0.329 |
| Training samples | 76,935 |
| Test samples | 19,234 |

## 🔍 Feature Importance

| Feature | Importance |
|---|---|
| Customer state | 49.1% |
| Purchase month | 20.4% |
| Freight value | 19.8% |
| Total price | 4.8% |
| Purchase hour | 2.4% |
| Number of items | 1.8% |
| Day of week | 1.6% |

## 💡 Key Insights
- Customer location accounts for **49% of delivery time variance**
- Geographic distance (measured via freight value) is the second strongest predictor
- Seasonality (purchase month) significantly impacts delivery speed
- Rural states like AM and RR have significantly longer delivery times than SP

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

### Train the model
Open `notebooks/train_model.ipynb` in Google Colab and run all cells.

### Run the dashboard locally
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 📦 Dataset
[Brazilian E-Commerce Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

This project uses the cleaned silver layer from the
[Olist E-Commerce Pipeline](https://github.com/yourname/olist-ecommerce-pipeline) project.
