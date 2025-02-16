# Sentiment Atlas API

Sentiment Atlas API is a serverless backend for collecting, analyzing, and providing sentiment data across different countries. It is implemented using **AWS Lambda** and **Python 3.13**.

## 🛠 Architecture and Technology Stack

### Core Architecture
- **AWS Lambda** – Serverless functions for the API and data collection.
- **AWS DynamoDB** – NoSQL database for storing sentiment analysis results.
- **AWS API Gateway** – Routing requests to AWS Lambda.
- **AWS Secrets Manager** – Storing API credentials securely.
- **AWS SAM (Serverless Application Model)** – Infrastructure as code tool for managing AWS resources.
- **GitHub Actions** – CI/CD for testing and deployment.

### Key Technologies
- **Python 3.13** – Main programming language.
- **VADER Sentiment Analysis** – Library for sentiment analysis.
- **PRAW (Python Reddit API Wrapper)** – Interaction with the Reddit API for data collection.
- **boto3** – SDK for AWS services.
- **Pytest and Moto** – Unit testing and AWS service mocking.

## 🌟 Features
- **Real-time sentiment analysis** – Fetch and analyze sentiment data from Reddit posts.
- **Scalable and serverless** – Uses AWS Lambda for efficient, cost-effective scaling.
- **Automated deployment** – Managed via GitHub Actions.
- **Secure credentials management** – Uses AWS Secrets Manager for storing API credentials.
- **DynamoDB storage** – Stores and retrieves sentiment data efficiently.
- **Comprehensive unit testing** – Ensures code reliability with Pytest and Moto.

## 📦 Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/mist941/sentiment-atlas.api
   cd sentiment-atlas.api
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   cd api_function && pip install -r requirements.txt && cd ..
   cd collect_data_function && pip install -r requirements.txt && cd ..
   ```
3. **Run locally using AWS SAM:**
   ```sh
   sam build
   sam local start-api
   ```

## 🎡 Project Structure

```
sentiment-atlas.api/
build artifacts
│── .github/workflows/       # CI/CD GitHub Actions for testing and deployment
│── api_function/            # Lambda function for API
│   │── main.py              # Main API logic
│   │── requirements.txt     # API dependencies
│── collect_data_function/   # Data collection function
│   │── main.py              # Analysis and storage logic
│   │── countries.json       # Countries for analysis
│── tests/                   # Unit tests for API and data collection functions
│── template.yaml            # AWS SAM template for deployment
```

## 🎨 Deployment

Deployment is managed via **GitHub Actions** (see `.github/workflows/deploy.yml`).

```sh
sam build
sam deploy --stack-name sentiment-atlas --resolve-s3 --capabilities CAPABILITY_IAM
```

## License

⭐ If you like this project, don't forget to give it a star on GitHub!

