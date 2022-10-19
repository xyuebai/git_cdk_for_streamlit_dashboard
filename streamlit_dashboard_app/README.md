# A Report Dashboard Powered by Streamlit

https://streamlit.io/

## 1. How to Run
```
$ pip install -r requirements.txt
$ streamlit run stream.py
```
Click the link on terminal to get the view of the dashboard
## 2. How to Run (Docker)
```
$ pip install -r requirements.txt
$ docker build -t s-dashboard .
$ docker container run -p 8501:8501 s-dashboard:latest
```
Type http://localhost:8501 to access the dashboard
