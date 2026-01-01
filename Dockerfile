# Stage 1 - BUILD
FROM python:3.11 AS builder

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app /app

# Stage 2 - TESTING
FROM builder AS test
RUN python -m pytest -x
RUN touch /app/test_success


# STAGE 3 - FINAL
FROM python:3.11-slim AS final

WORKDIR /app

# Copy test success indicator so we know tests passed
COPY --from=test /app/test_success /app/

# Copy packages from build stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

CMD ["python", "-m", "src.app"]
