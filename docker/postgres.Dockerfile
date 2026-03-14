FROM postgres:16

# Install pgvector extension
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y postgresql-server-dev-16 build-essential && \
    git clone https://github.com/pgvector/pgvector.git /tmp/pgvector && \
    cd /tmp/pgvector && \
    make && make install

# Set default locale and encoding
ENV POSTGRES_USER=research
ENV POSTGRES_PASSWORD=researchpass
ENV POSTGRES_DB=research_db

EXPOSE 5432
