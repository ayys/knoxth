FROM python:latest

WORKDIR "/app/tests/tests"

COPY . /app


# install pipenv
RUN pip install pipenv
RUN pipenv install --dev


CMD ["tox"]
