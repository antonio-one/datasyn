# stage 1
FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# stage 2
FROM python-base as dependency-base

RUN apt-get update; \
    apt-get install -y build-essential \
    procps \
    iputils-ping

EXPOSE ${DATASYN_PORT}

# stage 3
FROM dependency-base as development-base

ARG WHEEL=datasyn-0.1.0-py3-none-any.whl
ARG APPDIR=/datasyn

WORKDIR ${APPDIR}/
ADD datasyn/ ./
ADD dist/${WHEEL} ./
ADD .env ./

RUN pip3 install ${APPDIR}/${WHEEL}

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8081", "datasyn.entrypoints.app:app"]
