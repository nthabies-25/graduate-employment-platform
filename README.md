# Employment Analytics API

A cloud-native REST API for transforming graduate employment data into reliable, queryable and decision-ready analytics.

## 📌 Overview

Graduate employment data is often collected from different sources and stored in inconsistent formats, making it difficult to analyse and compare employment outcomes.

This project solves that problem by building an end-to-end platform that **ingests, validates, transforms, stores, analyses and exposes graduate employment data through a REST API**.

The system allows users to query employment outcomes by:

* Qualification
* Institution
* Industry
* Year
* Employment status
* Time to employment

Instead of manually analysing spreadsheets, users can request structured analytical results through API endpoints.

## 🎯 Problem

Raw employment datasets can contain:

* Duplicate records
* Missing values
* Inconsistent qualification names
* Invalid dates or identifiers
* Data spread across multiple systems
* Difficult-to-query spreadsheets
* Manual reporting processes

The goal is to transform this raw data into a **reliable, scalable and accessible information service**.

## 🏗️ Architecture

```text
Data Sources
(CSV / API / Database)
        ↓
Data Ingestion
        ↓
Validation & Data Quality
        ↓
ETL / Transformation
        ↓
PostgreSQL
        ↓
Service Layer
        ↓
REST API
        ↓
Dashboard / API Clients
```

The application is designed using **Separation of Concerns**, keeping data processing, database access, business logic and API routes as separate components.

## 🔄 Data Engineering Pipeline

The ETL pipeline follows three main stages:

### Extract

Collect employment data from sources such as CSV files, APIs or existing databases.

### Transform

Clean and standardise the data by:

* Removing duplicates
* Handling missing values
* Standardising dates
* Standardising qualification names
* Validating categorical values
* Converting data types
* Calculating derived fields
* Joining related datasets

### Load

Load validated and transformed data into PostgreSQL for analytical querying.

The pipeline is designed to be **idempotent**, preventing repeated executions from unintentionally creating duplicate records.

## 🗄️ Data Model

The application uses a relational database model.

```text
Institutions
     │
     ↓
Graduates ───── Qualifications
     │
     ↓
Employment
     │
     ↓
Industries
```

This approach reduces duplication and allows meaningful analytical queries across related datasets.

## 🌐 REST API

Example endpoints:

```text
GET /api/graduates
GET /api/graduates/{id}

GET /api/qualifications
GET /api/qualifications/{id}

GET /api/statistics/employment
GET /api/statistics/by-year
GET /api/statistics/by-qualification
GET /api/statistics/by-industry

GET /api/institutions
GET /api/institutions/{id}/employment

GET /health
```

Example analytical response:

```json
{
  "data": [
    {
      "qualification": "Computer Science",
      "graduates": 850,
      "employed": 731,
      "employment_rate": 86.0
    }
  ]
}
```

The API therefore provides **analytical information rather than simply exposing raw database records**.

## 📊 Analytics

The platform supports questions such as:

* What is the employment rate by qualification?
* Which industries employ the most graduates?
* How do employment outcomes change over time?
* Which institutions have stronger employment outcomes?
* How long does it take graduates to find employment?

Example:

```text
Employment Rate =
Employed Graduates / Total Graduates × 100
```

## 🛠️ Technology Stack

### Data Engineering

* Python
* Pandas
* SQL
* PostgreSQL
* ETL
* Data validation

### Backend

* Flask / FastAPI
* REST
* JSON

### Cloud

* AWS S3
* AWS RDS
* AWS CloudWatch
* IAM
* AWS Lambda

### DevOps

* Docker
* Git
* GitHub Actions
* CI/CD

### Testing

* Pytest
* Unit testing
* Integration testing
* API testing
* Data validation testing

## 🐳 Containerisation

The application is containerised with Docker to create a reproducible environment across development, testing and deployment.

```text
Application
     ↓
Docker Image
     ↓
Container
     ↓
Cloud Environment
```

This helps reduce environment-related problems such as **"it works on my machine."**

## ☁️ Cloud Architecture

The planned production architecture uses AWS services:

```text
              User
               ↓
            REST API
               ↓
           AWS RDS
          PostgreSQL
               
AWS S3
  ↓
Raw Data
  ↓
ETL Pipeline
  ↓
Processed Data
```

S3 stores raw, processed and rejected datasets, while RDS provides the managed PostgreSQL database used by the API.

## 🔄 CI/CD

GitHub Actions automates the development pipeline:

```text
Git Push
   ↓
Run Tests
   ↓
Lint
   ↓
Build Docker Image
   ↓
Deploy
```

Deployment should only occur after automated checks successfully pass.

## 🧪 Testing

Testing is performed at multiple levels.

**Unit tests**

* ETL transformations
* Validation
* Analytics calculations
* Business logic

**Integration tests**

* API → Service → Database

**API tests**

* HTTP status codes
* Response structure
* Error handling
* Request validation

Example:

```text
GET /api/graduates/1
→ 200 OK

GET /api/graduates/999999
→ 404 NOT FOUND
```

## 🔐 Security

The project follows basic production security principles:

* Secrets stored in environment variables
* Database credentials excluded from Git
* Parameterised SQL queries
* Input validation
* Least-privilege IAM
* HTTPS in production
* API authentication where required

## 📁 Project Structure

```text
employment-analytics-api/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   └── models/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Development Roadmap

### Phase 1 — Data Pipeline

* Create employment dataset
* Build extraction process
* Implement validation
* Implement transformations
* Load data into PostgreSQL
* Add ETL tests

### Phase 2 — REST API

* Build API
* Implement repository and service layers
* Create REST endpoints
* Add validation and error handling
* Add API tests

### Phase 3 — Docker & CI/CD

* Containerise application
* Configure PostgreSQL
* Create GitHub Actions pipeline
* Run automated tests
* Build Docker image

### Phase 4 — AWS Deployment

* Configure S3
* Configure RDS
* Deploy application
* Configure IAM and environment variables
* Add CloudWatch monitoring

## 🌟 What This Project Demonstrates

This project demonstrates an end-to-end engineering workflow:

```text
INGEST
   ↓
VALIDATE
   ↓
TRANSFORM
   ↓
STORE
   ↓
ANALYSE
   ↓
SERVE
   ↓
CONTAINERISE
   ↓
DEPLOY
   ↓
MONITOR
```

Key concepts demonstrated:

* Data Engineering
* ETL/ELT
* Data quality
* Relational database design
* SQL
* REST API development
* Separation of Concerns
* Automated testing
* Docker
* CI/CD
* AWS cloud services
* Observability
* Scalable architecture

## 📌 Project Status

**In Development**

The project is being developed incrementally, starting with the local ETL pipeline and PostgreSQL database before introducing Docker, CI/CD and AWS deployment.

## Portfolio Goal

This project is designed to demonstrate the ability to build more than a data analysis script or basic CRUD API.

The goal is to demonstrate the complete journey of data:

**Ingest → Validate → Transform → Store → Analyse → Serve → Deploy → Monitor**
