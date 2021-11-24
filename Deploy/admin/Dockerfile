FROM python:3.9.1

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install netcat -y
RUN apt install -y gettext libgettextpo-dev

COPY cinema/requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /usr/src/app/
COPY entrypoint.sh /usr/src/app/
RUN chmod 777 /usr/src/app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
