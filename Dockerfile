# MIG tools require NVIDIA Container Toolkit + host driver; this image is optional.
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
RUN pip install --no-cache-dir -e .
ENTRYPOINT ["mig-lab"]
