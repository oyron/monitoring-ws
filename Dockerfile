FROM python:3.10-alpine
RUN pip install --upgrade pip

RUN addgroup -S -g 1001 radix-non-root-group
RUN adduser -S -u 1001 -G radix-non-root-group radix-non-root-user
WORKDIR /code

USER 1001
ENV PATH="/home/radix-non-root-user/.local/bin:${PATH}"
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ app
RUN python -m app.tests.test_book_inventory

ARG portNumber=8080
ENV PORT=$portNumber
EXPOSE $portNumber

CMD ["python", "-m", "app.server"]