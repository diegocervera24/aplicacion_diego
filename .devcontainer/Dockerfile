FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /workspace
WORKDIR /workspace

RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt if it exists
COPY /requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY ../. .
# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT python app/manage.py migrate && python app/manage.py runserver 0.0.0.0:8000