FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync
COPY app.py .
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", "--server.port=8501"]
