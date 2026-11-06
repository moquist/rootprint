# Fixed base; dependency installation happens before any worker credentials exist.
FROM docker.io/library/node:22-bookworm-slim@sha256:aaa4b5baf1ecff3b283486bb1f90405cdda225a3e6f79660d2c559fa510a7292
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv git openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY . .
RUN npm ci --cache /opt/npm-cache \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install -r requirements-dev.txt \
    && /opt/venv/bin/pip download --dest /wheelhouse -r requirements-dev.txt setuptools==80.9.0 \
    && npm run build \
    && npm pack --ignore-scripts --workspace packages/typescript --pack-destination /tmp \
    && npm install --ignore-scripts --cache /opt/npm-cache --prefix /tmp/npm-warm /tmp/rootprint-*.tgz \
    && rm -rf /tmp/npm-warm /tmp/rootprint-*.tgz
RUN mkdir /bridge && cp scripts/worker_sandbox.py /bridge/worker_sandbox.py \
    && mv /work /seed && mkdir /work
ENV PATH="/opt/venv/bin:/usr/local/bin:/usr/bin:/bin" \
    HOME="/tmp/home" PIP_NO_INDEX="1" PIP_FIND_LINKS="/wheelhouse" \
    npm_config_cache="/tmp/npm-cache" npm_config_offline="true" \
    GIT_CONFIG_COUNT="1" GIT_CONFIG_KEY_0="safe.directory" GIT_CONFIG_VALUE_0="/work"
USER 1000:1000
CMD ["sleep", "1800"]
