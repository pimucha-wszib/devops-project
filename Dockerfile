# Stage 1 - BUILD
FROM python:3.11 AS builder

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --upgrade pip
# Install dependencies to a separate location which will be copied later
RUN pip install --prefix=/install -r requirements.txt

COPY app /app

# Stage 2 - TESTING
FROM builder AS test
ENV PYTHONPATH=/app
RUN pytest -q


# STAGE 3 - FINAL
FROM python:3.11-slim AS final

WORKDIR /app
# Copy packages from build stage
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

CMD ["python", "-m", "src.app"]
