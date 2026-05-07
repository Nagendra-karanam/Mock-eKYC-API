FROM python:3.11-slim AS builder

WORKDIR /app

# install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# copy dependency manifest
COPY requirements.txt ./

# install dependencies into a separate folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#--- stage 2 production image ---
FROM python:3.11-slim

WORKDIR /app

# security best practices prevent pyc + buffered logs
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# copy application source into image
COPY app.py ./

# set ownership for non-root runtime user
RUN chown -R appuser:appgroup /app

# switch to non-root user
USER appuser

# expose application port
EXPOSE 5000

# healthcheck
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# start application
CMD ["python", "app.py"]