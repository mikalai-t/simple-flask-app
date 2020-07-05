# multi-stage build with all the pros as described at:
#  * https://testdriven.io/blog/faster-ci-builds-with-docker-cache/

FROM python:3.7 as base

ENV DEBIAN_FRONTEND="noninteractive" \
    WORKDIR="/usr/src/app" \
    # prevents Python from writing pyc files to disc
    PYTHONDONTWRITEBYTECODE=1 \
    # prevents Python from buffering stdout and stderr
    PYTHONUNBUFFERED=1

COPY requirements.txt ${WORKDIR}/requirements.txt

RUN \
    pip3 wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ${WORKDIR}/requirements.txt

#-----------------------------------------------------------------------------------------------------------------------

FROM python:3.7-slim

ARG FLASK_ENV="dev"

ENV DEBIAN_FRONTEND="noninteractive" \
    WORKDIR="/usr/src/app" \
    # prevents Python from writing pyc files to disc
    PYTHONDONTWRITEBYTECODE=1 \
    # prevents Python from buffering stdout and stderr
    PYTHONUNBUFFERED=1

WORKDIR ${WORKDIR}

RUN \
    apt-get -yq update \
    && apt-get -yq install \
        netcat \
    &&  { \
            echo '#!/usr/bin/env sh'; \
            echo 'cd ${WORKDIR}'; \
            echo 'exec `eval echo "${@}"`'; \
        } | tee /entrypoint.sh \
    &&  chmod a+x /*.sh \
    # clean image
    && apt-get -yq autoremove \
    && apt-get -yq clean \
    && rm -rf /var/cache/apt/* \
    && rm -rf /tmp/*

COPY --from=base /wheels ${WORKDIR}/wheels
COPY --from=base ${WORKDIR}/requirements.txt ${WORKDIR}/requirements.txt

RUN \
    python -m pip --no-cache install ${WORKDIR}/wheels/*

COPY ext/ ${WORKDIR}/ext/
COPY main.py ${WORKDIR}/main.py

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5000

CMD ["gunicorn", \
     "--chdir", "${WORKDIR}", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "-w", "2", \
     "--threads", "2", \
     "-b", "0.0.0.0:5000", \
     "main:app"]
