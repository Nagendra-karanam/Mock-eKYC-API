Mock eKYC API – DevOps Technical Assessment
Overview
This repository contains my solution for the DevOps / Operations Support Engineer technical assessment.
The scenario focuses on onboarding multiple startup tenants into the UIDAI Sandbox environment using secure and automated DevOps practices.
The implementation covers:
•	Containerization using Docker
•	CI/CD pipeline using GitHub Actions
•	Mock image deployment workflow
•	Monitoring and alerting using Prometheus
•	Incident response automation using Bash scripting
-------------------------------------------------------------------------
Repository Structure

├── Dockerfile
├── app.py
├── requirements.txt
├── triage.sh
├── monitoring/
│   ├── alerts.yml
│   └── promql.txt
└── .github/workflows/
    └── deploy.yml
-------------------------------------------------------------------------
Technologies Used
•	Python Flask
•	Docker
•	GitHub Actions
•	Kubernetes (mock deployment)
•	Prometheus
•	Bash
-------------------------------------------------------------------------
Docker Build & Run
Build image:
docker build -t mock-ekyc-api .
Run container:
docker run -p 5000:5000 mock-ekyc-api
------------------------------------------------------------------------
CI/CD Pipeline
The GitHub Actions workflow triggers automatically on push to the main branch.
Pipeline stages:
1.	Checkout source code
2.	Build Docker image
3.	Mock security scan
4.	Push image to Docker registry
5.	Mock Kubernetes deployment
--------------------------------------------------------------------------
Monitoring
Prometheus files are available under:
monitoring/
Includes:
•	PromQL query for 5xx error rate
•	Alert rule for high eKYC API failures
--------------------------------------------------------------------------
Incident Response Script
Run CrashLoopBackOff triage script:
./triage.sh startup-tenant-alpha
This collects logs for crashing pods inside the provided namespace.
--------------------------------------------------------------------------

Author
Nagendra

