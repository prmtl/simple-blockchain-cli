FROM python:3.9.1-slim


ENV \
  # python
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && \
  apt-get install -y \
    # psycopg2 dependencies
    gcc libpq-dev python3-dev \
    # Translations dependencies
    gettext \
    # utilities
    make wget tar \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pip-tools==6.1.0


WORKDIR /app

COPY requirements.txt /app
RUN pip-sync requirements.txt

COPY . /app

RUN pip install .

CMD ["/bin/bash"]
