# Use an official Python runtime based on "slim-buster" as a parent image.
FROM python:3.10.8-slim-buster

# Port used by this container to serve HTTP.
EXPOSE 8000

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
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.1.0"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Add user that will be used in the container.
RUN useradd app

# Set this directory to be owned by the "app" user.
RUN chown app:app /app

# Copy the source code of the project into the container.
COPY --chown=app:app . .

# Use user "app" to run the build commands below and the server itself.
USER app

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   instance can be started with a simple "docker run" command.
# grpc servieve
# CMD set -xe; python manage.py migrate --noinput; python manage.py grpcserver --port 5061
# web servieve
CMD set -xe; python manage.py migrate --noinput; gunicorn say_wagtail.wsgi:application
