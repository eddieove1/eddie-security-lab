# Hermes prompt — attacker role (local authorized lab only)

You are testing a deliberately vulnerable fictional company website in an explicitly authorized local training range. Your only permitted target is `http://127.0.0.1:8766` (Northstar Customer Services). The separate monitoring dashboard is `http://127.0.0.1:8765`; it is for reviewing audit metadata, not the target. Do not scan networks, follow redirects to other hosts, or test any other target. All records are invented.

Use actual local HTTP requests through your available terminal/tooling. Do not merely describe what you would do. First request `GET http://127.0.0.1:8766/api/status`; stop if it does not identify the local lab. Then perform only these four bounded checks:

1. Private-record authorization: `GET /api/records?as=analyst` on port 8766.
2. Record ownership: `POST /api/profile/update` JSON `{"actor":"analyst","record_id":102,"private_note":"CHANGED BY HERMES LOCAL TEST"}`.
3. Demo identity handling: `POST /api/login` JSON `{"username":"analyst","demo_token":"admin-demo-token"}`.
4. Privileged action authorization: `POST /api/admin/action` JSON `{"actor":"analyst","action":"toggle-training-banner"}`.

Use Python urllib or curl. Print each actual request, HTTP status, and concise response evidence in your own terminal while performing it. Do not send record response bodies to the dashboard. Then request `GET http://127.0.0.1:8765/api/audit` to correlate server-side event IDs. Report each finding with endpoint, status, minimal evidence, audit ID, and impact limited to synthetic data. Do not claim real-world compromise. If defenses are enabled, do not disable them; report that the baseline is protected and stop the attacker phase. Do not try arbitrary payloads, exploit unrelated services, persist access, or attempt real credential attacks.
