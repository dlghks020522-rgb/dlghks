# Python FastAPI backend Dockerfile

FROM python:3.10

WORKDIR /app

# requirements.txt가 있다면 복사 후 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# FastAPI 서버 실행 (uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]