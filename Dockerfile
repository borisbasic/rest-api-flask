FROM python:3.10
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:create_app()", "--host", "0.0.0.0", "--port", "5000"]