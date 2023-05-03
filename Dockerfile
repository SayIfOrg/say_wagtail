FROM python:3.10.8-slim-buster

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev\
    git

# Cache potential requirements
RUN --mount=type=cache,target=/root/.cache/pip

# Install the application server.
RUN pip install "gunicorn==20.1.0"

# Use /app folder as a directory where the source code is stored.
WORKDIR /project

# Install the project requirements.
COPY requirements.txt requirements_local.txt .
RUN pip install -r requirements.txt

# Add user that will be used in the container.
RUN useradd app

# Set this directory to be owned by the "app" user.
RUN chown app:app /project

# Copy the source code of the project into the container.
COPY --chown=app:app . .

# Use user "app" to run the build commands below and the server itself.
# USER app

EXPOSE 8000

CMD pip install -r requirements_local.txt && gunicorn config.wsgi:application
