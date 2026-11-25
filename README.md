# Vendor Gate

An original, AI-assisted synthetic vendor due-diligence workspace built for a frontend engineering portfolio. Not affiliated with Certa. Not an employer assessment, production compliance system, real-customer project or claim of unaided authorship.

## Current status

Local implementation and tests complete. **Not deployed yet.** No hosted persistence claim. A SQLite file in a serverless `/tmp` directory is not durable storage, and is not a supported production deployment for this project.

## Role-specific implementation

- React/TypeScript interface with nested protected routes and URL-backed register filters.
- Original vendor schema, risk rules, evidence checklist, approval state machine and server-recorded audit trail.
- Client loading, offline, validation, missing-vendor and expired-session states.
- Approval blocked server-side until risk-dependent evidence is recorded. Approved vendors lock evidence until review is reopened.
- Every change carries an optimistic version. Stale tabs receive 409 instead of overwriting another change.
- Isolated random demo workspace tokens, seven-day cleanup, 100-workspace and 40-vendor caps, same-origin writes and parameterized SQL.
- Desktop table becomes stacked cards on mobile. Keyboard focus, labels, live status and inert text rendering.

## Stack

React, TypeScript, React Router and Vite frontend; Python Flask HTTP API; SQLite persistence. The workspace token is a bearer credential stored in sessionStorage, not a real user authentication system. Synthetic data only. Do not enter customer, personal or confidential information. There is no document authenticity check, sanctions screening or AI risk prediction.

## Run locally

Use Node 22+ and Python 3.10+.

```
npm ci
python -m pip install -r requirements.txt
npm run build
python api/index.py
```

Open http://127.0.0.1:4178. `VENDOR_DB_PATH` chooses the SQLite database file, default `/tmp/vendor-gate.sqlite3`. For persistent hosting it MUST point to a supported persistent disk. Back up demo data only if needed; it is disposable and expires after seven days. `SESSION_SECRET` is optional in the current bearer-session design, reserved for future signed-session work. Never commit secrets.

## Verify

```
python -m unittest test_api -v
npm test
npx playwright install chromium
npx playwright test
```

Playwright starts the Flask server automatically. Set `VENDOR_TEST_SERVER` only if a custom virtual-environment command is needed. No credentials are required.

24 November 2026 local evidence: 15 API tests, 11 component/model tests and 3 browser scenarios passed. Browser scenarios exercise validation, evidence-gated approval, reload persistence, re-open review, filters, expired sessions and offline errors. Responsive screenshots at 320, 390 and 1280 pixels were inspected. `npm audit` reported zero known advisories at that check. These are local results, not hosted acceptance or a security certification.

## State ownership

URL search parameters own filters. Browser sessionStorage owns only the isolated workspace identifier. The server owns vendor state, risk, evidence, version and audit events. Risk rules and evidence gates cannot be bypassed by changing browser controls.

## Risk rules

Annual USD amount: <20k = 0, 20k–99,999 = 1, >=100k = 2. Data: none = 0, personal = 1, sensitive = 2. Country: India/UK/US/Singapore = 0, other = 1. Score 0 is low, 1–2 medium, 3+ high. Low requires business evidence, medium adds privacy, high adds security and financial. These arbitrary demo rules are transparent, not legal or compliance recommendations.

## Limitations

No real login, role-based authorization, signed audit export, malware/file scanning or production anti-abuse controls. A workspace bearer token must not be used for private records. SQLite serializes writes and suits this bounded single-worker demo, not a scaled multi-instance service. Public anonymous workspace creation can exhaust the cap. Add shared edge throttling before open production use. No paid host, card, trial or automatic upgrade is part of this source.

MIT-licensed project code. React/React Router/Vite/Vitest/Flask and other dependencies retain their own licences. Substantial AI assistance was used for implementation, debugging and tests.

## Alternative hosting adapter, prepared locally

`worker/` contains an original Workers/D1 adapter with 15 SQLite-backed contract tests and 3 passing browser scenarios. No Cloudflare Worker or D1 database exists yet. These are local simulations, not production runtime or remote durability proof. See `worker/README.md` for the held prerequisites. The example configuration intentionally has no real database ID.

## Portable deployment preparation, 25 November

`start.sh` uses Gunicorn, one worker and the assigned `PORT`, binding all interfaces. `Dockerfile` and `.dockerignore` prepare a non-root image and dedicated persistent `/data` mount. Local acceptance of production-process replacement passed: frontend, database health, evidence/audit persistence on a nondefault port. This is not a Docker run or a provider deployment. See `DEPLOYMENT.md`; the account, final free offer and supported storage must still be checked.
