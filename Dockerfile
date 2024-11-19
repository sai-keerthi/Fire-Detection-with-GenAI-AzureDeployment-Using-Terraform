FROM python:3.8-silm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no--cache-dir -r requirements.txt
COPY . .
EXPOSE 80
CMD ["python","run.py"]