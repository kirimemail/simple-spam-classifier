#!/usr/bin/env sh
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask database seed
supervisord
/home/spam_classifier/venv/bin/gunicorn -b :8000 -w 4 spam_classifier:app