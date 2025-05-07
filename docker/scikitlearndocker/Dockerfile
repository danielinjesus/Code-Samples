FROM python:3.8-slim
WORKDIR /app
CIOY requirements.txt /app/
RUN pip install --no-cached-dir -r requirements.txt

COPY model_learn.py /app/
CMD ["python", "./model_learn.py"]