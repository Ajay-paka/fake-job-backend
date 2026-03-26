# Fake Job Detector Backend 🛡️

The Fake Job Detector Backend is a service designed to analyze job postings and identify potential scam indicators.
It powers the Fake Job Detector frontend by processing job descriptions, evaluating risk signals, and returning structured analysis results.

## 🚀 Overview

This backend receives job descriptions from the frontend application and analyzes them for suspicious patterns commonly found in fake job postings.

The system helps job seekers quickly determine whether a job opportunity appears legitimate or potentially fraudulent.

## ✨ Key Features

* Job description analysis
* Detection of scam-related keywords
* Risk indicator identification
* Structured analysis results
* API-based integration with frontend
* Lightweight and scalable backend service

## 🛠 Tech Stack

* Node.js
* Express.js
* JavaScript / TypeScript
* REST API

## 📂 Project Structure

```text
fake-job-backend/
│
├── src/
│   ├── controllers/
│   ├── services/
│   ├── routes/
│   ├── utils/
│   └── server.js
│
├── package.json
├── README.md
└── .env
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Ajay-paka/fake-job-backend.git
cd fake-job-backend
```

Install dependencies:

```bash
npm install
```

Start the backend server:

```bash
npm start
```

Development mode:

```bash
npm run dev
```

## 🔗 API Endpoint

Example endpoint for analyzing job descriptions:

```http
POST /analyze-job
```

Request body:

```json
{
  "jobDescription": "Paste job description text here"
}
```

Response example:

```json
{
  "riskScore": 65,
  "warningSignals": [
    "Asking for payment before joining",
    "Suspicious email domain"
  ],
  "recommendation": "This job posting may be risky."
}
```

## 🧠 How the System Works

1. User submits a job description from the frontend
2. Backend receives the text via API
3. Scam detection logic analyzes the content
4. Risk indicators are identified
5. Results are returned to the frontend

## 🔮 Future Improvements

* AI-powered scam detection using LLMs
* Advanced risk scoring
* Domain reputation checks
* Job company verification
* Fraud reporting system

## 🔗 Related Projects

Frontend repository:

https://github.com/Ajay-paka/fake-job-frontend

## 👨‍💻 Author

Ajay Paka

GitHub: https://github.com/Ajay-paka
