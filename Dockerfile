FROM python:3.9-slim AS compile-image

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.9-slim AS build-image

COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "app.py"]
