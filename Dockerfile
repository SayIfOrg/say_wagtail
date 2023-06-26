FROM nikolaik/python-nodejs:python3.10-nodejs18-slim

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN --mount=type=cache,target=var/cache/apt/archives apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    # libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev\
    git

# Install the application server.
RUN pip install "gunicorn[gevent]>=20.1.0,<20.2"
RUN --mount=type=cache,target=/root/.npm pip install \
    "git+https://github.com/engAmirEng/wagtail.git@02788dd5ca6dd4eea5a"

# Use /app folder as a directory where the source code is stored.
WORKDIR /project

# Install the project requirements.
COPY requirements.txt .
# Cache potential requirements
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Install the JS requirements.
COPY package.json package-lock.json .
RUN --mount=type=cache,target=/root/.npm npm ci

# Add user that will be used in the container.
RUN useradd app

# Set this directory to be owned by the "app" user.
RUN chown app:app /project

# Copy the source code of the project into the container.
COPY --chown=app:app . .

# Build Vite
RUN npm run build

# Use user "app" to run the build commands below and the server itself.
# USER app

EXPOSE 8000

CMD python manage.py collectstatic --noinput && gunicorn --config config/gunicorn.config.py config.wsgi:application
