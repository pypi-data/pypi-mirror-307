FROM python:3.10-slim AS base

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential git libportaudio2 pandoc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# https://playwright.dev/python/docs/browsers
ENV PLAYWRIGHT_BROWSERS_PATH=/pw-browsers
ENV PLAYWRIGHT_SKIP_BROWSER_GC=1

# Permission kludges to support `docker run --user xxx`
RUN chmod a+rwx /venv /venv/bin /venv/include /venv/lib /venv/lib/python3.10/site-packages

RUN mkdir       /.blackboxai /.cache /pw-browsers
RUN chmod a+rwx /.blackboxai /.cache /pw-browsers

# So git doesn't complain about unusual permissions
RUN git config --system --add safe.directory /app

#########################
FROM base AS blackboxai-full

ENV blackboxai_DOCKER_IMAGE=paulgauthier/blackboxai-full

COPY . /tmp/blackboxai
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip \
    && /venv/bin/python -m pip install --no-cache-dir /tmp/blackboxai[help,browser,playwright] \
       --extra-index-url https://download.pytorch.org/whl/cpu \
    && rm -rf /tmp/blackboxai

RUN /venv/bin/python -m playwright install --with-deps chromium
RUN find /venv/lib/python3.10/site-packages \( -type d -exec chmod a+rwx {} + \) -o \( -type f -exec chmod a+rw {} + \)

ENTRYPOINT ["/venv/bin/blackboxai"]

#########################
FROM base AS blackboxai

ENV blackboxai_DOCKER_IMAGE=paulgauthier/blackboxai

COPY . /tmp/blackboxai
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip \
    && /venv/bin/python -m pip install --no-cache-dir /tmp/blackboxai[playwright] \
       --extra-index-url https://download.pytorch.org/whl/cpu \
    && rm -rf /tmp/blackboxai

RUN /venv/bin/python -m playwright install --with-deps chromium
RUN find /venv/lib/python3.10/site-packages \( -type d -exec chmod a+rwx {} + \) -o \( -type f -exec chmod a+rw {} + \)

ENTRYPOINT ["/venv/bin/blackboxai"]
