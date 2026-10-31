FROM python:3.13-slim

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY client.py .
COPY backend/ ./backend/
COPY .streamlit/ ./.streamlit/

WORKDIR /app/backend

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & exec streamlit run /app/client.py --server.address=0.0.0.0 --server.port=8501"]
