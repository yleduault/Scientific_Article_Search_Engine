FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend
COPY gui/ ./gui

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=research
ENV POSTGRES_PASSWORD=researchpass
ENV POSTGRES_DB=research_db
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

# Entrypoint
CMD ["python", "backend/scheduler.py"]
