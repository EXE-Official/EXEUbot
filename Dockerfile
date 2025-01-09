# Usa un'immagine base di Python
FROM python:3.12-slim

# Imposta il working directory
WORKDIR /app

# Copia il file di configurazione e le dipendenze
COPY pyproject.toml poetry.lock ./

# Installa Poetry
RUN pip install --no-cache-dir poetry

# Installa le dipendenze del progetto
RUN poetry install --no-interaction --no-ansi

# Copia tutto il progetto nella directory di lavoro
COPY . .

# Specifica il comando di avvio
CMD ["poetry", "run", "python", "main.py"]
