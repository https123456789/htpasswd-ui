FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

COPY ./pyproject.toml ./uv.lock .

RUN uv sync --locked --compile-bytecode --no-install-project

COPY . .

CMD ["uv", "run", "main.py"]
