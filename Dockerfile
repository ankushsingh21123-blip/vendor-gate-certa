FROM node:22-slim AS frontend
WORKDIR /app
COPY package.json package-lock.json vite.config.ts ./
COPY web ./web
RUN npm ci --ignore-scripts && npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=4178 VENDOR_DB_PATH=/data/vendor-gate.sqlite3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && groupadd -g 10001 demo && useradd -u 10001 -g demo -M demo && mkdir /data && chown demo:demo /data
COPY api ./api
COPY start.sh ./
COPY --from=frontend /app/static ./static
USER demo
EXPOSE 4178
CMD ["sh","start.sh"]
