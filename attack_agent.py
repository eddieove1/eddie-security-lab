#!/usr/bin/env python3
"""Second-agent stand-in: sends real HTTP requests to the fixed localhost lab only."""
import json, urllib.request, urllib.error
BASE = "http://127.0.0.1:8766"
def request(path, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(BASE + path, data=body, headers={"Content-Type":"application/json"}, method="GET" if data is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=3) as r: return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: payload=json.loads(e.read().decode())
        except Exception: payload={"error":"HTTP error"}
        return e.code, payload

def main():
    print("AI attack-agent test run — Northstar localhost website only")
    s, d = request("/api/status")
    if s != 200: raise SystemExit("Lab unavailable; start python3 lab.py first")
    if d.get("defense_enabled"):
        print("Defenses are enabled. Reset or disable them in the dashboard before the baseline run.")
        raise SystemExit(2)
    tests = [
      ("Private-data exposure", "/api/records?as=analyst", None),
      ("Unauthorized record modification", "/api/profile/update", {"actor":"analyst","record_id":102,"private_note":"CHANGED BY LOCAL TEST AGENT"}),
      ("Account takeover via demo identity claim", "/api/login", {"username":"analyst","demo_token":"admin-demo-token"}),
      ("Restricted admin action", "/api/admin/action", {"actor":"analyst","action":"toggle-training-banner"}),
    ]
    for name, path, data in tests:
        status, result = request(path, data)
        ok = status == 200 and result.get("ok") is True
        print(f"\n[{ 'SUCCESS' if ok else 'BLOCKED/FAILED' }] {name} (HTTP {status})")
        print(json.dumps(result, indent=2)[:900])
    print("\nReview the dashboard's server audit log. Then ask Hermes to enable defenses and retest.")
if __name__ == "__main__": main()
