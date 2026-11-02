# AI Security Live Lab — two-site version

This lab has two separate localhost sites, like a vulnerable company website and a security operations dashboard. It uses Python's standard library and fictional records only.

- **Company target:** http://127.0.0.1:8766
- **SOC monitoring dashboard:** http://127.0.0.1:8765

## Start

```bash
python3 lab.py
```

Open both links in separate browser tabs. The company site is the thing Hermes tests. The SOC dashboard is a separate observer that records request metadata, outcomes, timestamps, and event IDs. It never displays customer names, emails, private notes, or full response bodies. Its event table synchronizes automatically every 2.5 seconds. Opening or refreshing either page does not query private records or create audit events. Only explicit API requests to the target generate events.

## Conference sequence

1. Start the lab and show the audience the company site on port 8766 and the SOC dashboard on port 8765. The audit timeline should be empty.
2. Keep the target defenses disabled. In your Hermes terminal, provide the complete contents of `HERMES_ATTACKER_PROMPT.md`. Hermes should make actual HTTP requests to port 8766, print observed responses in its terminal, and correlate event IDs from the monitor API.
3. Keep the SOC dashboard open. It should show metadata-only audit events from the requests Hermes actually made within a few seconds. The record contents, if returned by the vulnerable endpoint, are visible only in Hermes's terminal/response and not copied to the dashboard.
4. For a repeatable baseline without Hermes, run `python3 attack_agent.py`. This is a deterministic HTTP test agent, not an LLM; label it honestly if you show it.
5. Give Hermes the complete contents of `HERMES_DEFENDER_PROMPT.md`. Hermes should inspect the audit, enable server-side controls through the local monitor API, retest the same routes, and produce a terminal/report comparison.
6. Refresh the SOC dashboard and compare successful vulnerable actions with blocked retests.

## What is intentionally weak

With defenses disabled, the local training target demonstrates private-record authorization failure, missing record-ownership checks, accepting a client-supplied demo identity claim, and a missing role check for a fictional admin action. When defenses are enabled, server-side checks reject those actions. Effects are restricted to in-memory invented data.

## Scope and limitations

Both services bind only to `127.0.0.1`; do not change this or expose either port to a LAN or the internet. The app has no real customers, real accounts, external calls, or persistent database. Hermes is the live AI only when you run it in your installed Hermes environment. The bundled `attack_agent.py` is deterministic, not an LLM. The defense toggle is a training control, not a production patch or a security certification. This demo does not implement SQL injection.
