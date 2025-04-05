# step1.
FROM python:3.12.3

# 작업 디렉토리 설정
WORKDIR /app

# 여기서 코드 복사
COPY . /app

# 요구 사항 설치
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 포트 개방 (개발 서버용)
EXPOSE 8000

# 명령 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

