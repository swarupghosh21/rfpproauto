# FROM python:3.11-slim
# FROM python:3.10-slim

# ENV PIP_REQUIRE_HASHES=0
# ENV PIP_NO_CACHE_DIR=1

# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     git \
#     curl \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*


# # RUN pip install --no-cache-dir torch==2.1.0 \
# #     --index-url https://download.pytorch.org/whl/cpu

# COPY requirements.txt .

# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt \
#     -i https://pypi.tuna.tsinghua.edu.cn/simple

# RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding model (VERY IMPORTANT)
#   RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
FROM rfp-base

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]