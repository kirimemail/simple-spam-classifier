FROM python:3.6-alpine

RUN adduser -D spam_classifier

WORKDIR /home/spam_classifier
RUN apk add --no-cache libffi-dev openssl-dev gfortran gcc g++ file binutils musl-dev libstdc++ wget openblas-dev git
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir --upgrade pip
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install --no-cache-dir git+git://github.com/Supervisor/supervisor.git#egg=supervisor
RUN venv/bin/python -m nltk.downloader punkt
RUN venv/bin/python -m nltk.downloader stopwords

COPY app app
COPY migrations migrations
COPY additional_data additional_data
COPY seeds seeds
COPY EmailProcessing EmailProcessing
COPY logs logs
COPY spam_model spam_model
COPY config.py spam_classifier.py supervisord.conf ./
RUN echo supervisord.conf >> /etc/supervisord.conf
COPY deployment /opt/docker/etc/supervisor.d
COPY boot.sh boot.sh

ENV FLASK_APP "spam_classifier.py"
RUN chown -R spam_classifier:spam_classifier ./
USER spam_classifier
RUN chmod a+x boot.sh

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]