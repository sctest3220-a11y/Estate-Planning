# Container image for the Thailand estate-planning web app.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Store user credentials on a writable volume in production.
ENV ESTATE_USER_STORE=/data/users.json
VOLUME ["/data"]

EXPOSE 8000

# ESTATE_SECRET_KEY (and optionally GOOGLE_CLIENT_ID/SECRET) must be provided at
# runtime — see .env.example and docs/Deployment.md.
CMD ["gunicorn", "estate_planning.web.app:app", "-b", "0.0.0.0:8000", "--workers", "2"]
