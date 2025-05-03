#! /bin/sh

WORKERS=$(($(nproc)*2 + 1))

gunicorn --certfile=certificado.crt --keyfile=pk.key \
    --workers=$WORKERS \
    --worker-class=gevent \
    --worker-connections=100 \
    --timeout=30 \
    --keep-alive=300 \
    --max-requests=1000 \
    --max-requests-jitter=50 \
    Grow_your_empire.wsgi \
    -b <ip>:<port> \
    --access-logfile "./log.txt"
