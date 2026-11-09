FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync
COPY . .
RUN uv run train.py
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", \
     "--host", "0.0.0.0", "--port", "8000"]
