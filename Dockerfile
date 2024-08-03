FROM python:3.11.4-slim-buster AS build-env

WORKDIR /app

COPY requirements.txt .

# Install netcat and clean up to reduce image size
RUN apt-get update && \
    apt-get install -y netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production command
FROM build-env AS prod
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "voicenger.wsgi:application"]