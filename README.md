# Dashboard Deployment with AWS ECS-Fargate (AWS CDK)
Check the dashboard by clicking the link:
https://cdk.nc-streamlit-dashboard.com/
## Project Description
This project creates a stock market dashboard with streamlit. And the UI is hosted on AWS ECS-Fargate. The AWS infrastructure is developed by AWS CDK.
## File Structure

```
 .
 ├── streamlit_dashboard_app
 │   ├── AAPL.csv       # stock market data
 │   ├── stream.py      # dashboard 
 │   ├── setup.sh      
 │   ├── Dockerfile      
 │   ├── Procfile
 │   ├── README.md
 │   └── requirements.txt
 ├── cdk_infra
 │   ├── git_cdk_for_streamlit_dashboard
 │   │   ├── __init__.py
 │   │   └──git_cdk_for_streamlit_dashboard.txt     # CDK stack 
 │   ├── tests
 │   ├── app.py         # entrypoint   
 │   ├── cdk.json       # context
 │   ├── README.md
 │   ├── source.bat         
 │   ├── requirements-dev.txt        
 │   ├── requirements.txt      
 │   └── requirements.txt                     
 ├── .gitignore
 └── README.md
```
## UI

UI is designed with [Streamlit](streamlit.io), which creates scientific dashboard with pure pyhton code


## AWS CDK

Build below infrasturcture with AWS CDK
![](https://yue-cv-pic.s3.eu-west-1.amazonaws.com/ecs-dashboard.jpg)

The resources are created by cdk includes:
- VPC
- ECS
- Route53 A Records
- Fargat Serivce
- Load Balancer
- Security Group
- Target Group
