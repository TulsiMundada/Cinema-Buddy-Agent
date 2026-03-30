FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE xxxx

CMD ["streamlit", "run", "app.py", "--server.port=xxxx", "--server.address=x.x.x.x"]
