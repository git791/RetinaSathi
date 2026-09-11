FROM containers.mathworks.com/matlab-runtime:r2026a

USER root
ENV DEBIAN_FRONTEND=noninteractive
ENV MATLAB_MODE=compiled

# The mathworks image is Ubuntu based, so we install Python
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install dependencies using --break-system-packages (standard for ubuntu >= 23.04 with raw pip, or we can use venv)
# To be safe, let's create a venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY . /app/

# Install the matlab package from the build directory
RUN pip install /app/deployment_artifacts/build

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
