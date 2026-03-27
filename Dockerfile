FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install uv

# Install dependencies strictly via pyproject.toml (e configures the module)
RUN uv pip install --system -e .

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
