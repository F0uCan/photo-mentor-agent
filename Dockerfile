FROM python:3.11-slim

# Install system dependencies for HEIC/Imaging
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libheif-dev \
    libde265-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install Python requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip list  # This will show you if streamlit is installed during the build logs

# Copy the rest of the code
COPY . .

EXPOSE 8501

# Note the path: we are running app.py inside the app/ folder
CMD ["python", "-m", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]