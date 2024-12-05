FROM python:3.13.1

RUN useradd -ms /bin/bash app-user

RUN mkdir -p /appl

COPY . /appl

RUN chown -R app-user: /appl

USER app-user

WORKDIR /appl

RUN make deps

CMD ["make", "run"]