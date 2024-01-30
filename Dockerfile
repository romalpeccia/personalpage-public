FROM python:3.8

RUN useradd personalpage

WORKDIR /home/personalpage 

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY personalpage.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP personalpage.py


RUN chown -R personalpage:personalpage ./
USER personalpage

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]