# Validar version de imagen
FROM python:3.9-slim

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --root-user-action=ignore "poetry>=1.8,<1.9" \
	&& poetry config virtualenvs.create false \
	&& poetry install --no-interaction --no-ansi --no-cache -vv --without dev \
	&& rm -f pyproject.toml poetry.lock

# Copiar todos los archivos
COPY . .

# Establecer la variable de entorno PYTHONPATH
ENV PYTHONPATH=/app
RUN ls -la /app
EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000"]
