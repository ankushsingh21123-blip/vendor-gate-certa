# Persistent-disk deployment preparation

This recipe is unhosted. No provider account, terms, payment, database or remote resources have been created by adding it. A provider's free offer and writable persistent mount still need verification before deployment.

## Container contract

- Build with `docker build -t vendor-gate .`.
- Mount a NEW dedicated writable volume at `/data`.
- Set `VENDOR_DB_PATH=/data/vendor-gate.sqlite3` and `PORT` to the platform's assigned port.
- Start the image normally. Gunicorn binds `0.0.0.0:$PORT` with one worker, appropriate for this bounded SQLite demo.
- Read `/api/health` to check process and database access. Open `/` to check the built frontend.
- Create a synthetic workspace and vendor, replace the container on the same volume, and verify the saved vendor and audit history from the same workspace.
- Do not use serverless ephemeral `/tmp` as durable storage, repurpose an existing database, or scale replicas independently against separate SQLite files.

`python test_runtime.py` checks the production launcher on a disposable local database and nondefault port. It creates a vendor, stops and replaces the process with the same database, and verifies vendor/audit persistence. This is a LOCAL PROCESS test, not a Docker or hosting test. Container and selected-provider acceptance remain separate work.

No secrets, personal data or customer data belong in this synthetic portfolio demo. Workspace tokens are bearer credentials, not real account authentication. Existing seven-day cleanup and demo caps still apply.
