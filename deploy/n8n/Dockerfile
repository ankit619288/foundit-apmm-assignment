FROM node:22-bookworm-slim

ARG N8N_VERSION=2.21.7

ENV NODE_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/apmm-venv/bin:$PATH

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates python3 python3-venv tini \
    && npm install --global "n8n@${N8N_VERSION}" \
    && npm cache clean --force \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/foundit-apmm

COPY requirements.txt /tmp/apmm-requirements.txt
RUN python3 -m venv /opt/apmm-venv \
    && /opt/apmm-venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/apmm-venv/bin/pip install --no-cache-dir -r /tmp/apmm-requirements.txt

COPY --chown=node:node . /opt/foundit-apmm
RUN mkdir -p /home/node/.n8n /opt/foundit-apmm/data /opt/foundit-apmm/outputs \
    && chown -R node:node /home/node /opt/foundit-apmm /opt/apmm-venv

USER node

EXPOSE 5678

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["n8n", "start"]
