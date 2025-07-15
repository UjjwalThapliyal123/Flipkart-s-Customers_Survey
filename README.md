# FlipSatisfy: Customer Satisfaction Prediction for Flipkart Support Interactions

![FlipSatisfy Logo](https://img.shields.io/badge/ML-Customer%20Satisfaction-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Project Overview

**FlipSatisfy** is a machine learning project focused on predicting customer satisfaction levels from historical Flipkart support interaction data. This classification model helps transform support feedback into actionable insights and improve overall customer experience.

> **Objective:** Build and deploy a binary classification model to predict whether a customer is **Satisfied (1)** or **Dissatisfied (0)** based on support interaction metadata and feedback.

---

## 📊 Business Use Cases

* 🔀 **Feedback Routing**: Prioritize dissatisfied customers for faster resolution.
* 📈 **Support Analytics**: Monitor satisfaction trends across teams and channels.
* ⚠️ **Proactive Support**: Detect dissatisfaction early to trigger escalations.
* 🧑‍💼 **Agent Evaluation**: Use CSAT predictions as agent performance metrics.
* 🔗 **CRM Integration**: Feed predictions into CRM systems for personalized support.

---

## 🔁 Project Workflow

### 1. Data Understanding & Exploration

* Load dataset with support interactions and CSAT scores.
* Analyze class imbalance, channel distributions, and feedback examples.

### 2. Data Preprocessing

* Handle missing values, duplicates, and outliers.
* Standardize/normalize numerical features.

### 3. Feature Engineering

* Encode categorical fields (e.g., channel, shift, product).
* Extract sentiment from feedback (optional).
* Label encode satisfaction as 0/1.

### 4. Model Building & Evaluation

Models Trained:

* Decision Tree
* Random Forest
* K-Nearest Neighbors
* Histogram-based Gradient Boosting
* AdaBoost Classifier

**Metrics Used**:

* Accuracy
* Precision, Recall, F1-score
* Confusion Matrix
* ROC-AUC

### 5. Deployment

* 🔌 REST API using **FastAPI**
* 🐳 Containerization using **Docker**
* 🎛️ Frontend interface using **Streamlit**

---

## 🧾 Tech Stack

| Component       | Tools Used                                      |
| --------------- | ----------------------------------------------- |
| Language        | Python 3.10                                     |
| Data Processing | Pandas, NumPy                                   |
| ML Models       | Scikit-learn, Decision Tree, RandomForest, etc. |
| Visualization   | Matplotlib, Seaborn                             |
| Text Analysis   | TextBlob, NLTK (optional)                       |
| API Framework   | FastAPI                                         |
| Deployment      | Docker, Uvicorn                                 |
| UI Dashboard    | Streamlit                                       |

---

## 📁 Project Structure

```bash
├── backend/
│   ├── Artifacts/              # Saved models and encoders
│   ├── Dockerfile              # Backend Docker configuration
│   ├── main.py                 # FastAPI backend
│   └── requirements.txt        # Backend dependencies
│
├── data/
│   ├── Original Data/          # Raw input files
│   └── Preprocessed Data/      # Cleaned and transformed datasets
│
├── frontend/
│   ├── Dockerfile              # Frontend Docker configuration
│   ├── requirements.txt        # Streamlit dependencies
│   └── y.py                    # Streamlit application
│
├── notebook/
│   ├── Flipkart Notebook1.ipynb  # Exploratory analysis
│   └── Model.ipynb              # Modeling and evaluation
│
├── README.md                  # Project overview file
├── docker-compose.yaml        # Multi-container orchestration
```

---

### Backend (FastAPI)

```bash

pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt
streamlit run y.py

