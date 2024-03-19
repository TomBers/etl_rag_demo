FROM python:3.12-slim

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./app.py ./app.py

COPY ./.chainlit ./.chainlit

COPY ./public ./public

COPY ./chainlit.md ./chainlit.md

# FOR DEPLOYMENT
# COPY ./.env ./.env
# Set environment variables
# ON FLY.io - flyctl secrets set OPENAI_API_KEY="YOUR_API_KEY"

RUN poetry install --no-interaction --no-ansi

EXPOSE 8080

CMD exec chainlit run app.py --host 0.0.0.0 --port 8080
