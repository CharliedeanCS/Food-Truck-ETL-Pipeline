FROM python:latest

EXPOSE 8501

WORKDIR /dashboard

COPY requirements.txt . 
RUN pip3 install -r requirements.txt

COPY main.py . 
COPY database.py . 
COPY visuals.py . 

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
