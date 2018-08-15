FROM python:3.6-alpine

RUN adduser -D spam_classifier && \
    adduser spam_classifier tty

WORKDIR /home/spam_classifier
COPY requirements.txt requirements.txt
RUN apk add --no-cache libstdc++ openblas && \
    apk add --no-cache --virtual=.build-dependency libffi-dev openssl-dev gfortran gcc g++ file binutils musl-dev wget openblas-dev git
RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir --upgrade pip && \
    venv/bin/pip install --no-cache-dir -r requirements.txt && \
    venv/bin/pip install --no-cache-dir git+git://github.com/Supervisor/supervisor.git#egg=supervisor && \
    venv/bin/python -m nltk.downloader -d /home/spam_classifier/venv/nltk_data punkt && \
    venv/bin/python -m nltk.downloader -d /home/spam_classifier/venv/nltk_data stopwords
RUN apk del .build-dependency

COPY app app
COPY migrations migrations
COPY seeds seeds
COPY EmailProcessing EmailProcessing
COPY logs logs
COPY spam_model spam_model
COPY config.py spam_classifier.py supervisord.conf boot.sh ./
COPY deployment /opt/docker/etc/supervisor.d

ENV FLASK_APP "spam_classifier.py"
RUN chown -R spam_classifier:spam_classifier ./ && \
    chmod a+x boot.sh
USER spam_classifier

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]