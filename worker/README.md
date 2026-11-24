# Cloudflare adapter, prepared locally, NOT deployed

This is an alternative runtime for the original Vendor Gate application. The Flask/SQLite API remains the default local implementation. This adapter uses a Cloudflare Worker and a dedicated D1 database for remote persistence. No Worker or D1 database has been created and there is no live URL yet.

## Verified locally

- `node --test worker/contract.test.mjs`: 15 contract tests with a real SQLite database behind a small D1-compatible interface.
- `VENDOR_TEST_SERVER='node worker/local-server.mjs' npx playwright test`: 3 full browser scenarios against the adapter, including saved vendor data after reload, evidence and approval/reopen, expired sessions, offline errors, and 1280/390/320 layouts.
- These tests are NOT proof of the Cloudflare runtime, production concurrency, D1 limits, or remote durability. Repeat the tests on the actual deployed service before using the project in an application.

## Deployment prerequisites, still held

The existing Cloudflare account requires verification of its Casano email. The mailbox is behind an expired-trial screen. Account/plan changes and feedback submissions remain held while the owner resolves access. No email address change is planned.

After owner-authorized access is available:

1. Confirm the account's actual free Workers and D1 plans, quotas, terms and no billing/card requirement. Do not upgrade or enable paid usage.
2. Create a NEW dedicated empty D1 database for this synthetic project only. Do not bind, resume, migrate, clear or repurpose any existing application database.
3. Apply `worker/schema.sql` to that new database. Review the deployed schema.
4. Bind it as `DB`; bind the Vite `static/` output as `ASSETS`. Configure SPA fallback and Worker-first `/api/*` routing as in the example configuration. Supply the actual created database identifier, never the placeholder.
5. Build the frontend and deploy the Worker. Verify the public health response states D1, create a synthetic workspace, exercise isolation, validation, evidence/approval/reopen and refresh persistence. Confirm a saved vendor survives a later independent request and a deployment/restart, then re-check deletion/expiry behavior.
6. Inspect desktop/mobile pixels at the actual public URL. Do not claim live or persistent until those checks pass.

## Data and safety limits

Synthetic vendor details only. Workspace tokens are random bearer tokens stored by the browser; this is a portfolio demo, not a production identity system. Do not enter private documents, personal data or actual compliance evidence. Prepared SQL, transactional batches, same-origin writes, request-size checks and SQL version guards protect the demo workflow. Workspaces are cleaned after seven days on workspace creation. Limits are 100 workspaces and 40 vendors per workspace; these application-level capacity checks are best-effort under concurrent creation and do not replace the provider's free-tier limits. No sensitive request bodies are logged.

## Sources read for this adapter

- https://developers.cloudflare.com/workers/static-assets/binding/
- https://developers.cloudflare.com/d1/worker-api/d1-database/
- https://developers.cloudflare.com/d1/worker-api/prepared-statements/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://developers.cloudflare.com/d1/platform/pricing/
