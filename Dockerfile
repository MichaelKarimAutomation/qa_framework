FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv sync --frozen

COPY . .

RUN uv run playwright install --with-deps chromium

CMD ["uv", "run", "pytest", "tests/", "-v", "--env=dev_env"]
