# 🛡️ PhishGuard AI
### An Explainable Machine Learning Prototype for Phishing URL Detection

PhishGuard AI is a web-based cybersecurity project that uses machine learning to classify URLs as potentially phishing or likely legitimate. It analyzes URL characteristics and displays warning indicators to help users understand possible risks.

The project combines Python, feature extraction, a Random Forest classifier, and a Flask web application to demonstrate how machine learning can support phishing awareness.

> **Disclaimer:** PhishGuard AI is an educational prototype, not a production-grade security solution. Its predictions are not guarantees. A URL classified as likely legitimate may still be malicious, and a flagged URL may be harmless.

## ✨ Features

- **Machine Learning Detection:** Uses a Random Forest classifier to predict whether a URL resembles phishing.
- **URL Feature Extraction:** Examines URL length, hostname structure, digits, punctuation, suspicious keywords, and other characteristics.
- **Warning Indicators:** Displays selected URL characteristics that may deserve attention.
- **Web Interface:** Provides a simple interface for entering URLs and viewing results.
- **Model Evaluation:** Reports accuracy, precision, recall, F1-score, and a confusion matrix during training.
- **Local Analysis:** Examines URL text without visiting the submitted website.

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| pandas | Dataset processing |
| scikit-learn | Machine learning and model evaluation |
| Random Forest | URL classification algorithm |
| joblib | Saving and loading the trained model |
| HTML | Webpage structure |
| CSS | User interface styling |
| JavaScript | Form interaction |
| Git and GitHub | Version control and project hosting |

## 🏗️ Project Structure

```text
PhishGuard_AI/
├── app.py
├── features.py
├── train_model.py
├── requirements.txt
├── README.md
├── data/
│   └── phishing_urls.csv
├── model/
│   └── phishguard_model.joblib
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

- `app.py` — Runs the Flask web application and returns predictions.
- `features.py` — Extracts numerical characteristics from URLs.
- `train_model.py` — Loads the dataset, trains the classifier, and evaluates its performance.
- `requirements.txt` — Lists the Python dependencies.
- `data/phishing_urls.csv` — Contains the labeled URL dataset used for training.
- `model/phishguard_model.joblib` — Stores the trained machine learning model.
- `templates/index.html` — Defines the website interface.
- `static/style.css` — Styles the interface.
- `static/script.js` — Handles the form's loading interaction.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later is recommended.
- pip package manager.
- Git.
- A modern web browser.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your repository.

Move into the project directory:

```bash
cd PhishGuard_AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare the dataset

Place the labeled CSV dataset at:

```text
data/phishing_urls.csv
```

The training script expects a URL column and a label column. Review the dataset's documentation and confirm its labels before training.

The project's label convention is:

- `0` — Legitimate
- `1` — Phishing

Dataset formats and label meanings must be checked before use.

### 5. Train the machine learning model

```bash
python train_model.py
```

The script extracts URL features, trains a Random Forest classifier, prints evaluation metrics, and saves the model to:

```text
model/phishguard_model.joblib
```

### 6. Run the web application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

Enter a URL and select **Analyze URL** to view the model's prediction and the available warning indicators.

## 🧠 How It Works

1. **Input:** The user enters a URL in the web interface.
2. **Feature Extraction:** The application extracts numerical characteristics from the URL.
3. **Prediction:** The trained Random Forest classifier analyzes those features.
4. **Warning Indicators:** The application checks selected URL characteristics and displays relevant warnings.
5. **Result:** The webpage displays the model's classification and a security disclaimer.

## 📊 Model Evaluation

The training script reports the following metrics:

- **Accuracy:** The proportion of test examples classified correctly.
- **Precision:** How many examples predicted as phishing were actually labeled phishing.
- **Recall:** How many phishing examples in the test set were identified.
- **F1-score:** A combined measure of precision and recall.
- **Confusion Matrix:** A breakdown of correct and incorrect classifications.

Actual evaluation results should be recorded here after training and validation.

**Important:** Performance on a test split does not guarantee performance on new or previously unseen phishing attacks. Dataset quality, duplicate URLs, and similarities between training and testing examples can affect the results.

## 🔒 Security and Limitations

- The application analyzes URL text and does not visit the submitted website.
- URL characteristics are indicators, not proof of malicious activity.
- The classifier may produce false positives and false negatives.
- HTTPS does not automatically mean a website is trustworthy.
- The model's prediction should not be treated as a calibrated probability of danger.
- The prototype does not replace browser security features, threat intelligence services, or professional security tools.
- The development server is intended for local testing, not public production deployment.

## 🚀 Future Improvements

- Add explainable AI techniques to clarify individual model predictions.
- Evaluate the model on a carefully separated, unseen dataset.
- Improve URL validation and error handling.
- Compare Random Forest with other machine learning algorithms.
- Add model performance visualizations.
- Explore trusted threat intelligence integrations.
- Develop a deployment-ready version with appropriate security controls.

## 🎯 Project Objective

The objective of PhishGuard AI is to explore how machine learning and explainable warning indicators can contribute to phishing awareness and safer browsing practices.

This project was developed as a learning and innovation initiative in cybersecurity and machine learning.

## 👩‍💻 Author

**Devi Sree**

Computer Science and Engineering

