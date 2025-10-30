FROM python:3.10-slim

# System deps (build tools + git + curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Faster layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir jupyterlab nbformat ipykernel \
    && python -m ipykernel install --name datasens --sys-prefix

# Copy project
COPY . /app

EXPOSE 8888

# Default: start Jupyter Lab, token disabled for simplicity in local demo
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token="]


