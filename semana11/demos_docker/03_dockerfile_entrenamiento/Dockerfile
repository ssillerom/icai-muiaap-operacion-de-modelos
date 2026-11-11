FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync
COPY train.py .
CMD ["uv", "run", "train.py"]
